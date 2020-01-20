import logging
import sys, os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QHeaderView
import pyqt5ac
import datetime as dt

from my_lib import log_util as lu
# https://likegeeks.com/pyqt5-tutorial/
""" Variables globales"""
script_path = os.path.dirname(os.path.abspath(__file__))
lg = logging.getLogger("dialog_util")
lg.addHandler(lu.SQLiteHandler())

""" Generando GUI desde archivo dialog.ui"""
gui_file = os.path.join(script_path, "dialog.ui")
gui_py_path = os.path.join(script_path, "dialog.py")
input_path = script_path.replace("gui", "input")
resource_path = os.path.join(script_path, "resources")
resource_py_path = os.path.join(script_path, "resource_rc.py")

""" Añadiendo algunos recursos a la variable PATH"""
sys.path.append(resource_path)

# transformando el GUI a código Python:
pyqt5ac.main(rccOptions='', force=False, config='',
                 ioPaths=[[script_path + '/*.ui', script_path + '/%%FILENAME%%.py'],
                          [resource_path + '/*.qrc', resource_path + '/%%FILENAME%%_rc.py']])


# importando el archivo generado:
from gui.dialog import Ui_MainWindow


class tpl_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(tpl_window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_load_files.clicked.connect(self.open_file_names_dialog)
        self.ui.about_software.triggered.connect(self.open_about_window)
        self.ui.dateEdit.setDate(dt.datetime.now().date())
        self.ui.tb_files.setColumnCount(3)
        self.ui.tb_files.setHorizontalHeaderLabels(('Archivo', 'Estado', 'Acción'))
        self.ui.tb_files.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)


    def open_file_names_dialog(self):
        self.ui.tb_files.setRowCount(0)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccione los archivos a procesar", input_path,
                                                "All Files (*);;Excel XLSX (*.xlsx);; Excel XLS (*.xls);; ;;",
                                                initialFilter="Excel XLS (*.xls)",
                                                options=options)
        if len(files) > 0:
            self.ui.tb_files.setRowCount(len(files))
            for ix, file in enumerate(files):
                f = str(file).split("/")[-1]
                self.ui.tb_files.setItem(ix, 0, QTableWidgetItem(f))

        self.ui.tb_files.resizeColumnsToContents()


        return files

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == QtCore.Qt.Key_A:
            self.open_file_names_dialog()



    def open_about_window(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle("Acerca del software")
        msgBox.setText("Creado por: Roberto Sánchez (rg.sanchez.a@gmail.com)")
        msgBox.setInformativeText("Sistemas de Tiempo Real \nrsanchez@cenace.or.ec"
                                  "\n\nEnero 2020 ")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.exec_()

"""

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Seleccione los archivos a procesar'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog()
        self.openFileNamesDialog()
        self.saveFileDialog()

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Excel Files (*.xlsx)", options=options)
        if fileName:
            print(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Excel Files (*.xlsx)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Excel Files (*.xlsx)", options=options)
        if fileName:
            print(fileName)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
    
"""