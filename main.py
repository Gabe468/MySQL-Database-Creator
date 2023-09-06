import sys
import mysql.connector
from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableView, QDialog, QApplication, QMainWindow, QPushButton,QVBoxLayout,QHBoxLayout, QGridLayout, QLabel, QWidget, QLineEdit, QFrame
from root import Error, Connect


class Login(QMainWindow):


    def __init__(self):
        super().__init__()
        self.setWindowTitle("MDC")

        #layout
        self.layout = QGridLayout( )
        labell = QLabel("MYSQL Database Creator")
        self.layout.addWidget(labell, 0, 0)

        #Username text and box
        self.labelu = QLabel("Username:")
        self.layout.addWidget(self.labelu, 1, 0)
        self.usern = QLineEdit()
        self.usern.setFixedWidth(100)
        self.layout.addWidget(self.usern, 1, 1)

        #Password text and box
        self.labelp = QLabel("Password:")
        self.layout.addWidget(self.labelp,2,0)
        self.passw = QLineEdit()
        self.passw.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addWidget(self.passw, 2, 1)
        self.passw.setFixedWidth(100)

        #Submit Button
        self.buttons = QPushButton("Submit")
        self.buttons.clicked.connect(self.submit)
        self.layout.addWidget(self.buttons, 3, 1)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setMenuWidget(widget)

        #Window params
        self.setFixedHeight(130)
        self.setFixedWidth(300)



    def submit(self):
        try:
            Login.usern = self.usern.text()
            Login.passw = self.passw.text()
            Connect.connection(Login.usern, Login.passw)
            self.close()
            SelectDatabase.openWindow(self)


        except Error as e:
            labele = QLabel(str(e))
            labele.setStyleSheet("color: red;")
            self.layout.addWidget(labele, 3, 0)
            self.setFixedHeight(150)


    
