import mysql.connector
from mysql.connector import Error
class Connect():
    #Function to connect to database
    def connection(usern, passw):
        connector = mysql.connector.connect(
        host="localhost",
        user = usern ,
        password = passw
        )
    #Function to return connection   
    def getConnection(usern, passw):
        connector = mysql.connector.connect(
        host="localhost",
        user = usern ,
        password = passw
        )
        return connector