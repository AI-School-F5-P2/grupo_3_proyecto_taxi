from flask import Flask
import time
from datetime import datetime
import tkinter as tk
from PIL import ImageTk, Image
from logs import logs
from database_historial import Database_historial
import os
import threading
from database_data import Data

class Taximetro:
    def __init__(self):
        self.taximetroActivo = False
        self.cocheEnMovimiento = False
        self.tiempoInicio = 0
        self.tiempoTrancurrido = 0
        self.tarifaTotal = 0
        self.tarifa = 0
        self.yaSeAfrenado = False
        self.precio1 = 0
        self.precio2 = 0



    def iniciar(self):
        data = Data()
        precios = data.precios()
        
        self.precio1 = precios[0]["precio1"] if precios else 0.02
        self.precio2 = precios[0]["precio2"] if precios else 0.05

        
        result_label_info.config(text="")
        if not self.taximetroActivo:
            if self.tarifaTotal > 0:
                self.tarifaTotal = 0
            result_label.config(text="Taximetro inicializado", font=("Arial", 12, "bold"), justify="center")
            self.taximetroActivo = True
            self.tiempoInicio = time.time()
        else:
            result_label.config(text="El taximetro ya se ha iniciado", font=("Arial", 12, "bold"), justify="center")

        



    def moverCoche(self):
        if self.taximetroActivo and not self.cocheEnMovimiento:
            if self.yaSeAfrenado:
                self.calcularTarifa("detenido")
<<<<<<< HEAD
                
            result_label_info.config(
            text=f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.",
            font=("Courier", 12, "bold"),
            justify="center",
            fg="red",
            bg="black",
            padx=10,
            pady=10
            )
=======

>>>>>>> 389e91294db6f056f7ffafe7ff173c357366414f
            self.cocheEnMovimiento = True
            self.tiempoInicio = time.time()
            result_label.config(text="Coche en movimiento", font=("Arial", 12, "bold"), justify="center")
        elif not self.taximetroActivo:
            result_label.config(text="Antes de poner en movimiento el coche, debes inicializar el taximetro", font=("Arial", 12, "bold"), justify="center")
        else:
            result_label.config(text="El Coche ya está en movimiento", font=("Arial", 12, "bold"), justify="center")



    def detenerCoche(self):
        if self.cocheEnMovimiento:
            self.cocheEnMovimiento = False
            self.yaSeAfrenado = True
            self.calcularTarifa("moviendose")
            result_label.config(text="El Coche se ha detenido", font=("Arial", 12, "bold"), justify="center")
            self.tiempoInicio = time.time()
        else:
            result_label.config(text="El coche ya está detenido", font=("Arial", 12, "bold"), justify="center")




    def finalizarRecorrido(self):
        if self.cocheEnMovimiento == False and self.taximetroActivo:
            result_label.config(text="Carrera terminada. Para iniciar otra carrera, haz clic en 'Iniciar Carrera'", font=("Arial", 12, "bold"), justify="center")
            self.calcularTarifa("detenido")
            self.agregarABaseDeDatos()
            result_label_info.config(text=f"Total a pagar: {self.tarifaTotal:.2f} Euros.", font=("Arial", 12, "bold"), justify="center")
            self.reiniciarValores()
        elif not self.taximetroActivo:
            result_label.config(text="No hay carrera en curso", font=("Arial", 12, "bold"), justify="center")
        else:
            result_label.config(text="Para finalizar el recorrido, primero debes detener el coche", font=("Arial", 12, "bold"), justify="center")




    def cambiarPrecios(self, precio_det, precio_mov):
        if not self.taximetroActivo:
            db = Data()
            db.editarPrecios(precio_det, precio_mov)
        else:
            print("Para cambiar los precios debes de terminar la carrera")
            
        

        
    def calcularTarifa(self, accion):
        monto = self.precio1 if accion == "detenido" else self.precio2
        self.tiempoTrancurrido = time.time() - self.tiempoInicio
        self.tarifa = self.tiempoTrancurrido * monto
        self.tarifaTotal += self.tarifa
        result_label_info.config(text=f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.", font=("Arial", 12, "bold"), justify="center")



    def mostrarHistorial(self):
        database = Database_historial()
        historial = database.all()
        return historial



    def agregarABaseDeDatos(self):
        fecha_actual = datetime.now()
        database = Database_historial()
        fecha_hora_actual_str = fecha_actual.strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "tarifa": str(self.tarifaTotal),
            "fecha": str(fecha_hora_actual_str)
        }
        database.insertar(data)



    def reiniciarValores(self):
        self.taximetroActivo = False
        self.cocheEnMovimiento = False
        self.tiempoInicio = 0
        self.tiempoTrancurrido = 0
        self.tarifaTotal = 0
        self.tarifa = 0
        self.yaSeAfrenado = False


    def finalizarWindows(self):
        window.destroy()


