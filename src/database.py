import mysql.connector
import os

class Database:
    #CONEXION A BASE DE DATOS
    def conector(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="taxi_database"
        )
        return self.conexion
    
    
    # EXTRAER HISTORIAL COMPLETO 
    def all(self):
        conexion = self.conector()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM  `historial-carreras`")
        fila = cursor.fetchall()
        
        historial = []
        for element in fila:
            data = {
                "id":element[0],
                "tarifa":element[1],
                "fecha":element[2]
            }
            historial.append(data)
        return historial
    
    # INSERTAR
    def insertar(self, data):
        tarifa = data["tarifa"]
        fecha = data["fecha"]
        conexion = self.conector()
        cursor = conexion.cursor()
        cursor.execute(f"INSERT INTO `historial-carreras` (tarifa, fecha) VALUES ('{tarifa}','{fecha}')")
        conexion.commit()
        
    