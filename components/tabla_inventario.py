import customtkinter as ctk
import colors
from tkfontawesome import icon_to_image
import functools


class TablaInventario(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(corner_radius=0, fg_color=colors.grey)
        
        _edit_icon = icon_to_image('edit', fill=colors.grey, scale_to_width=16)
        _trash_icon = icon_to_image('trash-alt', fill=colors.grey, scale_to_width=16)
        
        # Estas son las cabeceras que indican qué va en cada columna
        headers = ["ID", "Descripcion", "Cantidad"]
        
        # Esta cosa hace que se muestren los headers en la app, creando objetos de Etiqueta por cada header 
        for col, header in enumerate(headers):
            etiqueta = ctk.CTkLabel(self, text=header, width=30, text_color=colors.darkbrown, font=("Helvetica", 18, "bold"))
            etiqueta.grid(row=0, column=col, sticky='wn')
        
        # Esto es importante, si van a hacer alguna tabla, usen el "get" correspondiente
        # En este caso, estoy trayendo todas las citas. Pueden ver cómo funciona en ./controllers/postgres.py
        fetch_inventario = parent.conn.getInventory() # Esto lo van a cambiar por el que corresponde a la pantalla
        
        # Este es el dataset que deberán organizar. Será usado para mostrarlo en la app
        # Con objetos de Etiqueta (ctk.CTkLabel)
        # Cambien la variable "cita" por cualquier otra cosa para que se entienda bien
        # Lo que está entre comillas simples es EL NOMBRE DE LA COLUMNA QUE VIENE EN NUESTRA BASE DE DATOS
        data = [(
                inventario['idinventario'],
                inventario['descripcion'],
                inventario['cantidad'],
                )
                for inventario in fetch_inventario]
        

        # Esto muestra en la app cada registro del dataset que armaron anteriormente.
        for i, fila in enumerate(data, start=1):
            for j, valor in enumerate(fila):
                etiqueta = ctk.CTkLabel(self, text=valor, font=("Helvetica", 16))
                etiqueta.grid(row=i, column=j, sticky='w')
            ctk.CTkButton(self,
                        image=_edit_icon,
                        text="",
                        fg_color=colors.darkbrown,
                        hover_color=colors.brown,
                        width=10,
                        height=10,
                        corner_radius=20,
                        command=functools.partial(self.editAppointment, data[i-1][0])).grid(row=i, column=j, sticky='e')
            
            # Botón de eliminar
            ctk.CTkButton(self,
                        image=_trash_icon,
                        text="",
                        fg_color=colors.darkbrown,
                        hover_color=colors.brown,
                        width=10,
                        height=10,
                        corner_radius=20,
                        command=functools.partial(self.deleteAppointment, data[i-1][0])).grid(row=i, column=j+1, sticky='e')
            
                
        # Esto, también importante, es para modificar el tamaño horizontal de cada columna
        # De la siguiente función:
        #   self.grid_columnconfigure(0, weight=1)
        # - el primer parámetro (0) es el índice de la columna
        # - el segundo parámetro (weight=1) indica el tamaño horizontal que le toca A ESA COLUMNA EN ESPECIFICO
        
        self.grid_columnconfigure(0, weight=1) # ID
        self.grid_columnconfigure(1, weight=4) # Descripcion
        self.grid_columnconfigure(2, weight=1) # Cantidad
        self.grid_columnconfigure(3, weight=1) # boton editar
        self.grid_columnconfigure(4, weight=1) # boton eliminar

        
        self.pack(expand=True, fill='both')
        
    def deleteInventory(self, idinventario):
        self.parent.conn.deleteInventory(str(idinventario))
        
        # Recarga la pantalla
        self.change_page("Inventario")
        
    def editInventory(self, idinventario):
        inventario = self.parent.conn.getInventory(idinventario)
        
        self.change_page("AgregarInventario", inventario)