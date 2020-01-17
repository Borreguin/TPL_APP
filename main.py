import pandas as pd, logging, os
from my_lib import utils as u
from my_lib import log_util as lu
lg = logging.getLogger("main")

""" Variables globales"""
script_path = os.path.dirname(os.path.abspath(__file__))
node_path = os.path.join(script_path, "nodes")


def run_process():
    file_name = os.path.join(script_path, "input", "KCOLTU - test.xls")
    success, df = u.read_excel_file(file_name)
    print(df.columns)
    print(df)

run_process()