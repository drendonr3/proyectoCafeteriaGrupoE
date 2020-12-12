import sqlite3
from sqlite3 import Error

class Db:
    nombre=''
    conexion=''
    def __init__(self, nombre):
        self.nombre=nombre

    def get_db(self,nombre):
        try:
            self.conexion=sqlite3.connect(nombre)
            return self.conexion
        except :
            print('Error al conectar BB..')

    def close_db(self):
        if self.conexion is not None:
            self.conexion.close()
    