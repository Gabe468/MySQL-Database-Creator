import mysql.connector
from mysql.connector import Error
class Connect():
    def connection(usern, passw):
        connector = mysql.connector.connect(
        host="localhost",
        user = usern ,
        password = passw
        )