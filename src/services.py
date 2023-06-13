from flask import Flask, request, jsonify
import mysql.connector


app = Flask(__name__)

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="taxi_database"
)



@app.route("/historial")
def getHistorial():
    return


@app.route("/agregar", methods="POST")
def agregar():
    cursor = conexion.cursor()
    # data = request.json
    tarifa = request.form.get('tarifa')
    fecha = request.form.get('fecha')
    sql= "INSERT INTO `historial-carreras` (tarifa, fecha) VALUES ('%s', '%s')"
    valores = (tarifa, fecha)
    cursor.execute(sql,valores)
    conexion.commit()
    cursor.close()
    conexion.close()
    print(valores)
    return




if __name__== '__main__':
    app(debug=True)