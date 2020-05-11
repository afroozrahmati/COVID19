import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication,QDialog
from PyQt5.uic import loadUi
from DataManagment import *

class LoginPage(QDialog):
    def __init__(self):
        super(LoginPage,self).__init__()
        loadUi('loginpage.ui',self)
        self.setWindowTitle('login page')
        self.BtnLogin.clicked.connect(self.on_pushButton_clicked)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        db=DataManagment()        
        result=db.is_authenticate(self.txtUserName.text(),self.txtPassword.text())
        db.connect_close()
        if not result:
            self.lblError.setText("The username/Password is incorrect, please try again!")
            return
        
    

app= QApplication(sys.argv)
widget=LoginPage()
widget.show()
sys.exit(app.exec_())
