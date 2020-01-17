from datetime import datetime as dt
from datetime import timedelta
import logging
import os, numpy as np
import pandas as pd
from my_lib import log_util as lu

lg = logging.getLogger("utils")
lg.addHandler(lu.SQLiteHandler())

script_path = os.path.dirname(os.path.abspath(__file__))
config_file = script_path.replace("my_lib", "config.json")
name = ""


def read_excel_file(file_name:str):
    global name
    name = file_name.split('\\')[-1]
    print("[{0}] Processing file".format(name))
    try:
        df = pd.read_excel(file_name)
        df.dropna(inplace=True)
        # check si las columnas del archivo son correctas:
        success, result = valid_columns_names(list(df.columns))
        if not success:
            lg.exception(result)
            return False, result
        df.columns = result

        # check si las fechas son correctas en la columna FECHA
        df.sort_values(by=["FECHA"], inplace=True)
        success, date, timestamp, msg = check_dates_in_a_list(list(df['FECHA']))
        if not success:
            lg.exception(msg)
            return False, msg

        df["FECHA"] = date
        df["HORA"] = timestamp
        or_columns = ["FECHA", "HORA"]
        df_final = df[or_columns].copy()

        # check si el numero de periodos es 96:
        if len(df.index) != 96:
            msg = "[{0}] El archivo no contiene 96 periodos. \n " \
                  "Número de periodos: [{1}]".format(name, len(df.index))
            return False, msg

        # check si el dataframe contiene solo números:
        df.drop(columns=or_columns, inplace=True)
        check_if_is_number = np.vectorize(lambda x: np.issubdtype(x, np.number))
        is_number = check_if_is_number(df.dtypes)
        if not all(is_number):
            ix_c = [i for i, x in enumerate(is_number) if not x]
            cls = [df.columns[ix] for ix in ix_c]
            msg = "[{0}] El archivo contiene valores no reconocidos como números " \
                  "en las columnas [{1}]".format(name, cls)
            lg.exception(msg)
            return False, msg
        df_final = pd.concat([df_final, df], axis=1)
        return True, df_final

    except Exception as e:
        print(e)
        return None

def get_columns_by_default():
    check_json = os.path.exists(config_file)
    columns = ['FECHA', 'AS (kWh)', 'AE (kWh)', 'RS (kVARh)', 'RE (kVARh)']
    if check_json:
        parameter = read_config("columnas")
        if parameter is not None:
            columns = parameter
        else:
            save_config("columnas", columns)
    else:
        save_config("columnas", columns)
    return columns

def valid_columns_names(columns_to_check):
    global name
    columns = get_columns_by_default()
    columns_a = [c.replace(" ", "") for c in columns]
    columns_a = [c.upper() for c in columns_a]

    columns_to_check = [c.replace(" ", "") for c in columns_to_check]
    columns_to_check = [c.upper() for c in columns_to_check]
    if list(columns_to_check) != columns_a:
        msg = "[{0}] Archivo con formato incorrecto en columnas. \n " \
              "Las columnas no coinciden con el formato {1}".format(name, columns)
        print(msg)
        lg.error(msg)
        return False, msg
    return True, columns


def get_default_date_formats():
    default_formats = read_config("fecha_formato")
    if default_formats is None:
        default_formats = ["%m/%d/%Y@%H:%M:%S.%f", "%m/%d/%Y@%H:%M:%S", "%m/%d/%Y@%H:%M",
                           "%m-%d-%Y@%H:%M:%S.%f", "%m-%d-%Y@%H:%M:%S", "%m-%d-%Y@%H:%M"]
        save_config("fecha_formato", default_formats)
    return default_formats


def check_str_as_date(str_value):
    default_formats = get_default_date_formats()
    f = None
    d = None
    for test_format in default_formats:
        try:
            d = dt.strptime(str_value, test_format)
            f = test_format
            break
        except:
            pass
    return d, f


def check_dates_in_a_list(str_lst:list):
    # chequear si cada str de tiempo tiene el formato establecido
    # excepto el último ya que tiene formato: m/d/y@24:00:00
    # (no reconocido como estandard)
    result = [check_str_as_date(value) for value in str_lst[:-1]]
    # El formato es único?
    fmts = list(set([r[1] for r in result]))
    fmts.sort()
    # tratar la hora m/d/y@24:00:00 como caso especial
    date, time = str_lst[-1].split("@")

    # si el formato es único
    if len(fmts) == 1:
        dates = [r[0].date() for r in result]
        times = [r[0].time().strftime("%H:%H:%S") for r in result]
        try:

            fmt_date, fmt_time = fmts[0].split("@")
            date = dt.strptime(date, fmt_date)
            time_is_ok = "24:00" in time
            date_is_ok = (date.date() == dates[0]) and len(set(dates)) == 1

            if time_is_ok:
                time = "24:00:00"
            if date_is_ok and time_is_ok:
                dates.append(date.date())
                times.append(time)
                return True, dates, times, "Formato detectado: {0}".format(fmts[0])

            return False, None, None, "Problemas en detectar la fecha (revise hora 24h, " \
                                      "o hay fechas diferentes en el archivo): [{0}]".format(str_lst[-1])

        except Exception as e:
            lg.error(e)
    elif len(fmts) > 1:
        return False, None, None, "Se ha detectado más de un formato de fecha: [{0}]".format(fmts)

    return False, None, None, "No se ha podido detectar la fecha del archivo"


def read_config(parameter):
    check_json = os.path.exists(config_file)
    if check_json:
        df_config = pd.read_json(config_file)
        if parameter in df_config.index:
            return df_config["Value"][parameter]
    return None


def save_config(parameter_name, parameter_value):
    check_json = os.path.exists(config_file)
    df_config = pd.DataFrame(columns=["Value"])
    if check_json:
        df_config = pd.read_json(config_file)

    df_config.loc[parameter_name] = [parameter_value]
    try:
        df_config.to_json(config_file)
        return True, "El parámetro {0} fue ingresado".format(parameter_name)
    except Exception as e:
        lg.error(e)
        return False, "Error: {0}".format(e)


def transform_info(df: pd.DataFrame):
    clmn = get_columns_by_default()
    'AS (kWh)', 'AE (kWh)', 'RS (kVARh)', 'RE (kVARh)'
    df_t = pd.DataFrame(columns=["sp_1", "FECHA", "HORA", "sp_2", "ql_0", "sp_3", "p",
                                 "sp_4", clmn[0], "sp_5", "ql_1",
                                 "sep_6", clmn[1], "sp_7", "ql_2",
                                 "sp_8", clmn[2], "sp_9", "ql_3",
                                 "sp_10", clmn[3], "sp_11", "ql_4", "end"])

