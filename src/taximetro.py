import time
import getpass



class Taximetro:
    def __init__(self):
        self.taximetroActivo=False
        self.cocheEnMovimiento= False
        self.tiempoInicio = 0
        self.tiempoTrancurrido = 0
        self.tarifaTotal = 0
        self.tarifa = 0
        self.yaSeAfrenado=False
        
        
        
    def iniciar(self):
        if not self.taximetroActivo:
            print("Taximetro inicializado")
            self.taximetroActivo = True
            self.tiempoInicio = time.time()
        else:
            print("El taximetro ya se a iniciado")
        
    
    def moverCoche(self):
        if self.taximetroActivo and not self.cocheEnMovimiento:
            if self.yaSeAfrenado:
                self.calcularTarifa("detenido")
                
            self.cocheEnMovimiento = True
            self.tiempoInicio = time.time()
            print("coche en movimiento")
        elif not self.taximetroActivo:
            print("Antes de poner a mover el coche debes inicializar el taximetro -> iniciar")
        else:
            print("El Coche ya esta en movimiento")


    def detenerCoche(self):
        if self.cocheEnMovimiento:
            self.cocheEnMovimiento = False
            self.calcularTarifa("moviendose")
            print(f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.")
            self.yaSeAfrenado = True
            self.tiempoInicio = time.time()
        else:
            print("El coche ya esta denetido")
            
    
  
    def finalizarRecorrido(self):
        if self.cocheEnMovimiento == False and self.taximetroActivo:
            print("carrera terminada")
            self.tiempoTrancurrido = time.time() - self.tiempoInicio
            self.tarifa = self.tiempoTrancurrido * 0.02
            self.tarifaTotal += self.tarifa
            print(f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.")
            #reinicio todos los valores
            self.taximetroActivo=False
            self.cocheEnMovimiento= False
            self.tiempoInicio = 0
            self.tiempoTrancurrido = 0
            self.tarifaTotal = 0
            self.tarifa = 0
            self.yaSeAfrenado=False
            
        elif not self.taximetroActivo:
            print("No hay carrera en curso")
        else:
            print("Para finalizar el recorrido primero debes detener el coche -> detener")
            
            
            
            
    def calcularTarifa(self,accion):
        if accion == "detenido":
            self.tiempoTrancurrido = time.time() - self.tiempoInicio
            self.tarifa = self.tiempoTrancurrido * 0.02
            self.tarifaTotal += self.tarifa
            print(f"Tiempo transcurrido desde que se detuvo el taxi {self.tiempoTrancurrido}")
            print(f"Tarifa de ese tiempo transcurrido {self.tarifa}")
            print(f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.")
        if accion == "moviendose":
            self.tiempoTrancurrido = time.time() - self.tiempoInicio
            self.tarifa = self.tiempoTrancurrido * 0.05
            self.tarifaTotal += self.tarifa
            print(f"Se ha acumulado una tarifa de {self.tarifaTotal:.2f} Euros.")
            
                 
    def correr(self):
        
            print("Bienvenido")
            contrasena = getpass.getpass("Por favor, ingrese la contraseña: ")

            if contrasena == "1234":
                
                print("Para iniciar la carrera, ingresa 'iniciar'")
                print("Para mover el taxi, ingresa 'mover'")
                print("Para detener el taxi, ingresa 'detener'")
                print("Para finalizar la carrera, ingresa 'fin'")
                print("Para salir del programa, ingresa 'salir'")
                
                while True:
                    instruccion = input("Ingrese una instrucción: ")

                    if instruccion == "iniciar":
                        self.iniciar()
                    if instruccion == "mover":
                        self.moverCoche()
                    elif instruccion == "detener":
                        self.detenerCoche()
                    elif instruccion == "fin":
                        self.finalizarRecorrido()
                    elif instruccion == "salir":
                        break
                
            else:
                print("Contraseña Incorrecta")
            