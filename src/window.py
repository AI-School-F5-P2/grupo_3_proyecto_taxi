import tkinter as tk
import tkinter.font as tkFont
from database_data import Data
from logs import logs
from PIL import ImageTk, Image
from taximetro import Taximetro
import time

class Ventana:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Taximetro")
        self.window.geometry("710x510")
        self.taximetro = Taximetro()
        self.contador = 0
        # self.init = Taximetro()
    
    
    def actualizarpreciodos(self):
        return self.contador


    def finalizarWindows(self):
        self.window.destroy()

    def actualizarPrecio(self):
        self.taximetro.actualizarPrecio()
        newvalor = self.taximetro.tarifaTotal
        print(newvalor)
        self.result_label_info.config(text=f"{newvalor:.2f} EUROS.", font=self.custom_font, justify="center", bg="black", fg="white",  borderwidth=2, relief="solid", padx=5, pady=5)
        self.taximetro.actualizar_precio = self.window.after(1000, self.actualizarpreciodos)

    def iniciarCarrera(self):
        contrasena_ingresada = self.entry_contrasena.get()
        usuario = Data()
        contraseña_bbdd = usuario.password_get()
        contaseña_hash = usuario.password_hash(contrasena_ingresada)
        logs()
        if contaseña_hash == contraseña_bbdd:
            
            self.label_contrasena.pack_forget()
            self.button_iniciar.pack_forget()
            self.entry_contrasena.pack_forget()
            self.message_widget.pack_forget()
            self.button_init.pack(pady=10, ipady=10, ipadx=100)
            self.button_mover.pack(pady=10, ipady=10, ipadx=100)
            self.button_detener.pack(pady=10, ipady=10, ipadx=100)
            self.button_finalizar.pack(pady=10, ipady=10, ipadx=90)
            self.button_close.pack()
            data = Data()
            precios = data.precios()
            self.precio_mov = precios[0]["precio_mov"] if precios else 0.05
            self.precio_det = precios[0]["precio_det"] if precios else 0.02
            self.precioActual = self.precio_det
            if not self.taximetro.taximetroActivo:
                if self.taximetro.tarifaTotal > 0:
                    self.taximetro.tarifaTotal = 0
                self.result_label.config(text="Taximetro inicializado", font=("Arial", 12, "bold"), justify="center")
                self.taximetro.taximetroActivo = True
                self.taximetro.tiempoInicio = time.time()
                
                self.taximetro.actualizar_precio = self.window.after(1000, self.actualizarPrecio)

            else:
                self.result_label.config(text="El taximetro ya se ha iniciado", font=("Arial", 12, "bold"), justify="center")
        if not self.taximetro.taximetroActivo:
            self.result_label.config(text="Taximetro inicializado", font=("Arial", 12, "bold"), justify="center")
            # modificarPrecio_BTN.pack(padx=10, pady=10, side="right")
        else:
            self.label_contrasena.config(text="Contraseña Incorrecta", font=("Arial", 12, "bold"), justify="center")
            self.label_contrasena.pack(pady=10, ipady=10, ipadx=100)


    def moverCoche(self):
        self.taximetro.moverCoche()

    def detenerCoche(self):
        self.taximetro.detenerCoche()

    def finalizarRecorrido(self):
        self.taximetro.finalizarRecorrido()
        
    def crearVentanaModificarPrecio(self):
        self.taximetro = Taximetro()



    def crearButtons(self):
        self.button_init = tk.Button(self.window, text="Iniciar Carrera", command=self.iniciarCarrera)
        self.button_mover = tk.Button(self.window, text="Mover Coche", command=self.moverCoche)
        self.button_detener = tk.Button(self.window, text="Detener Coche", command=self.detenerCoche)
        self.button_finalizar = tk.Button(self.window, text="Finalizar Recorrido", command=self.finalizarRecorrido)
        self.button_close = tk.Button(self.window, text="Cerrar", command=self.taximetro.finalizarWindows)

        self.label_contrasena = tk.Label(self.window, text="Por favor, ingrese la contraseña:", font=("Arial", 12, "bold"), justify="center")
        self.label_contrasena.pack(pady=10, ipady=10, ipadx=100)


        self.entry_contrasena = tk.Entry(self.window, show="*")
        self.entry_contrasena.pack(pady=10, ipady=10, ipadx=50)
        self.entry_contrasena.configure(
            font=("Arial", 12),
            bg="white",
            fg="black",
            relief="solid",
            width=20,
            justify="center",
        )
        self.button_iniciar = tk.Button(self.window, text="Iniciar Carrera", command=self.iniciarCarrera)
        self.button_iniciar.pack(padx=10, pady=10, ipady=10, ipadx=100)

        imagen = Image.open("../assets/taxi.png")
        imagen_tk = ImageTk.PhotoImage(imagen)
        label = tk.Label(self.window, image=imagen_tk)
        label.pack()


        self.message_widget = tk.Message(self.window, text="\tBienvenido al Taxímetro:\n\nPara iniciar el taxi, presiona 'Iniciar '.\nPara mover el taxi, presiona 'Mover '.\nPara detener el taxi, presiona 'Detener '.\nPara finalizar el taxi, presiona 'Finalizar'.", width=400)
        self.message_widget.configure(
        font=("Arial", 13),
        borderwidth=1,
        )
        self.message_widget.pack(pady=10)

        ruta_fuente = "taximeter.ttf"
        self.custom_font = tkFont.Font(family="taximeter", size=35)


        self.result_label = tk.Label(self.window, text="")
        self.result_label.pack()
        self.result_label_info = tk.Label(self.window, font=self.custom_font, fg="red")
        self.result_label_info.pack()

        self.result_label_count = tk.Label(self.window, text="")
        self.result_label_count.pack()
        self.window.mainloop()

        # self.button_iniciar = tk.Button(self.window, text="Iniciar Carrera", command=self.iniciarCarrera)
        # self.button_iniciar.pack(padx=10, pady=10, ipady=10, ipadx=100)

        # self.imagen = self.Image.open("../assets/taxi.png")
        # self.imagen_tk = self.ImageTk.PhotoImage(self.imagen)
        # self.label = tk.Label(self.window, image=self.imagen_tk)
        # self.label.pack()

        # self.modificarPrecio_BTN = tk.Button(self.window, text="Modificar precio", command=self.crearVentanaModificarPrecio)

        # self.message_widget = tk.Message(self.window, text="\tBienvenido al Taxímetro:\n\nPara iniciar el taxi, presiona 'Iniciar '.\nPara mover el taxi, presiona 'Mover '.\nPara detener el taxi, presiona 'Detener '.\nPara finalizar el taxi, presiona 'Finalizar'.", width=400)
        # self.message_widget.configure(
        #     font=("Arial", 13),
        #     borderwidth=1,
        # )
        # self.message_widget.pack(pady=10)

        # self.result_label = tk.Label(self.window, text="")
        # self.result_label.pack()

        # self.ruta_fuente = "taximeter.ttf"
        # self.custom_font = tkFont.Font(family="taximeter", size=35)


        # self.result_label_info = tk.Label(self.window, font=self.custom_font, fg="red")
        # self.result_label_info.pack()

        # self.result_label_count = tk.Label(self.window, text="")
        # self.result_label_count.pack()

        # self.window.mainloop()


    

    def crearVentanaModificarPrecio(self):
        taximetro = Taximetro()
        
        def cerrar_reiniciar():
            nueva_ventana.destroy()
        
        nueva_ventana = tk.Toplevel(self.window)
        nueva_ventana.title("Ventana Nueva")
        nueva_ventana.geometry("400x300")

        frame = tk.Frame(nueva_ventana)
        frame.pack()

        label = tk.Label(frame, text="¡Modificar precios!")
        label.grid(row=0, column=0, padx=10, pady=10)
        
        label = tk.Label(frame, text="¡Precio sin movimiento!")
        label.grid(row=0, column=0, padx=10, pady=10)
        precio_sin_movimiento = tk.Entry(nueva_ventana)
        sin_movimiento = precio_sin_movimiento.get()
        precio_sin_movimiento.pack(pady=10, ipady=10, ipadx=50)
            
            
        label = tk.Label(frame, text="¡Precio con movimiento!")
        label.grid(row=0, column=0, padx=10, pady=10)
        precio_con_movimiento = tk.Entry(nueva_ventana)
        con_movimiento = precio_con_movimiento.get()
        print(con_movimiento)
        precio_con_movimiento.pack(pady=10, ipady=10, ipadx=50)
        
        modificarPrecio_BTN = tk.Button(nueva_ventana, text="Modificar precio", command=lambda:( taximetro.cambiarPreciosBD(precio_sin_movimiento, precio_con_movimiento), cerrar_reiniciar()))
        modificarPrecio_BTN.pack()
        

    # def moverCoche():
    #     taximetro.moverCoche()

    # def detenerCoche():
    #     taximetro.detenerCoche()

    # def finalizarRecorrido():
    #     taximetro.finalizarRecorrido()
        
    # def crearVentanaModificarPrecio():
    #     taximetro = Taximetro()




ventana = Ventana()
ventana.crearButtons()