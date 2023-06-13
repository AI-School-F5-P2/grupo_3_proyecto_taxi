# import libraries
import time
import requests
from datetime import datetime
import tkinter as tk # importar tkinter
from PIL import ImageTk, Image # importar imagenes
from logs import logs # importar logs

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
        if not self.taximetroActivo:
            result_label.config(text="Taximetro inicializado", font=("Arial", 12, "bold"),justify="center")
            self.taximetroActivo = True
            self.tiempoInicio = time.time()
        else:
            result_label.config(text="El taximetro ya se a iniciado", font=("Arial", 12, "bold"),justify="center")
        
    def moverCoche(self):
        if self.taximetroActivo and not self.cocheEnMovimiento:
            if self.yaSeAfrenado:
                self.calcularTarifa("detenido")
                
            self.cocheEnMovimiento = True
            self.tiempoInicio = time.time()
            # print("coche en movimiento")
            result_label.config(text="Coche en movimiento", font=("Arial", 12, "bold"),justify="center")
            result_label_info.config(text=f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.", font=("Arial", 12, "bold"),justify="center")
        elif not self.taximetroActivo:
            # print("Antes de poner a mover el coche debes inicializar el taximetro -> iniciar")
            result_label.config(text="Antes de poner a mover el coche debes inicializar el taximetro -> iniciar", font=("Arial", 12, "bold"),justify="center")
        else:
            # print("El Coche ya esta en movimiento")
            result_label.config(text="El Coche ya esta en movimiento", font=("Arial", 12, "bold"),justify="center")

    def detenerCoche(self):
        if self.cocheEnMovimiento:
            self.cocheEnMovimiento = False
            self.calcularTarifa("moviendose")
            # print(f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.")
            result_label.config(text="El Coche se ha detenido", font=("Arial", 12, "bold"),justify="center")
            result_label_info.config(text=f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.", font=("Arial", 12, "bold"),justify="center")
            self.yaSeAfrenado = True
            self.tiempoInicio = time.time()
        else:
            # print("El coche ya esta denetido")
            result_label.config(text="El coche ya esta denetido", font=("Arial", 12, "bold"),justify="center")
              
    def finalizarRecorrido(self):
        if self.cocheEnMovimiento == False and self.taximetroActivo:
            # print("carrera terminada")
            result_label.config(text="Carrera terminada", font=("Arial", 12, "bold"),justify="center")
            self.tiempoTrancurrido = time.time() - self.tiempoInicio
            self.tarifa = self.tiempoTrancurrido * 0.02
            self.tarifaTotal += self.tarifa
            # print(f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.")
            result_label_info.config(text=f"Total a pagar:  {self.tarifaTotal:.2f} Euros.", font=("Arial", 12, "bold"),justify="center")
            #reinicio todos los valores
            self.taximetroActivo=False
            self.cocheEnMovimiento= False
            self.tiempoInicio = 0
            self.tiempoTrancurrido = 0
            self.tarifaTotal = 0
            self.tarifa = 0
            self.yaSeAfrenado=False
            self.agegrarABaseDeDatos()
            
            
        elif not self.taximetroActivo:
            # print("No hay carrera en curso")
            result_label.config(text="No hay carrera en curso", font=("Arial", 12, "bold"),justify="center")
        else:
            # print("Para finalizar el recorrido primero debes detener el coche -> detener")
            result_label.config(text="Para finalizar el recorrido primero debes detener el coche -> detener", font=("Arial", 12, "bold"),justify="center")
    
    # create method to close the window
    def finalizar_windows(self):
        window.destroy()
        

# create method to calculate the rate
    def calcularTarifa(self,accion):
        if accion == "detenido":
            self.tiempoTrancurrido = time.time() - self.tiempoInicio
            self.tarifa = self.tiempoTrancurrido * 0.02
            self.tarifaTotal += self.tarifa
            # print(f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.")
            result_label_info.config(text=f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.", font=("Arial", 12, "bold"),justify="center")
        if accion == "moviendose":
            self.tiempoTrancurrido = time.time() - self.tiempoInicio
            self.tarifa = self.tiempoTrancurrido * 0.05
            self.tarifaTotal += self.tarifa
            # print(f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.")
            result_label_info.config(text=f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.", font=("Arial", 12, "bold"),justify="center")


    #extraer historial
    def extraerHistorial(self):
        api_url = "http://127.0.0.1:4000/historial"
        response = requests.get(api_url + api_url)
        historial_data = response.json()
        print("Historial:", historial_data)
        return

    #agregar a la base de datos
    def agegrarABaseDeDatos(self):
        fecha_actual = datetime.now()
        fecha_hora_actual_str = fecha_actual.strftime('%Y-%m-%d %H:%M:%S')
        api_url = "http://127.0.0.1:4000/agregar" 
        data = {
            'tarifa': 10,
            'fecha': str(fecha_hora_actual_str)
        }
        
        response = requests.post(api_url, data=data)
        response_data = response.json()
        print("Respuesta:", response_data)



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
    contrasena = entry_contrasena.get()
    logs()
    if contrasena == "1234":
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

# create main loop
window = tk.Tk()

window.title("Taxímetro")
window.geometry("720x480")

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
imagen = Image.open("assets/taxi.png") 
imagen_tk = ImageTk.PhotoImage(imagen)
label = tk.Label(window, image=imagen_tk)
label.pack()
# Resto del código...

# create text area
message_widget = tk.Message(window, text="\tBienvenido al Taxímetro:\n\nPara iniciar el taxi, presiona 'Iniciar '.\nPara mover el taxi, presiona 'Mover '.\nPara detener el taxi, presiona 'Detener '.\nPara finalizar el taxi, presiona 'Finalizar'.", width=400)
message_widget.configure(
    font=("Arial", 13),  # Tamaño y fuente del texto
    borderwidth=1,  # Ancho del borde en píxeles
    # Alineación del texto (centrado)
)
message_widget.pack(pady=10)  # Agregar un espacio de relleno vertical

# label show the result
result_label = tk.Label(window, text="")
result_label.pack()

result_label_info = tk.Label(window, text="")
result_label_info.pack()

result_label_count = tk.Label(window, text="")
result_label_count.pack()

window.mainloop()