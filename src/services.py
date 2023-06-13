from flask import Flask, request, jsonify
import mysql.connector


app = Flask(__name__)

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="taxi_database"
)

cursor = conexion.cursor()


#historial
@app.route("/historial")
def getAllData():
    # Ejecutar consultas o comandos SQL
    cursor.execute("SELECT * FROM  `historial-carreras`")
    filas = cursor.fetchall()
    
    # Recorrer los resultados

    historial = []
    for fila in filas:
        data = {
            "tarifa":fila[0],
            "fecha":fila[1],
        }
        historial.append(data)
    return jsonify(historial)





@app.route("/agregar", methods=["POST"])
def agregar():
    tarifa = request.form.get('tarifa')
    fecha = request.form.get('fecha')
    sql = f"INSERT INTO `historial-carreras` (tarifa, fecha) VALUES ('{tarifa}','{fecha}')"
    cursor.execute(sql)
    conexion.commit()
    return jsonify({'message':'tarifa agregada a la base de datos'})








if __name__ == '__main__':
    app.run(debug=True, port=4000)
    