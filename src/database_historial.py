import mysql.connector
import hashlib
import os
import asyncio

class Database_historial:
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
        self.guardarEnTextoPlano(historial)
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


   
    
     #guardar en un archivo .txt
    def guardarEnTextoPlano(self,historial):
        carpeta = "../historial"
        archivo = "historial.txt"

        # Comprobar si la carpeta existe, si no, crearla
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Ruta completa del archivo
        ruta_archivo = os.path.join(carpeta, archivo)

        # Abrir archivo de texto para escritura
        archivo_txt = open(ruta_archivo, "w")   
                    
        # db = Database()
        # historial = db.all()
        # archivo_txt = open("datos.txt", "w")
        for data in historial:
            texto = f"ID: {data['id']} TARIFA: {data['tarifa']} FECHA: {data['fecha']} \n"
            archivo_txt.write(texto)
        archivo_txt.close()
    



    
# #crear contraseña
# pas = Database()
# pas.password_insert()



 
