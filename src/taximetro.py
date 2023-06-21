from flask import Flask
import time
from datetime import datetime
import tkinter as tk
from PIL import ImageTk, Image
from logs import Logs
from database_historial import Database_historial
import os
import threading
from database_data import Data
import tkinter.font as tkFont
import keyboard

class Taximetro:
    def __init__(self):
        self.taximetroActivo = False
        self.cocheEnMovimiento = False
        self.tarifaTotal = 0
        self.yaSeAfrenado = False
        self.precio_mov = 0
        self.precio_det = 0
        self.precioActual=0
        self.actualizar_precio = None
        self.logs = Logs()
       
        
    def aplicarPrecios(self):
        self.data = Data()
        self.precios = self.data.precios()
        self.precio_mov = self.precios[0]["precio_mov"] if self.precios else 0.05
        self.precio_det = self.precios[0]["precio_det"] if self.precios else 0.02
        self.precioActual = self.precio_det
        


    def iniciar(self):
        self.aplicarPrecios()
        self.data = Data()
        result_label_info.config(text="")
        if not self.taximetroActivo:
            self.logs.info("Se a iniciado el taximetro")
            if self.tarifaTotal > 0:
                self.tarifaTotal = 0
            result_label.config(text="Taximetro inicializado", font=("Arial", 12, "bold"), justify="center")
            self.taximetroActivo = True
            self.actualizar_precio = window.after(1000, self.actualizarPrecio)
        else:
            self.logs.warning("Se intento de iniciar el taxímetro cuando ya está activo")
            result_label.config(text="El taximetro ya se ha iniciado", font=("Arial", 12, "bold"), justify="center")


    def moverCoche(self):
        if self.taximetroActivo and not self.cocheEnMovimiento:
            self.logs.info("Se a empezado a mover el coche")
            self.precioActual = self.precio_mov
            self.cocheEnMovimiento = True
            result_label.config(text="Coche en movimiento", font=("Arial", 12, "bold"), justify="center")
            result_label_info.config(text=f"{self.tarifaTotal:.2f} EUROS.", font=custom_font, justify="center", bg="black", fg="white",  borderwidth=2, relief="solid", padx=5, pady=5)
        elif not self.taximetroActivo:
            self.logs.warning("Se intento poner en movimiento el coche antes de inicializar el taximetro")
            result_label.config(text="Antes de poner en movimiento el coche, debes inicializar el taximetro", font=("Arial", 12, "bold"), justify="center")
        else:
            self.logs.warning("Se intento poner en movimiento el coche ya estando en movimiento")
            result_label.config(text="El Coche ya está en movimiento", font=("Arial", 12, "bold"), justify="center")
            result_label_info.config(text=f"{self.tarifaTotal:.2f} EUROS.", font=custom_font, justify="center", bg="black", fg="white",  borderwidth=2, relief="solid", padx=5, pady=5)


    def detenerCoche(self):
        if self.cocheEnMovimiento:
            self.logs.info("El coche se detuvo")
            self.precioActual = self.precio_det
            self.cocheEnMovimiento = False
            self.yaSeAfrenado = True
            result_label.config(text="El Coche se ha detenido", font=("Arial", 12, "bold"), justify="center")
        else:
            self.logs.warning("se intento detener el coche cuando ya estaba detenido")
            result_label.config(text="El coche ya está detenido", font=("Arial", 12, "bold"), justify="center")




    def finalizarRecorrido(self):
        if self.cocheEnMovimiento == False and self.taximetroActivo:
            self.logs.info(f"Se finalizo la carrera, con una tarifa total de {self.tarifaTotal:.2f}")
            result_label.config(text="Carrera terminada. Para iniciar otra carrera, haz clic en 'Iniciar Carrera'", font=("Arial", 12, "bold"), justify="center")
            self.detenerActualizacionPrecio()
            self.guardarRegistroTaximetro_BD()
            result_label_info.config(text=f"Total a pagar: {self.tarifaTotal:.2f} Euros.", font=("Arial", 12, "bold"), justify="center")
            self.reiniciarValores()
            modificarPrecio_BTN.pack(padx=10, pady=10, side="right")
        elif not self.taximetroActivo:
            self.logs.warning("Se intento finalizar una carrera sin haber inicializado el taximetro")
            result_label.config(text="No hay carrera en curso", font=("Arial", 12, "bold"), justify="center")
        else:
            self.logs.warning("Se intento finalizar una carrera sin primero haber detenido el coche")
            result_label.config(text="Para finalizar el recorrido, primero debes detener el coche", font=("Arial", 12, "bold"), justify="center")




    def actualizarPrecio(self):
        self.tarifaTotal += self.precioActual
        result_label_info.config(text=f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.", font=("Arial", 12, "bold"), justify="center")
        self.actualizar_precio = window.after(1000, self.actualizarPrecio)



    def detenerActualizacionPrecio(self):
        if self.actualizar_precio is not None:
            window.after_cancel(self.actualizar_precio)
            self.actualizar_precio = None



    def guardarRegistroTaximetro_BD(self):
        fecha_actual = datetime.now()
        database = Database_historial()
        fecha_hora_actual_str = fecha_actual.strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "tarifa": str(self.tarifaTotal),
            "fecha": str(fecha_hora_actual_str)
        }
        database.insertar(data)
        self.logs.info("Se ha guardado los registro del taximetro en la base de datos")




    def cambiarPreciosBD(self, precio_Det, precio_Mov):
        if not self.taximetroActivo:
            db = Data()
            precio_det = precio_Det.get()
            precio_mov = precio_Mov.get()
            db.editarPrecios(precio_det, precio_mov)
            self.logs.info("Se han cambiado los precios del taximetro")
        else:
            self.logs.warning("Se intento cambiar los precios del taximetro cuando habia una carrera en curso")
            print("Para cambiar los precios debes de terminar la carrera")
            
            
    def detenerActualizacionPrecio(self):
        if self.actualizar_precio is not None:
            window.after_cancel(self.actualizar_precio)
            self.actualizar_precio = None

    def actualizarPrecio(self):
        self.tarifaTotal += self.precioActual
        result_label_info.config(text=f"{self.tarifaTotal:.2f} EUROS.", font=custom_font, justify="center", bg="black", fg="white",  borderwidth=2, relief="solid", padx=5, pady=5)
        self.actualizar_precio = window.after(1000, self.actualizarPrecio)

        

    def mostrarHistorial(self):
        database = Database_historial()
        historial = database.all()
        self.logs.info("Se ha hecho una consulta del historial")
        return historial


    def reiniciarValores(self):
        self.taximetroActivo = False
        self.cocheEnMovimiento = False
        self.tarifaTotal = 0
        self.yaSeAfrenado = False
        self.precio_mov = 0
        self.precio_det = 0
        self.precioActual=0
        self.actualizar_precio = None


    def finalizarWindows(self):
        window.destroy()















