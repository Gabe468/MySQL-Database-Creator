import sys
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton,QVBoxLayout,QHBoxLayout, QGridLayout, QLabel, QWidget, QLineEdit, QFrame
from root import Error, Connect

class Login(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDC")

        #layout
        self.layout = QGridLayout( )
        labell = QLabel("MYSQL Database Creator")
        self.layout.addWidget(labell,0,0)

        #Username text and box
        self.labelu = QLabel("Username:")
        self.layout.addWidget(self.labelu,1,0)
        self.usern = QLineEdit()
        self.usern.setFixedWidth(100)
        self.layout.addWidget(self.usern,1,1)

        #Password text and box
        labelp = QLabel("Password:")
        self.layout.addWidget(labelp,2,0)
        self.passw = QLineEdit()
        self.passw.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.passw,2,1)
        self.passw.setFixedWidth(100)

        #Submit Button
        self.buttons = QPushButton("Submit")
        self.buttons.clicked.connect(self.submit)
        self.layout.addWidget(self.buttons,3,1)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setMenuWidget(widget)

        #Window params
        self.setFixedHeight(130)
        self.setFixedWidth(300)

        global usernstring
        usernstring = self.usern

    def submit(self):
        try:
            Connect.connection(self.usern.text(), self.passw.text())
            self.close()
            self.window = mainPage()
            self.window.show()

        except Error as e:
            labele = QLabel(str(e))
            labele.setStyleSheet("color: red;")
            self.layout.addWidget(labele,3,0)
            self.setFixedHeight(150)


    
class mainPage(QMainWindow):

    def __init__(self):
        super().__init__()


        self.resize(600, 600)
        self.setFixedHeight(900)
        self.setFixedWidth(900)
        self.setWindowTitle("MDC")

        self.Body = QGridLayout()
        labelp = QLabel("Hello "+ (usernstring.text()).upper())
        self.Body.addWidget(labelp,0,0)

        self.createdd = QPushButton("Create Database")
        self.Body.addWidget(self.createdd,1,0)
        self.createdd.clicked.connect(self.cDatabase)

        self.deleted = QPushButton("Delete Database")
        self.Body.addWidget(self.deleted,1,1)
        self.deleted.clicked.connect(self.dDatabase)

        self.createdt = QPushButton("Create Table")
        self.Body.addWidget(self.createdt,1,2)
        self.createdt.clicked.connect(self.cTable)

        self.deletet = QPushButton("Drop Table")
        self.Body.addWidget(self.deletet,1,3)
        self.deletet.clicked.connect(self.dTable)

        self.search = QPushButton("Search")
        self.Body.addWidget(self.search,2,0)





        widget1 = QWidget()
        widget1.setLayout(self.Body)
        self.setMenuWidget(widget1)


    def cDatabase(self, checked):
        self.w = createDatabase()
        self.w.show()

    def dDatabase(self, checked):
        self.w = deleteDatabase()
        self.w.show()

    def cTable(self, checked):
        self.w = createTable()
        self.w.show()
    
    def dTable(self, checked):
        self.w = dropTable()
        self.w.show()
    
    def search(self, checked):
        self.w = Search()
        self.w.show()

class createDatabase(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDC")
        layout = QGridLayout()
        self.enterl = QLabel("Enter Database Name")
        

        self.entert = QLineEdit()
        self.entert.setFixedWidth(150)

        self.enterb = QPushButton("Enter")

        layout.addWidget(self.enterl)
        layout.addWidget(self.entert)
        layout.addWidget(self.enterb)
        self.setLayout(layout)

        self.enterl.setFixedWidth(150)
        self.setFixedHeight(105)
        self.setFixedWidth(200)

class deleteDatabase(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDC")
        layout = QGridLayout()
        self.enterl = QLabel("Enter Database Name")
        

        self.entert = QLineEdit()
        self.entert.setFixedWidth(150)

        self.enterb = QPushButton("Enter")

        layout.addWidget(self.enterl)
        layout.addWidget(self.entert)
        layout.addWidget(self.enterb)
        self.setLayout(layout)

        self.enterl.setFixedWidth(150)
        self.setFixedHeight(105)
        self.setFixedWidth(200)

class createTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDC")
        layout = QGridLayout()
        self.enterl = QLabel(" Enter Table Name")
        

        self.entert = QLineEdit()
        self.entert.setFixedWidth(130)

        self.enterb = QPushButton("Enter")

        layout.addWidget(self.enterl)
        layout.addWidget(self.entert)
        layout.addWidget(self.enterb)
        self.setLayout(layout)

        self.enterl.setFixedWidth(130)
        self.setFixedHeight(105)
        self.setFixedWidth(200)

class dropTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDC")
        layout = QGridLayout()
        self.enterl = QLabel(" Enter Table Name")
        

        self.entert = QLineEdit()
        self.entert.setFixedWidth(130)

        self.enterb = QPushButton("Enter")

        layout.addWidget(self.enterl)
        layout.addWidget(self.entert)
        layout.addWidget(self.enterb)
        self.setLayout(layout)

        self.enterl.setFixedWidth(130)
        self.setFixedHeight(105)
        self.setFixedWidth(200)

class Search(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDC")
        layout = QGridLayout()
        self.enterl = QLabel(" Enter name")
        

        self.entert = QLineEdit()
        self.entert.setFixedWidth(130)

        self.enterb = QPushButton("Enter")

        layout.addWidget(self.enterl)
        layout.addWidget(self.entert)
        layout.addWidget(self.enterb)
        self.setLayout(layout)

        self.enterl.setFixedWidth(130)
        self.setFixedHeight(105)
        self.setFixedWidth(200)


app = QApplication(sys.argv)

window = Login()
with open("styles.css","r") as file:
    app.setStyleSheet(file.read())
window.show()

app.exec()