class   SelectDatabase(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(600, 600)
        self.setFixedHeight(500)
        self.setFixedWidth(300)
        self.setWindowTitle("MDC")

        self.Body = QGridLayout()
        self.labelp = QLabel("Hello "+ (Login.usern).upper())
        self.Body.addWidget(self.labelp, 0, 0)

        self.created = QPushButton("Create Database")
        self.Body.addWidget(self.created, 1, 0)
        self.created.clicked.connect(self.cDatabase)

        self.deleted = QPushButton("Delete Database")
        self.Body.addWidget(self.deleted, 1, 1)
        self.deleted.clicked.connect(self.dDatabase)

        self.selected = QLabel("Select Database:")
        self.Body.addWidget(self.selected, 2, 0)

        self.dSelection = QVBoxLayout()
        SelectDatabase.listDatabase(self)


        self.setLayout(self.Body)

    def openWindow(self):
        self.win = SelectDatabase()
        self.win.show()

    def listDatabase(self):
        mydb = Connect.getConnection(Login.usern, Login.passw)
        myc = mydb.cursor()
        databases = ("SHOW SCHEMAS")
        myc.execute(databases)
        x = 3
        for databases in myc:
            databases = str(databases).strip("',()")
            self.databases = QPushButton(str(databases))
            text = self.databases.text()
            self.databases.clicked.connect(lambda c, text=text : SelectTable.getDatabase(text))
            self.databases.clicked.connect(self.showTables)
            self.Body.addWidget(self.databases, x, 0)
            x+=1
            self.databases.setStyleSheet("QPushButton { background-color: white; color: black; border-radius: 0px; border-width: 0px;}"
                                        "QPushButton:hover { background-color: #818181 }")
    def cDatabase(self):
        self.close()
        self.w = CreateDatabase()
        self.w.show()

    def dDatabase(self):
        self.close()
        self.w = DeleteDatabase()
        self.w.show()

    def showTables(self):
        self.close()
        self.w = SelectTable()
        self.w.show()

class CreateDatabase(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create Database")
        self.layout = QGridLayout()
        self.enterl = QLabel("Enter Database Name To Create")
        

        self.entert = QLineEdit()
        self.entert.setFixedWidth(150)

        self.enterb = QPushButton("Enter")
        self.enterb.clicked.connect(self.databaseCreate)

        self.layout.addWidget(self.enterl, 0, 0)
        self.layout.addWidget(self.entert, 1, 0)
        self.layout.addWidget(self.enterb, 3, 0)
        self.setLayout(self.layout)

        self.enterl.setFixedWidth(150)
        self.setFixedHeight(105)
        self.setFixedWidth(200)

        
    def databaseCreate(self):
        try:
                mydb = Connect.getConnection(Login.usern, Login.usern)
                myc = mydb.cursor()

                myc.execute("CREATE DATABASE " + self.entert.text())
                self.close()
                SelectDatabase.openWindow(self)
        except Error as err:
            labele = QLabel(str(err))
            labele.setStyleSheet("color: red;")
            self.layout.addWidget(labele, 2, 0)
            self.setFixedHeight(130)


class DeleteDatabase(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Delete Database")
        self.layout = QGridLayout()
        self.enterl = QLabel("Enter Database Name")
        

        self.entert = QLineEdit()
        self.entert.setFixedWidth(150)

        self.enterb = QPushButton("Enter")
        self.enterb.clicked.connect(self.databaseDelete)

        self.layout.addWidget(self.enterl, 0, 0)
        self.layout.addWidget(self.entert, 1, 0)
        self.layout.addWidget(self.enterb, 3, 0)
        self.setLayout(self.layout)

        self.enterl.setFixedWidth(150)
        self.setFixedHeight(105)
        self.setFixedWidth(200)

    def databaseDelete(self):
        try:
                mydb = Connect.getConnection(Login.usern, Login.usern)
                myc = mydb.cursor()

                myc.execute("DROP DATABASE " + self.entert.text())
                self.close()
                SelectDatabase.openWindow(self)
        except Error as err:
            labele = QLabel(str(err))
            labele.setStyleSheet("color: red;")
            self.layout.addWidget(labele, 2, 0)
            self.setFixedHeight(130)

class SelectTable(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(600, 600)
        self.setFixedHeight(500)
        self.setFixedWidth(300)
        self.setWindowTitle("MDC")

        self.Body = QGridLayout()
        self.labelp = QLabel("Hello "+ (Login.usern).upper())
        self.Body.addWidget(self.labelp, 0, 0)

        self.createt = QPushButton("Create Table")
        self.Body.addWidget(self.createt, 1, 0)
        self.createt.clicked.connect(self.cTable)

        self.deletet = QPushButton("Delete Table")
        self.Body.addWidget(self.deletet, 1, 1)
        self.deletet.clicked.connect(self.dTable)

        self.selected = QLabel("Select Table:")
        self.Body.addWidget(self.selected, 2, 0)

        self.dSelection = QVBoxLayout()
        self.setLayout(self.Body)
        SelectTable.listTable(self)
    
    def getDatabase(text):
        SelectTable.getDatabase.text = text

    def listTable(self):
        mydb = Connect.getConnection(Login.usern, Login.passw)
        myc = mydb.cursor()
        myc.execute("USE "+ SelectTable.getDatabase.text)
        myc.execute("SHOW TABLES")
        x=3
        for tables in myc:
            tables = str(tables).strip("',()")
            self.tables = QPushButton(tables)
            text = self.tables.text()
            self.tables.clicked.connect(lambda c, text=text : ViewTable.getTable(text))
            self.tables.clicked.connect(self.showData)
            self.Body.addWidget(self.tables, x, 0)
            x+=1
            self.tables.setStyleSheet("QPushButton { background-color: white; color: black; border-radius: 0px; border-width: 0px;}"
                                        "QPushButton:hover { background-color: #818181 }")
    
    def showData(self):
        self.close()
        self.w = ViewTable()
        self.w.show()
    
    def cTable(self):
        self.close()
        self.w = CreateTable()
        self.w.show()

    def dTable(self):
        self.close()
        self.w = DropTable()
        self.w.show()
    

class CreateTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Table")
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

class DropTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drop Table")
        layout = QGridLayout()
        self.enterl = QLabel(" Enter Table Name")
        

        self.entert = QLineEdit()
        self.entert.setFixedWidth(130)

        self.enterb = QPushButton("Enter")
        self.enterb.clicked.connect(self.tableDrop)

        layout.addWidget(self.enterl)
        layout.addWidget(self.entert)
        layout.addWidget(self.enterb)
        self.setLayout(layout)

        self.enterl.setFixedWidth(130)
        self.setFixedHeight(105)
        self.setFixedWidth(200)

    def tableDrop(self):
        try:
            mydb = Connect.getConnection(Login.usern, Login.passw)
            myc = mydb.cursor()

            myc.execute("DROP TABLE " + self.entert.text())
            self.close()
            SelectDatabase.openWindow(self)
        except Error as err:
            labele = QLabel(str(err))
            labele.setStyleSheet("color: red;")
            self.layout.addWidget(labele, 2, 0)
            self.setFixedHeight(130)

class ViewTable(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(600, 600)
        self.setFixedHeight(500)
        self.setFixedWidth(300)
        self.setWindowTitle(ViewTable.getTable.text + " Table View")

        self.Body = QGridLayout()
        self.labelp = QLabel("Hello "+ (Login.usern).upper())
        self.Body.addWidget(self.labelp, 0, 0)

        self.dSelection = QVBoxLayout()
        self.setLayout(self.Body)
        ViewTable.listData(self)
    

        self.table = QTableView()
        data = [list(i) for i in ViewTable.listData.query]
        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.Body.addWidget(self.table, 1, 0)

    def getTable(text):
        ViewTable.getTable.text = text

    def listData(self):
        mydb = Connect.getConnection(Login.usern, Login.passw)
        myc = mydb.cursor()
        myc.execute("USE "+ SelectTable.getDatabase.text)
        myc.execute("SELECT * FROM " + ViewTable.getTable.text)
        ViewTable.listData.tables = len(myc.description)
        ViewTable.listData.col_names = [i[0] for i in myc.description]
        ViewTable.listData.query = myc.fetchall()

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(ViewTable.listData.col_names)
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ViewTable.listData.col_names[section]
        return super().headerData(section, orientation, role)


app = QApplication(sys.argv)

window = Login()
with open("styles.css","r") as file:
    app.setStyleSheet(file.read())
window.show()

app.exec()