import sys
import mysql.connector
from PyQt6 import QtCore, QtGui
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
            #Connection to SQL Database
            Login.usern = self.usern.text()
            Login.passw = self.passw.text()
            Connect.connection(Login.usern, Login.passw)
            self.close()
            SelectDatabase.openWindow(self)


        except Error as e:
            #Error codes
            labele = QLabel(str(e))
            labele.setStyleSheet("color: red;")
            self.layout.addWidget(labele, 3, 0)
            self.setFixedHeight(150)
    
class   SelectDatabase(QWidget):
    def __init__(self):
        super().__init__()

        #Window params
        self.resize(600, 600)
        self.setFixedHeight(600)
        self.setFixedWidth(400)
        self.setWindowTitle("MDC")

        #Layouts
        self.body = QGridLayout()
        self.header = QGridLayout()
        
        #Header
        self.labelp = QLabel("Signed In As: "+ (Login.usern).upper())
        self.backb = QPushButton()
        self.backb.setIcon(QtGui.QIcon('340.png'))
        self.backb.clicked.connect(self.back)
        self.backb.setFixedWidth(40)

        self.header.addWidget(self.backb, 0, 0)
        self.header.addWidget(self.labelp, 0, 2, alignment=Qt.AlignmentFlag.AlignRight)
        
        #Buttons for Create/Delete databases
        self.created = QPushButton("Create Database")
        self.body.addWidget(self.created, 1, 0)
        self.created.clicked.connect(self.cDatabase)

        self.deleted = QPushButton("Delete Database")
        self.body.addWidget(self.deleted, 1, 1)
        self.deleted.clicked.connect(self.dDatabase)

        self.selected = QLabel("Select Database:")
        self.body.addWidget(self.selected, 2, 0)

        #Function for Showing Databases
        SelectDatabase.listDatabase(self)

        #Layout finisher
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.header)
        self.layout.addLayout(self.body)
        self.setLayout(self.layout)

        #Open database selection
    def openWindow(self):
        self.win = SelectDatabase()
        self.win.show()

        #Function to list all databases
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
            self.body.addWidget(self.databases, x, 0)
            x+=1
            self.databases.setStyleSheet("QPushButton { background-color: white; color: black; border-radius: 0px; border-width: 0px;}"
                                        "QPushButton:hover { background-color: #818181 }")

        #Function to open database creation window
    def cDatabase(self):
        self.close()
        self.w = CreateDatabase()
        self.w.show()

        #Function to open database delete window
    def dDatabase(self):
        self.close()
        self.w = DeleteDatabase()
        self.w.show()

        #Function to open table selector
    def showTables(self):
        self.close()
        self.w = SelectTable()
        self.w.show()

        #Function to return to previous window
    def back(self):
        self.close()
        self.w = Login()
        self.w.show()

class CreateDatabase(QDialog):
    def __init__(self):
        super().__init__()

        #Layouts
        self.setWindowTitle("Create Database")
        self.layout = QVBoxLayout()
        self.body = QGridLayout()
        self.header = QHBoxLayout()
        
        #Back button
        self.backb = QPushButton()
        self.backb.setIcon(QtGui.QIcon('340.png'))
        self.backb.clicked.connect(self.back)
        self.backb.setFixedWidth(40)
        self.header.addWidget(self.backb, alignment=Qt.AlignmentFlag.AlignLeft)
        
        #Body of window
        self.enterl = QLabel("Enter Database Name To Create")
        self.entert = QLineEdit()
        self.entert.setFixedWidth(150)
        self.enterb = QPushButton("Enter")
        self.enterb.clicked.connect(self.databaseCreate)

        self.body.addWidget(self.enterl, 0, 0)
        self.body.addWidget(self.entert, 1, 0)
        self.body.addWidget(self.enterb, 3, 0)

        #Layout finisher
        self.layout.addLayout(self.header)
        self.layout.addLayout(self.body)
        self.setLayout(self.layout)

        #Window params
        self.enterl.setFixedWidth(150)
        self.setFixedHeight(140)
        self.setFixedWidth(200)

        #Function to create Database
    def databaseCreate(self):
        try:
            #Connection to database and execution
            mydb = Connect.getConnection(Login.usern, Login.usern)
            myc = mydb.cursor()
            myc.execute("CREATE DATABASE " + self.entert.text())
            self.close()
            SelectDatabase.openWindow(self)
        except Error as err:
            #Error codes
            labele = QLabel(str(err))
            labele.setStyleSheet("color: red;")
            self.body.addWidget(labele, 2, 0)
            self.setFixedHeight(130)

        #Function to go to previous window
    def back(self):
        self.close()
        self.w = SelectDatabase()
        self.w.show()

