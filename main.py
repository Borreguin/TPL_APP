import pandas as pd, logging, os
from my_lib import utils as u
from my_lib import log_util as lu
from gui import dialog_util as du
from PyQt5 import uic
from PyQt5 import QtWidgets


""" Variables globales"""
script_path = os.path.dirname(os.path.abspath(__file__))
node_path = os.path.join(script_path, "nodes")
lg = logging.getLogger("main")


def run_application():
    # file_name = os.path.join(script_path, "input", "KCOLTU - test.xls")
    # success, df = u.read_excel_file(file_name)
    # print(df.columns)
    # print(df)

    app = QtWidgets.QApplication([])
    application = du.tpl_window()
    application.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    import sys
    run_application()