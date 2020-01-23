# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\proyectos\TPL_APP\gui\DF_Window.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DF_Window(object):
    def setupUi(self, DF_Window):
        DF_Window.setObjectName("DF_Window")
        DF_Window.setWindowModality(QtCore.Qt.WindowModal)
        DF_Window.resize(831, 774)
        self.centralwidget = QtWidgets.QWidget(DF_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tb_DF = QtWidgets.QTableWidget(self.centralwidget)
        self.tb_DF.setObjectName("tb_DF")
        self.tb_DF.setColumnCount(0)
        self.tb_DF.setRowCount(0)
        self.verticalLayout.addWidget(self.tb_DF)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        DF_Window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(DF_Window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 831, 26))
        self.menubar.setObjectName("menubar")
        DF_Window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(DF_Window)
        self.statusbar.setObjectName("statusbar")
        DF_Window.setStatusBar(self.statusbar)

        self.retranslateUi(DF_Window)
        QtCore.QMetaObject.connectSlotsByName(DF_Window)

    def retranslateUi(self, DF_Window):
        _translate = QtCore.QCoreApplication.translate
        DF_Window.setWindowTitle(_translate("DF_Window", "MainWindow"))
