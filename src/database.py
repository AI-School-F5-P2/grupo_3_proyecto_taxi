from flask import Flask, request, jsonify
import mysql.connector
import hashlib

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
                "tarifa":element[1],
                "fecha":element[2]
            }
            historial.append(data)
        
        print(historial)
        return historial
    
    # INSERTAR
    def insertar(self, data):
        tarifa = data["tarifa"]
        fecha = data["fecha"]
        conexion = self.conector()
        cursor = conexion.cursor()
        cursor.execute(f"INSERT INTO `historial-carreras` (tarifa, fecha) VALUES ('{tarifa}','{fecha}')")
        conexion.commit()
        
    def password_hash(self, password):
        hash_object = hashlib.sha256()
        contraseña_bytes = password.encode('utf-8')
        hash_object.update(contraseña_bytes)
        hash_hex = hash_object.hexdigest()
        # Retornar el hash
        return hash_hex

    def password_insert(self):
        password = "1234"
        hash_object = hashlib.sha256()
        contraseña_bytes = password.encode('utf-8')
        hash_object.update(contraseña_bytes)
        hash_hex = hash_object.hexdigest()
        # Retornar el hash
        conexion = self.conector()
        cursor = conexion.cursor()
        cursor.execute(f"INSERT INTO DATA (password) VALUE ('{hash_hex}')")
        conexion.commit()
        
        # fila = cursor.fetchall()
        # print(fila)
        return hash_hex

    def password_get(self):
        conexion = self.conector()
        cursor = conexion.cursor()
        cursor.execute(f"SELECT * FROM DATA ")
        fila = cursor.fetchall()
        return fila[0][0]


