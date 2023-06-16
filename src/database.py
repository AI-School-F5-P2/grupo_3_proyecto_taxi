import mysql.connector
import hashlib
import os
import asyncio

class Database:
    #CONEXION A BASE DE DATOS
    def __init__(self):   
        try:
            self.conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="taxi_database"
            )
            
        except mysql.connector.Error as error:
            print("Error al conectar a la base de datos:", error)
           
    
    # EXTRAER HISTORIAL COMPLETO 
    def all(self):
        # conexion = self.conexion()
        cursor = self.conexion.cursor()
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
        tarifa =  data["tarifa"]
        fecha =  data["fecha"]
        cursor = self.conexion.cursor()
        query = "INSERT INTO `historial-carreras` (tarifa, fecha) VALUES (%s, %s)"
        values = (tarifa, fecha)
        cursor.execute(query, values)
        self.conexion.commit()


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

        cursor = self.conexion.cursor()
        cursor.execute(f"INSERT INTO DATA (password) VALUE ('{hash_hex}')")
        self.conexion.commit()
        
        # fila = cursor.fetchall()
        # print(fila)
        return hash_hex

    def password_get(self):
        cursor = self.conexion.cursor()
        cursor.execute(f"SELECT * FROM DATA ")
        fila = cursor.fetchall()
        return fila[0][0]
    
     #guardar en un archivo .txt
    def guardarEnHistorial(self):
        carpeta = "historial"
        archivo = "historial.txt"

        # Comprobar si la carpeta existe, si no, crearla
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Ruta completa del archivo
        ruta_archivo = os.path.join(carpeta, archivo)

        # Abrir archivo de texto para escritura
        archivo_txt = open(ruta_archivo, "w")   
                    
        db = Database()
        historial = db.all()
        # archivo_txt = open("datos.txt", "w")
        for data in historial:
            texto = f"ID: {data['id']} TARIFA: {data['tarifa']} FECHA: {data['fecha']} \n"
            archivo_txt.write(texto)
        archivo_txt.close()
    

