import os
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
os.environ['QT_SCALE_FACTOR'] = '1'
os.environ['QT_SCREEN_SCALE_FACTORS'] = '1'

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        
        # Set the main window background color
        MainWindow.setStyleSheet("background-color: #1f306e;")
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Create a label to hold the background image
        self.background_label = QtWidgets.QLabel(self.centralwidget)
        self.background_label.setGeometry(0, 0, 1200, 800)
        pixmap = QtGui.QPixmap("C:/Users/Dell Pc/Desktop/lol.jpg")
        if pixmap.isNull():
            print("Error: Unable to load image. Please check the path.")
        else:
            self.background_label.setPixmap(pixmap.scaled(1200, 800, QtCore.Qt.KeepAspectRatioByExpanding))
        self.background_label.setObjectName("background_label")
        
        # Increase the button size
        button_width = 250
        button_height = 250
        window_width = 1200
        window_height = 800
        button_x = (window_width - button_width) // 2
        button_y = (window_height - button_height) // 2
        
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(button_x, button_y, button_width, button_height))
        self.start_button.setObjectName("start_button")
        
        # Set the stylesheet for the start button
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #042A78;
                border: 2px solid #042A78;
                border-radius: 125px;  /* Half of the width/height to make it circular */
                color: white;
                font-size: 30px;
            }
            QPushButton:hover {
                background-color: #4C54AD;
            }
            QPushButton:pressed {
                background-color: #4C54AD;
            }
        """)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Voice Assistant"))
        self.start_button.setText(_translate("MainWindow", "Start"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
