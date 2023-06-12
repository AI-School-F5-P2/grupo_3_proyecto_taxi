import tkinter as tk




tarifaEnMovimiento=5
tarifaSinMovimiento=3
contador = 0
total = 0


def arrancar():
 return



def frenar():
 return



def terminarCarrera():
 return
 
 
 

window = tk.Tk()
window.title("Programa de Saludos")
window.geometry("1080x600")
submit_button = tk.Button(window, text="Arrancar", command=arrancar)
submit_button = tk.Button(window, text="Frenar", command=frenar)
submit_button = tk.Button(window, text="Terminar Carrera", command=terminarCarrera)
submit_button.pack() #
window.mainloop()