#TKINTER
def iniciarCarrera():

    logs = Logs()
    usuario = Data()
    contrasena_ingresada = entry_contrasena.get()
    contraseña_bbdd = usuario.password_get()
    contaseña_hash = usuario.password_hash(contrasena_ingresada)
    
    if contaseña_hash == contraseña_bbdd:
        descargarHistorial_BTN.place(x=10, y=10)
        descargarHistorial_BTN.configure(fg="white", bg="#00618E")
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
        # modificarPrecio_BTN.pack(padx=10, pady=10, side="right")
    else:
        label_contrasena.config(text="Contraseña Incorrecta", font=("Arial", 12, "bold"), justify="center")
        label_contrasena.pack(pady=10, ipady=10, ipadx=100)
        logs.warning("Han intentado ingresar al taximetro con una contraseña incorrecta")

def moverCoche():
    if taximetro.taximetroActivo:
        taximetro.moverCoche()

def detenerCoche():
    if taximetro.taximetroActivo:
        taximetro.detenerCoche()

def finalizarRecorrido():
    if taximetro.taximetroActivo:
        taximetro.finalizarRecorrido()
    
def crearVentanaModificarPrecio():
    taximetro = Taximetro()
    
    logs = Logs()
    logs.warning("Se ingreso a la ventana de moficicar los precios")
    
    def cerrar_reiniciar():
        taximetro.detenerActualizacionPrecio()
        taximetro.reiniciarValores()
        taximetro.iniciar()
        nueva_ventana.destroy()
        
    nueva_ventana = tk.Toplevel(window)
    nueva_ventana.title("Ventana Nueva")
    nueva_ventana.geometry("400x300")

    frame = tk.Frame(nueva_ventana)
    frame.pack()

    label = tk.Label(frame, text="¡Modificar precios!")
    label.grid(row=0, column=0, padx=10, pady=10)
    
    label2 = tk.Label(frame, text="¡Precio sin movimiento!")
    label2.grid(row=0, column=0, padx=10, pady=10)
    precio_sin_movimiento = tk.Entry(nueva_ventana)
    precio_sin_movimiento.pack(pady=10, ipady=10, ipadx=50)
        
        
    label3 = tk.Label(frame, text="¡Precio con movimiento!")
    label3.grid(row=0, column=0, padx=10, pady=10)
    precio_con_movimiento = tk.Entry(nueva_ventana)
    precio_con_movimiento.pack(pady=10, ipady=10, ipadx=50)
    
    modificarPrecio_BTN = tk.Button(nueva_ventana, text="Modificar precio", command=lambda:( taximetro.cambiarPreciosBD(precio_sin_movimiento, precio_con_movimiento), cerrar_reiniciar()))
    modificarPrecio_BTN.pack()
    
    
    
    
def descargarHistorial():
    print(taximetro.taximetroActivo)
    if taximetro.taximetroActivo:
        historial = Database_historial()
        historial.all()

taximetro = Taximetro()

window = tk.Tk()
window.title("Taxímetro")
window.geometry("710x510")

# create widgets
descargarHistorial_BTN = tk.Button(window, text="DescargarHistorial", command=descargarHistorial)
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



# modificar

modificarPrecio_BTN = tk.Button(window, text="Modificar precio", command=crearVentanaModificarPrecio)




message_widget = tk.Message(window, text="\tBienvenido al Taxímetro:\n\nPara iniciar el taxi, presiona 'Iniciar '.\nPara mover el taxi, presiona 'Mover '.\nPara detener el taxi, presiona 'Detener '.\nPara finalizar el taxi, presiona 'Finalizar'.", width=400)
message_widget.configure(
    font=("Arial", 13),
    borderwidth=1,
)
message_widget.pack(pady=10)

result_label = tk.Label(window, text="")
result_label.pack()

ruta_fuente = "taximeter.ttf"
custom_font = tkFont.Font(family="taximeter", size=35)


result_label_info = tk.Label(window, font=custom_font, fg="red")
result_label_info.pack()

result_label_count = tk.Label(window, text="")
result_label_count.pack()


# acciones del teclado
keyboard.add_hotkey('enter', iniciarCarrera)
keyboard.add_hotkey('m', moverCoche)
keyboard.add_hotkey('d', detenerCoche)
keyboard.add_hotkey('f', finalizarRecorrido)
keyboard.add_hotkey('h', descargarHistorial)

window.mainloop()