class DeleteDatabase(QDialog):
    def __init__(self):
        super().__init__()

        #Layouts for window
        self.setWindowTitle("Delete Database")
        self.layout = QVBoxLayout()
        self.body = QGridLayout()
        self.header = QHBoxLayout()

        #Back button
        self.backb = QPushButton()
        self.backb.setIcon(QtGui.QIcon('340.png'))
        self.backb.clicked.connect(self.back)
        self.backb.setFixedWidth(40)
        self.header.addWidget(self.backb, alignment=Qt.AlignmentFlag.AlignLeft)
        
        #Body of window
        self.enterl = QLabel("Enter Database Name")
        self.entert = QLineEdit()
        self.entert.setFixedWidth(150)
        self.enterb = QPushButton("Enter")
        self.enterb.clicked.connect(self.databaseDelete)
        
        self.body.addWidget(self.enterl, 0, 0)
        self.body.addWidget(self.entert, 1, 0)
        self.body.addWidget(self.enterb, 3, 0)

        #Layout finisher
        self.layout.addLayout(self.header)
        self.layout.addLayout(self.body)
        self.setLayout(self.layout)

        #Window params
        self.enterl.setFixedWidth(150)
        self.setFixedHeight(140)
        self.setFixedWidth(200)

        #Function to delete database
    def databaseDelete(self):
        try:
            #Connection to database and execution
            mydb = Connect.getConnection(Login.usern, Login.usern)
            myc = mydb.cursor()
            myc.execute("DROP DATABASE " + self.entert.text())
            self.close()
            SelectDatabase.openWindow(self)
        except Error as err:
            #Error codes
            labele = QLabel(str(err))
            labele.setStyleSheet("color: red;")
            self.body.addWidget(labele, 2, 0)
            self.setFixedHeight(130)

        #Function to return to previous window
    def back(self):
        self.close()
        self.w = SelectDatabase()
        self.w.show()

class SelectTable(QWidget):
    def __init__(self):
        super().__init__()

        #Window Params
        self.resize(600, 600)
        self.setFixedHeight(600)
        self.setFixedWidth(400)
        self.setWindowTitle("MDC")
        
        #Layouts
        self.body = QGridLayout()
        self.header = QGridLayout()
        
        #Header
        self.labelp = QLabel("Signed In As: "+ (Login.usern).upper())
        self.backb = QPushButton()
        self.backb.setIcon(QtGui.QIcon('340.png'))
        self.backb.clicked.connect(self.back)
        self.backb.setFixedWidth(40)
        self.header.addWidget(self.backb, 0, 0)
        self.header.addWidget(self.labelp, 0, 1, alignment=Qt.AlignmentFlag.AlignRight)

        #Buttons for Delete/Create Tables
        self.createt = QPushButton("Create Table")
        self.body.addWidget(self.createt, 1, 0)
        self.createt.clicked.connect(self.cTable)

        self.deletet = QPushButton("Delete Table")
        self.body.addWidget(self.deletet, 1, 1)
        self.deletet.clicked.connect(self.dTable)

        self.selected = QLabel("Select Table:")
        self.body.addWidget(self.selected, 2, 0)

        #Table lister
        SelectTable.listTable(self)
        
        #Layout finisher
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.header)
        self.layout.addLayout(self.body)
        self.setLayout(self.layout)
        
        #Function to open table selector
    def openWindow(self):
        self.win = SelectTable()
        self.win.show()
        
        #Function to get database clicked
    def getDatabase(text):
        SelectTable.getDatabase.text = text

        #Function to list tables in database
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
            self.body.addWidget(self.tables, x, 0)
            x+=1
            self.tables.setStyleSheet("QPushButton { background-color: white; color: black; border-radius: 0px; border-width: 0px;}"
                                        "QPushButton:hover { background-color: #818181 }")

        #Function to view window with data
    def showData(self):
        self.close()
        self.w = ViewTable()
        self.w.show()
        
        #Function to create table
    def cTable(self):
        self.close()
        self.w = CreateTable()
        self.w.show()

        #Function to delete table
    def dTable(self):
        self.close()
        self.w = DropTable()
        self.w.show()

        #Function to return to previous window
    def back(self):
        self.close()
        self.w = SelectDatabase()
        self.w.show()
    
