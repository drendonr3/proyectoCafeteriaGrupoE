import sqlite3
from sqlite3 import Error

class Db:
    nombre='db/cafeteriaBriocheDb.db'
    conexion=''
    def __init__(self):
        try:
            self.conexion = sqlite3.connect(self.nombre)
        except :
            print('Error al conectar BB..')

    def close_db(self):
        if self.conexion is not None:
            self.conexion.close()
    