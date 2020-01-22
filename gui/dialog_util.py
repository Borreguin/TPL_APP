import logging, time
import sys, os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTableWidgetItem, QHeaderView, QMainWindow
import pyqt5ac
import datetime as dt
from my_lib import utils as u
from threading import Thread
from my_lib import log_util as lu
from functools import partial
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

# procesando información en paralelo:
lst_th = list()
to_process = dict()
# importando los archivos generados:
from gui.dialog import Ui_MainWindow
from gui import DF_Window

# Table order:
c_select = 0
c_archive = 1
c_action = 3
c_p_frontera = 2
c_estado = 4
labels = ('-', 'Archivo', 'P. Frontera', 'Acciones', 'Estado')

class tpl_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(tpl_window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_load_files.clicked.connect(self.open_file_names_dialog)
        self.ui.about_software.triggered.connect(self.open_about_window)
        self.ui.dateEdit.setDate(dt.datetime.now().date())
        self.ui.tb_files.setColumnCount(len(labels))
        self.ui.tb_files.setHorizontalHeaderLabels(labels)
        self.ui.tb_files.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.ui.btn_proccess_files.clicked.connect(self.process_all_df)
        self.ui.tb_files.resizeColumnsToContents()

    def open_file_names_dialog(self):
        to_process = dict()
        self.ui.tb_files.clear()
        self.ui.tb_files.setColumnCount(len(labels))
        self.ui.tb_files.setHorizontalHeaderLabels(labels)
        self.ui.tb_files.setRowCount(0)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccione los archivos a procesar", input_path,
                                                "All Files (*);;Excel XLSX (*.xlsx);; Excel XLS (*.xls);; ;;",
                                                initialFilter="Excel XLS (*.xls)",
                                                options=options)
        self.process_files(files)
        return files

    def process_files(self, files_name):
        if len(files_name) > 0:
            self.ui.tb_files.setRowCount(len(files_name))
            for ix, file in enumerate(files_name):
                f = str(file).split("/")[-1]
                self.ui.tb_files.setItem(ix, c_archive, QTableWidgetItem(f))
                self.ui.tb_files.setItem(ix, c_estado, QTableWidgetItem("Leyendo archivo... "))

                # p_frontera:
                p_frontera = u.read_config(f)
                if p_frontera is None:
                    self.ui.tb_files.setItem(ix, c_p_frontera, QTableWidgetItem("temp_" + str(ix)))
                else:
                    self.ui.tb_files.setItem(ix, c_p_frontera, QTableWidgetItem(p_frontera))

                # check box to work with:
                cBox = QtWidgets.QCheckBox()
                cBox.setDisabled(True)
                cBox.setStyleSheet("QCheckBox::indicator { "
                                   "subcontrol-origin: padding; "
                                   "subcontrol-position: center; "
                                   "}")
                self.ui.tb_files.setCellWidget(ix, c_select, cBox)

                # botones de acción:
                btn = QtWidgets.QPushButton("Desplegar archivo")
                btn.setDisabled(True)
                self.ui.tb_files.setCellWidget(ix, c_action, btn)

                # Nombres propuestos:
                proposed_name = u.read_config(f)
                if proposed_name is not None:
                    self.ui.tb_files.setItem(ix, c_p_frontera, QTableWidgetItem(proposed_name))
        self.reading_files(files_name)

    def reading_files(self, files):
        for ix, file in enumerate(files):
            # Leyendo los archivos de Excel:
            t = Thread(target=self.populate_row, kwargs=dict(ix=ix, file=file))
            t.start()
            lst_th.append(t)

        # for l in lst_th:
        #    time.sleep(2)
        #    l.join()
        self.ui.tb_files.resizeColumnsToContents()

    def populate_row(self, ix, file):
        # leyendo el archivo Excel
        success, df, msg = u.read_excel_file(file)
        self.ui.tb_files.setItem(ix, c_estado, QTableWidgetItem(msg))
        f = str(file).split("/")[-1]
        to_process[f] = df
        try:
            # button
            item = self.ui.tb_files.cellWidget(ix, c_action)
            if item is not None:
                item.setDisabled(False)
                item.setChecked(True)
                item.clicked.connect(partial(self.show_file, f))

            if success:
                # setting for choosing correct files:
                # checkbox
                item = self.ui.tb_files.cellWidget(ix, c_select)
                item.setDisabled(False)
                item.setChecked(True)
        except Exception as e:
            print(str(e))

        self.ui.tb_files.resizeColumnsToContents()

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == QtCore.Qt.Key_A:
            self.open_file_names_dialog()

    def show_file(self, file_name):
        self.window = QtWidgets.QMainWindow()
        self.ui2 = DF_Window.Ui_DF_Window()
        self.ui2.setupUi(self.window)
        self.window.setWindowTitle(file_name)
        df = to_process[file_name]
        self.ui2.tb_DF.setColumnCount(len(df.columns))
        self.ui2.tb_DF.setRowCount(len(df.index))
        self.ui2.tb_DF.setHorizontalHeaderLabels(tuple(df.columns))
        for ix in df.index:
            for jx, column in enumerate(df.columns):
                if type(df[column].loc[ix]) is dt.date:
                    self.ui2.tb_DF.setItem(ix, jx, QTableWidgetItem(df[column].loc[ix].strftime("%m/%d/%Y")))
                else:
                    self.ui2.tb_DF.setItem(ix, jx, QTableWidgetItem(str(df[column].loc[ix])))

        self.ui2.tb_DF.resizeColumnsToContents()
        self.window.show()

    @staticmethod
    def open_about_window():
        msgBox = QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle("Acerca del software")
        msgBox.setText("Creado por: Roberto Sánchez (rg.sanchez.a@gmail.com)")
        msgBox.setInformativeText("Sistemas de Tiempo Real \nrsanchez@cenace.or.ec"
                                  "\n\nEnero 2020 ")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.setDefaultButton(QMessageBox.Ok)
        msgBox.exec_()

    def process_all_df(self):
        n = self.ui.tb_files.rowCount()
        for ix in range(n):
            item = self.ui.tb_files.cellWidget(ix, c_select)
            p_frontera = "temp_" + str(ix)
            if item is not None:
                p_frontera = self.ui.tb_files.item(ix, c_p_frontera).text()

            if item.isChecked():
                excel_file = self.ui.tb_files.item(ix, c_archive).text()
                success, msg = u.transform_info(to_process[excel_file], p_frontera)
                self.ui.tb_files.setItem(ix, c_estado, QTableWidgetItem(msg))
                u.save_config(excel_file, p_frontera)
        self.ui.tb_files.resizeColumnsToContents()

# New window for DF




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