class CreateTable(QWidget):
    def __init__(self):
        super().__init__()
        
        #Layout
        self.layout = QVBoxLayout()
        self.buttons = QHBoxLayout()
        self.header = QHBoxLayout()
        
        #Body of window
        self.enterl = QLabel(" Enter Table Name")
        self.entert = QLineEdit()
        self.enterb = QPushButton("Enter")
        self.enterb.clicked.connect(self.update)
        
        #Back button
        self.backb = QPushButton()
        self.backb.setIcon(QtGui.QIcon('340.png'))
        self.backb.clicked.connect(self.back)
        self.backb.setFixedWidth(40)
        
        #Buttons for data types
        self.pkb = QPushButton("PK")
        self.varb = QPushButton("VarChar")
        self.dateb = QPushButton("Date")
        self.intb = QPushButton("Int")
        
        #Adding buttons to layout
        self.header.addWidget(self.backb, alignment=Qt.AlignmentFlag.AlignRight)
        self.layout.addLayout(self.header)
        self.layout.addWidget(self.enterl, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.entert)
        self.buttons.addWidget(self.pkb)
        self.buttons.addWidget(self.varb)
        self.buttons.addWidget(self.dateb)
        self.buttons.addWidget(self.intb)
        
        self.pkb.clicked.connect(self.pkbTable)
        self.dateb.clicked.connect(self.dateTable)
        self.varb.clicked.connect(self.varTable)
        self.intb.clicked.connect(self.intTable)
        self.enterb.clicked.connect(self.cTable)
        self.varLayout = QGridLayout()
        
        #Layout finisher
        self.layout.addLayout(self.buttons)
        self.layout.addLayout(self.varLayout)
        self.layout.addWidget(self.enterb)
        self.setLayout(self.layout)

        #Window params
        CreateTable.height = 200
        self.setFixedHeight(CreateTable.height)
        self.setFixedWidth(300)
        
        #List of datatypes for creation
        CreateTable.text = []

        #Function to create table information
    def cTable(self):
        
        #Append data types if they were selected
        try:
            CreateTable.text.append(self.varText.text()+ " VARCHAR(255)")
        except:
            pass
        
        try:
            CreateTable.text.append(self.dateText.text()+ " DATE")
        except:
            pass
        
        try:
            CreateTable.text.append(self.intText.text() + " int")
        except:
            pass
        
        #Table name and data type selector
        try:
            #Connection to database and execution
            mydb = Connect.getConnection(Login.usern, Login.usern)
            myc = mydb.cursor()
            print("CREATE TABLE " + SelectTable.getDatabase.text + "."+ self.entert.text() + " (" + ', '.join([str(var) for var in CreateTable.text]) + ")")
            myc.execute("CREATE TABLE " + SelectTable.getDatabase.text + "."+ self.entert.text() + " (" + ', '.join([str(var) for var in CreateTable.text]) + ")")
            self.close()
            SelectDatabase.openWindow(self)
        except Error as err:
            #Error codes
            labele = QLabel(str(err))
            labele.setStyleSheet("color: red;")
            self.layout.addWidget(labele)
            CreateTable.height += 50
            self.setFixedHeight(CreateTable.height)
        
        #Function to add primary keys
    def pkbTable(self):
        self.pkbLabel = QLabel("PKB")
        self.varLayout.addWidget(self.pkbLabel)
        CreateTable.height += 50
        self.setFixedHeight(CreateTable.height)
        CreateTable.text.append("id INT AUTO_INCREMENT PRIMARY KEY")
        self.update()

        #Function to add varchars
    def varTable(self):
        self.varLabel = QLabel("VARCHAR")
        self.varText = QLineEdit()
        self.varLayout.addWidget(self.varLabel)
        self.varLayout.addWidget(self.varText)
        CreateTable.height += 50
        self.setFixedHeight(CreateTable.height)
        self.update()
        
        #Function to add dates
    def dateTable(self):
        self.dateLabel = QLabel("DATE")
        self.dateText = QLineEdit()
        self.varLayout.addWidget(self.dateLabel)
        self.varLayout.addWidget(self.dateText)
        CreateTable.height += 50
        self.setFixedHeight(CreateTable.height)
        self.update()
        
        #Function to add ints
    def intTable(self):
        self.intLabel = QLabel("INT")
        self.intText = QLineEdit()
        self.varLayout.addWidget(self.intLabel)
        self.varLayout.addWidget(self.intText)
        CreateTable.height += 50
        self.setFixedHeight(CreateTable.height)
        self.update()
        
        #Function to return to previous window
    def back(self):
        self.close()
        self.w = SelectTable()
        self.w.show()

