from database import Database
import os

class Historial:

    def all(self): 
        carpeta = "../historial"
        archivo = "historial.txt"
        
        if not os.path.exists(carpeta):
            os.makedirs(carpeta) 
            ruta_archivo = os.path.join(carpeta, archivo)
        
        db = Database()
        historial = db.all()
        
        archivo_txt = open(ruta_archivo, "w")
        for data in historial:
            texto = f"ID: {data['id']} TARIFA: {data['tarifa']} FECHA: {data['fecha']} \n"
            archivo_txt.write(texto)
        
        archivo_txt.close()
        
        
historial = Historial()
guardar = historial.all()
     
     
  