#################################################

def iniciarCarrera():
    contrasena_ingresada = entry_contrasena.get()
    usuario = Data()
    contraseña_bbdd = usuario.password_get()
    contaseña_hash = usuario.password_hash(contrasena_ingresada)
    logs()
    if contaseña_hash == contraseña_bbdd:
        label_contrasena.pack_forget()
        button_iniciar.pack_forget()
        entry_contrasena.pack_forget()
        message_widget.pack_forget()
        button_init.pack(pady=10, ipady=10, ipadx=100)
        button_mover.pack(pady=10, ipady=10, ipadx=100)
        button_detener.pack(pady=10, ipady=10, ipadx=100)
        button_finalizar.pack(pady=10, ipady=10, ipadx=90)
        button_close.pack()
        taximetro.iniciar()
    else:
        label_contrasena.config(text="Contraseña Incorrecta", font=("Arial", 12, "bold"), justify="center")
        label_contrasena.pack(pady=10, ipady=10, ipadx=100)

def moverCoche():
    taximetro.moverCoche()

def detenerCoche():
    taximetro.detenerCoche()

def finalizarRecorrido():
    taximetro.finalizarRecorrido()

taximetro = Taximetro()

window = tk.Tk()
window.title("Taxímetro")
window.geometry("720x480")

# create widgets
button_init = tk.Button(window, text="Iniciar Carrera", command=iniciarCarrera)
button_mover = tk.Button(window, text="Mover Coche", command=moverCoche)
button_detener = tk.Button(window, text="Detener Coche", command=detenerCoche)
button_finalizar = tk.Button(window, text="Finalizar Recorrido", command=finalizarRecorrido)
button_close = tk.Button(window, text="Cerrar", command=taximetro.finalizarWindows)

label_contrasena = tk.Label(window, text="Por favor, ingrese la contraseña:", font=("Arial", 12, "bold"), justify="center")
label_contrasena.pack(pady=10, ipady=10, ipadx=100)

entry_contrasena = tk.Entry(window, show="*")
entry_contrasena.pack(pady=10, ipady=10, ipadx=50)
entry_contrasena.configure(
    font=("Arial", 12),
    bg="white",
    fg="black",
    relief="solid",
    width=20,
    justify="center",
)

button_iniciar = tk.Button(window, text="Iniciar Carrera", command=iniciarCarrera)
button_iniciar.pack(padx=10, pady=10, ipady=10, ipadx=100)

imagen = Image.open("../assets/taxi.png")
imagen_tk = ImageTk.PhotoImage(imagen)
label = tk.Label(window, image=imagen_tk)
label.pack()

message_widget = tk.Message(window, text="\tBienvenido al Taxímetro:\n\nPara iniciar el taxi, presiona 'Iniciar '.\nPara mover el taxi, presiona 'Mover '.\nPara detener el taxi, presiona 'Detener '.\nPara finalizar el taxi, presiona 'Finalizar'.", width=400)
message_widget.configure(
    font=("Arial", 13),
    borderwidth=1,
)
message_widget.pack(pady=10)

result_label = tk.Label(window, text="")
result_label.pack()

result_label_info = tk.Label(window, text="")
result_label_info.pack()

result_label_count = tk.Label(window, text="")
result_label_count.pack()

window.mainloop()