class DropTable(QWidget):
    def __init__(self):
        super().__init__()
        
        #Layouts
        self.setWindowTitle("Drop Table")
        self.layout = QVBoxLayout()
        self.body = QGridLayout()
        self.header = QHBoxLayout()
        
        #Back button
        self.backb = QPushButton()
        self.backb.setIcon(QtGui.QIcon('340.png'))
        self.backb.clicked.connect(self.back)
        self.backb.setFixedWidth(40)
        self.header.addWidget(self.backb, alignment=Qt.AlignmentFlag.AlignLeft)

        #Body of window
        self.enterl = QLabel(" Enter Table Name")
        self.entert = QLineEdit()
        self.entert.setFixedWidth(130)
        self.enterb = QPushButton("Enter")
        self.enterb.clicked.connect(self.tableDrop)

        self.body.addWidget(self.enterl, 0, 0)
        self.body.addWidget(self.entert, 1, 0)
        self.body.addWidget(self.enterb, 3, 0)

        #Layout finisher
        self.layout.addLayout(self.header)
        self.layout.addLayout(self.body)
        self.setLayout(self.layout)

        #Window params
        self.enterl.setFixedWidth(130)
        self.setFixedHeight(140)
        self.setFixedWidth(200)

        #Function to Drop table
    def tableDrop(self):
        try:
            #Connection to database and execution
            mydb = Connect.getConnection(Login.usern, Login.passw)
            myc = mydb.cursor()
            myc.execute("DROP TABLE " + SelectTable.getDatabase.text + "." + self.entert.text())
            self.close()
            SelectTable.openWindow(self)
        except Error as err:
            #Error codes
            labele = QLabel(str(err))
            labele.setStyleSheet("color: red;")
            self.body.addWidget(labele, 2, 0)
            self.setFixedHeight(130)
        
        #Function to return to previous window
    def back(self):
        self.close()
        self.w = SelectTable()
        self.w.show()

class ViewTable(QWidget):
    def __init__(self):
        super().__init__()

        #Window params
        self.resize(600, 600)
        self.setFixedHeight(600)
        self.setFixedWidth(700)
        self.setWindowTitle(ViewTable.getTable.text + " Table View")

        #Layouts
        self.layout = QVBoxLayout()
        self.body = QGridLayout()
        self.header = QGridLayout()
        
        #Header
        self.labelp = QLabel("Signed In As: "+ (Login.usern).upper())
        self.backb = QPushButton()
        self.backb.setIcon(QtGui.QIcon('340.png'))
        self.backb.clicked.connect(self.back)
        self.backb.setFixedWidth(40)
        self.header.addWidget(self.backb, 0, 0)
        self.header.addWidget(self.labelp, 0, 1, alignment=Qt.AlignmentFlag.AlignRight)

        #Layout finisher
        self.layout.addLayout(self.header)
        self.layout.addLayout(self.body)
        self.setLayout(self.layout)
        
        #Table viewer
        ViewTable.listData(self)

        #Data for row and columns and Table Model
        self.table = QTableView()
        data = [list(i) for i in ViewTable.listData.query]
        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.body.addWidget(self.table, 1, 0)

        #Function to get text of table clicked
    def getTable(text):
        ViewTable.getTable.text = text
        
        #Function to add table data
    def listData(self):
        #Connection to database and execution
        mydb = Connect.getConnection(Login.usern, Login.passw)
        myc = mydb.cursor()
        myc.execute("USE "+ SelectTable.getDatabase.text)
        myc.execute("SELECT * FROM " + ViewTable.getTable.text)
        ViewTable.listData.tables = len(myc.description)
        ViewTable.listData.col_names = [i[0] for i in myc.description]
        ViewTable.listData.query = myc.fetchall()

        #Function to return to previous window
    def back(self):
        self.close()
        self.w = SelectTable()
        self.w.show()

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
    def data(self, index, role):
        #Data for rows and columns
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        #Count for rows
        return len(self._data)

    def columnCount(self, index):
        #Count for columns
        return len(ViewTable.listData.col_names)
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        #Header for columns
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ViewTable.listData.col_names[section]
        if role == QtCore.Qt.ItemDataRole.BackgroundRole:
            return QtCore.QVariant(QtGui.QColor(255, 0, 0, 127))
        return super().headerData(section, orientation, role)

#Application starter
app = QApplication(sys.argv)
window = Login()

#Stylesheet for application
with open("styles.css","r") as file:
    app.setStyleSheet(file.read())
window.show()

#Application execution
app.exec()