# import libraries
from flask import Flask
import time
import requests
from datetime import datetime
import tkinter as tk # importar tkinter
from PIL import ImageTk, Image # importar imagenes
from logs import logs # importar logs
from database import Database
import os


# create class
class Taximetro:
    def __init__(self):
        self.taximetroActivo=False
        self.cocheEnMovimiento= False
        self.tiempoInicio = 0
        self.tiempoTrancurrido = 0
        self.tarifaTotal = 0
        self.tarifa = 0
        self.yaSeAfrenado=False
        

    # create methods
    def iniciar(self):
        result_label_info.config(text=f"")
        if not self.taximetroActivo:
            if self.tarifaTotal > 0:
                self.tarifaTotal = 0
            result_label.config(text="Taximetro inicializado", font=("Arial", 12, "bold"),justify="center")
            self.taximetroActivo = True
            self.tiempoInicio = time.time()
        else:
            result_label.config(text="El taximetro ya se a iniciado", font=("Arial", 12, "bold"),justify="center")
        
    # metodo cuando el coche se mueve
    def moverCoche(self):
        if self.taximetroActivo and not self.cocheEnMovimiento:
            if self.yaSeAfrenado:
                self.calcularTarifa("detenido")
                
            self.cocheEnMovimiento = True
            self.tiempoInicio = time.time()
            result_label.config(text="Coche en movimiento", font=("Arial", 12, "bold"),justify="center")
        elif not self.taximetroActivo:
            # print("Antes de poner a mover el coche debes inicializar el taximetro -> iniciar")
            result_label.config(text="Antes de poner a mover el coche debes inicializar el taximetro -> iniciar", font=("Arial", 12, "bold"),justify="center")
        else:
            # print("El Coche ya esta en movimiento")
            result_label.config(text="El Coche ya esta en movimiento", font=("Arial", 12, "bold"),justify="center")

    # metodo cuando se detiene el coche
    def detenerCoche(self):
        if self.cocheEnMovimiento:
            self.cocheEnMovimiento = False
            self.yaSeAfrenado = True
            self.calcularTarifa("moviendose")
            result_label.config(text="El Coche se ha detenido", font=("Arial", 12, "bold"),justify="center")
            self.tiempoInicio = time.time()
        else:
            #print("El coche ya esta detenido")
            result_label.config(text="El coche ya esta denetido", font=("Arial", 12, "bold"),justify="center")
              
    # metodo para calcular la tarifa
    def finalizarRecorrido(self):
        if self.cocheEnMovimiento == False and self.taximetroActivo:
            result_label.config(text="Carrera terminada\n para inicar otra carrera da click en 'iniciar carrera'", font=("Arial", 12, "bold"),justify="center")
            self.calcularTarifa("detenido")
            self.agegrarABaseDeDatos()
            result_label_info.config(text=f"Total a pagar:  {self.tarifaTotal:.2f} Euros.", font=("Arial", 12, "bold"),justify="center")
            #reinicio todos los valores
            self.taximetroActivo=False
            self.cocheEnMovimiento= False
            self.tiempoInicio = 0
            self.tiempoTrancurrido = 0
            self.tarifaTotal = 0
            self.tarifa = 0
            self.yaSeAfrenado=False

        elif not self.taximetroActivo:
            # print("No hay carrera en curso")
            result_label.config(text="No hay carrera en curso", font=("Arial", 12, "bold"),justify="center")
        else:
            # print("Para finalizar el recorrido primero debes detener el coche -> detener")
            result_label.config(text="Para finalizar el recorrido primero debes detener el coche -> detener", font=("Arial", 12, "bold"),justify="center")
    
    # create method to close the window
    def finalizar_windows(self):
        window.destroy()
        
    #create method to calculate the rate
    def calcularTarifa(self,accion):
        monto:float
        if accion == "detenido":
            monto = 0.02
        elif accion == "moviendose":
            monto = 0.05
        
        self.tiempoTrancurrido = time.time() - self.tiempoInicio
        self.tarifa = int(self.tiempoTrancurrido) * monto
        self.tarifaTotal += self.tarifa
        result_label_info.config(text=f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.", font=("Arial", 12, "bold"),justify="center")

    #extraer historial
    def extraerHistorial(self):
        database = Database()
        historial = database.all()
        return historial

    # agregar a la base de datos
    def agegrarABaseDeDatos(self):
        fecha_actual = datetime.now()
        fecha_hora_actual_str = fecha_actual.strftime('%Y-%m-%d %H:%M:%S')
        database = Database()
        data = {
            "tarifa":str(self.tarifaTotal),
            "fecha": str(fecha_hora_actual_str)
        }
        database.insertar(data)
        print("Se agrego a la base de datos")
        return 
<<<<<<< HEAD
=======
    
    #guardar en un archivo .txt
    
        
        # archivo_txt.close()

>>>>>>> d86be2a056dfe8620984b9b5424d5985dad94f14

# create method to run the program       
    # def correr(self):
    #         print("Para iniciar la carrera, ingresa 'iniciar'")
    #         print("Para mover el taxi, ingresa 'mover'")
    #         print("Para detener el taxi, ingresa 'detener'")
    #         print("Para finalizar la carrera, ingresa 'fin'")
    #         print("Para salir del programa, ingresa 'salir'")
    #         instruccion = input("Ingrese una instrucción: ")

    #         if instruccion == "iniciar":
    #             self.iniciar()
    #         if instruccion == "mover":
    #             self.moverCoche()
    #         elif instruccion == "detener":
    #             self.detenerCoche()
    #         elif instruccion == "fin":
    #             self.finalizarRecorrido()
    #         elif instruccion == "salir":
    #             return
    #         else:
    #             print("Contraseña Incorrecta")

def iniciar_carrera():
    # obtener la contreseña ingresada
    contrasena_ingresada = entry_contrasena.get()
    # instanciar la clase Database
    database = Database()
    # obtener la contraseña de la base de datos
    contraseña_bbdd = database.password_get()
    # obtener la contraseña ingresada encryptada
    contaseña_hash = database.password_hash(contrasena_ingresada)
    # testing
        #unittest.main()
    # logs 
    logs()
    if contaseña_hash == contraseña_bbdd:
        # Ocultar widgets de inicio de sesión
        label_contrasena.pack_forget()
        button_iniciar.pack_forget()
        entry_contrasena.pack_forget()
        message_widget.pack_forget()
        # Mostrar botones de la carrera
        button_init.pack(pady=10, ipady=10, ipadx=100)
        button_mover.pack(pady=10, ipady=10, ipadx=100)
        button_detener.pack(pady=10, ipady=10, ipadx=100)
        button_finalizar.pack(pady=10, ipady=10, ipadx=90)
        button_close.pack()

        taximetro.iniciar()
    else:
        label_contrasena.config(text="Contraseña Incorrecta", font=("Arial", 12, "bold"), justify="center")
        label_contrasena.pack(pady=10, ipady=10, ipadx=100)

def mover_coche():
    taximetro.moverCoche()

def detener_coche():
    taximetro.detenerCoche()

def finalizar_recorrido():
    taximetro.finalizarRecorrido()

taximetro = Taximetro()

# init tkinter, window, resoluction and title
window = tk.Tk()
window.title("Taxímetro")
window.geometry("720x480")

# create widgets
button_init = tk.Button(window, text="Iniciar Carrera", command=iniciar_carrera)
button_mover = tk.Button(window, text="Mover Coche", command=mover_coche)
button_detener = tk.Button(window, text="Detener Coche", command=detener_coche)
button_finalizar = tk.Button(window, text="Finalizar Recorrido", command=finalizar_recorrido)
button_close = tk.Button(window, text="Cerrar", command=taximetro.finalizar_windows)

# create widgets
label_contrasena = tk.Label(window, text="Por favor, ingrese la contraseña:", font=("Arial", 12, "bold"),justify="center")
label_contrasena.pack(pady=10, ipady=10, ipadx=100)

# create entry
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

# call the mainloop
button_iniciar = tk.Button(window, text="Iniciar Carrera", command=iniciar_carrera)
button_iniciar.pack(padx=10, pady=10, ipady=10, ipadx=100)

# create image
imagen = Image.open("../assets/taxi.png") 
imagen_tk = ImageTk.PhotoImage(imagen)
label = tk.Label(window, image=imagen_tk)
label.pack()

# create message
message_widget = tk.Message(window, text="\tBienvenido al Taxímetro:\n\nPara iniciar el taxi, presiona 'Iniciar '.\nPara mover el taxi, presiona 'Mover '.\nPara detener el taxi, presiona 'Detener '.\nPara finalizar el taxi, presiona 'Finalizar'.", width=400)
message_widget.configure(
    font=("Arial", 13), 
    borderwidth=1,  
)
message_widget.pack(pady=10)  

# label show the result
result_label = tk.Label(window, text="")
result_label.pack()

# label show the result
result_label_info = tk.Label(window, text="")
result_label_info.pack()

# label show the result
result_label_count = tk.Label(window, text="")
result_label_count.pack()

<<<<<<< HEAD
# loop the window
window.mainloop()
=======
window.mainloop()


taximetro = Taximetro()
textoPlano = taximetro.guardarEnHistorial()

>>>>>>> d86be2a056dfe8620984b9b5424d5985dad94f14
