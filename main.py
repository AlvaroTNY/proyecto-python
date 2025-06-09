from customtkinter import CTk, CTkFrame, CTkEntry, CTkLabel, CTkButton, CTkCheckBox, CTkImage
from PIL import Image  # Importación necesaria para manejar imágenes
import customtkinter as ctk
import os

# Configuración inicial
ctk.set_appearance_mode("dark")

root = CTk() 
root.geometry("500x600+350+20")
root.minsize(480, 500)
root.title("Iniciar Sesion")

frame = CTkFrame(root, fg_color='#010101')
frame.grid(column=0, row=0, sticky='nsew', padx=50, pady=50)

# Configuración de grid (igual que antes)
frame.columnconfigure([0, 1], weight=1)
frame.rowconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Cargar imágenes CORRECTAMENTE
def load_image(path, size):
    """Función auxiliar para cargar imágenes con PIL"""
    return CTkImage(light_image=Image.open(path), size=size)

# Obtener la ruta base del script
base_path = os.path.dirname(os.path.abspath(__file__))

# Cargar imágenes
try:
    logo = load_image(os.path.join(base_path, 'images', 'logo.png'), (100, 100))
    img_google = load_image(os.path.join(base_path, 'images', 'google.png'), (20, 20))
    img_facebook = load_image(os.path.join(base_path, 'images', 'facebook.png'), (20, 20))
except Exception as e:
    print(f"Error cargando imágenes: {e}")
    exit()

# Resto de tu interfaz (igual que antes)
CTkLabel(frame, image=logo, text="").grid(columnspan=2, row=0)

correo = CTkEntry(frame, font=('sans serif', 12), placeholder_text='Correo electronico', 
                 border_color='#2cb67d', fg_color='#010101', width=220, height=40)
correo.grid(columnspan=2, row=1, padx=4, pady=4)

contrasenna = CTkEntry(frame, show="*", font=('sans serif', 12), placeholder_text='Contraseña',
                      border_color='#2cb67d', fg_color='#010101', width=220, height=40)
contrasenna.grid(columnspan=2, row=2, padx=4, pady=4)

checkbox = CTkCheckBox(frame, text="Recordarme", hover_color='#7f5af0', 
                      border_color='#2cb67d', fg_color='#2cb67d')
checkbox.grid(columnspan=2, row=3, padx=4, pady=4)

bt_iniciar = CTkButton(frame, font=('sans serif', 12), border_color='#2cb67d', fg_color='#010101',
                      hover_color='#2cb67d', corner_radius=12, border_width=2,
                      text='INICIAR SESIÓN')
bt_iniciar.grid(columnspan=2, row=4, padx=4, pady=4)

bt_google = CTkButton(frame, font=('sans serif', 12), border_color='#7f5af0', fg_color='#010101', 
                     hover_color='#16161a', corner_radius=12, border_width=2,
                     text=' Google Login ', image=img_google, compound="left")
bt_google.grid(column=0, row=6, padx=4, pady=4)

bt_facebook = CTkButton(frame, font=('sans serif', 12), border_color='#7f5af0', fg_color='#010101',
                       hover_color='#16161a', corner_radius=12, border_width=2,
                       text='Facebook Login', image=img_facebook, compound="left")
bt_facebook.grid(column=1, row=6, padx=4, pady=4)

root.mainloop()