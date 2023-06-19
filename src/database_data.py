import hashlib
import mysql.connector

class Data:
    
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="taxi_database"
        
    )
    
    def precios(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT precio_mov, precio_det FROM data")
        fila = cursor.fetchall()
        precios = []
        for fila in fila:
            precio = {
                "precio1":fila[0],
                "precio2":fila[1]
            }
            precios.append(precio)
        return precios
        
    def editarPrecios(self, precio_det, precio_mov):
        cursor = self.conexion.cursor()
        cursor.execute(f"UPDATE data SET precio_mov = {precio_mov} , precio_det = {precio_det}")
        self.conexion.commit()
        # self.conexion.close()
        # cursor.close()
        
        
        
    def password_hash(self, password):
        hash_object = hashlib.sha256()
        contraseña_bytes = password.encode('utf-8')
        hash_object.update(contraseña_bytes)
        hash_hex = hash_object.hexdigest()
        # Retornar el hash
        return hash_hex

    def password_insert(self,password):
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
  
  
  
  
  
  
##cambiar clave
# usuario = Data()
# nueva_clave = "1234"
# usuario.password_insert(nueva_clave)

##cambiar precios
# usuario = Data()
# precio_det = 0.02
# precio_mov = 0.05
# usuario.editarPrecios(precio_det, precio_mov)