import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton,QVBoxLayout,QHBoxLayout, QGridLayout, QLabel, QWidget, QLineEdit, QFrame
from root import Error, Connect

class Login(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDC")

        #layout
        global layout2
        layout2 = QGridLayout( )
        labell = QLabel("MYSQL Database Creator")
        layout2.addWidget(labell,0,0)

        #Username text and box
        self.labelu = QLabel("Username:")
        layout2.addWidget(self.labelu,1,0)
        self.usern = QLineEdit()
        self.usern.setFixedWidth(100)
        layout2.addWidget(self.usern,1,1)

        #Password text and box
        labelp = QLabel("Password:")
        layout2.addWidget(labelp,2,0)
        self.passw = QLineEdit()
        layout2.addWidget(self.passw,2,1)
        self.passw.setFixedWidth(100)

        #Submit Button
        self.buttons = QPushButton("Submit")
        self.buttons.clicked.connect(self.submit)
        layout2.addWidget(self.buttons,3,1)

        widget = QWidget()
        widget.setLayout(layout2)
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
            layout2.addWidget(labele,3,0)
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

        created = QPushButton("Create Database")
        self.Body.addWidget(created,1,0)
        created = QPushButton("Delete Database")
        self.Body.addWidget(created,1,1)
        created = QPushButton("Create Table")
        self.Body.addWidget(created,1,2)
        created = QPushButton("Drop Table")
        self.Body.addWidget(created,1,3)

        created = QPushButton("Search")
        self.Body.addWidget(created,2,0)





        widget1 = QWidget()
        widget1.setLayout(self.Body)
        self.setMenuWidget(widget1)



app = QApplication(sys.argv)

window = Login()
with open("styles.css","r") as file:
    app.setStyleSheet(file.read())
window.show()

app.exec()