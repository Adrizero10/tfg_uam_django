import tkinter as tk
from tkinter import ttk
from Django.tfg_urls.home.phising import url_phising

def main():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Te quieroooo lupitaaa :)")

    # Configurar el tamaño de la ventana y el color de fondo
    root.geometry("500x400")
    root.configure(bg='#e0f7fa')

    # Estilo para los widgets
    style = ttk.Style()
    style.theme_use('clam')  # Usar el tema 'clam' para una apariencia más moderna

    # Configuración de estilos
    style.configure('TLabel', font=('Helvetica', 14, 'italic'), background='#e0f7fa', foreground='#4b6043')
    style.configure('TEntry', font=('Helvetica', 12), foreground='#4b6043', fieldbackground='#ffffff')
    style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=6, background='#a3c9a8', foreground='#ffffff')
    style.map('TButton', background=[('active', '#8fb996'), ('!active', '#a3c9a8')])

    # Crear un marco para el contenido central
    main_frame = tk.Frame(root, bg='#dcedc8', bd=2, relief='groove')
    main_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=300)

    # Crear y empaquetar el mensaje de bienvenida
    welcome_label = ttk.Label(main_frame, text="Phising detector")
    welcome_label.pack(pady=20)

    # Crear y empaquetar el campo de entrada de texto
    entry_label = ttk.Label(main_frame, text="Introduce your campany url")
    entry_label.pack(pady=10)

    text_entry = ttk.Entry(main_frame, width=30)
    text_entry.pack(pady=10)

    # Crear y empaquetar el botón
    submit_button = ttk.Button(main_frame, text="Enviar", command=lambda: submit_action(text_entry.get()))
    submit_button.pack(pady=20)

    # Ejecutar el bucle principal de la interfaz gráfica
    root.mainloop()

def submit_action(text):
    print(f"Texto introducido: {text}")
    url_phising(text)

if __name__ == "__main__":
    main()
