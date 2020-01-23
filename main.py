import logging
from sys import path as sysPath
from os import path, mkdir, makedirs
from PyQt5 import QtWidgets

""" Variables globales"""
script_path = path.dirname(path.abspath(__file__))
gui_path = path.join(script_path, "gui")
input_path = path.join("c:\\", "SIMEC")
output_path = path.join("c:\\", "SIMEC", "TPL", "salida")
logs_path = path.join(script_path, "logs")
lg = logging.getLogger("main")

directories = [gui_path, input_path, output_path, logs_path]


def run_application():

    app = QtWidgets.QApplication([])
    application = du.tpl_window()
    application.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    import sys
    for d in directories:
        if not path.exists(d):
            makedirs(d)
            sysPath.append(d)
    from gui import dialog_util as du
    run_application()