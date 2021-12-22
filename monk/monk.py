import tkinter as tk 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import core

class Aplicacion(tk.Frame):
   def __init__(self, ventana_ppal):
      tk.Frame.__init__(self,ventana_ppal)
      self.ventana_ppal=ventana_ppal
      self.ventana_ppal.title("Monk")
      self.ventana_ppal.wm_attributes('-zoomed', True)
      self.ventana_ppal.resizable(False, False)

      self.construir_barra_en(ventana_ppal)
      self.construir_panel_en(ventana_ppal)

   def construir_barra_en(self,ventana_ppal):
      barra=tk.Frame(ventana_ppal)
      barra.pack(fill=tk.BOTH)

      botonAbrirArchivo = tk.Button(barra, text="Abrir archivo", command=self.abrir)
      botonAbrirArchivo.pack(side=tk.LEFT)
      self.botonGuardarArchivo = tk.Button(barra, text="Guardar gráfico", command=self.guardar, state= tk.DISABLED)
      self.botonGuardarArchivo.pack(side=tk.LEFT)
      self.botonEditarHallazgo = tk.Button(barra, text="Editar hallazgo", command=self.editar_hallazgo,state= tk.DISABLED)
      self.botonEditarHallazgo.pack(side=tk.LEFT)
      self.botonConsultarAyuda = tk.Button(barra, text="Ayuda", command=self.consultar_ayuda,state= tk.DISABLED)
      self.botonConsultarAyuda.pack(side=tk.LEFT)

   def construir_panel_en(self,ventana_ppal):
      panel=tk.Frame(ventana_ppal)
      #panel.pack()
      panel.pack(fill=tk.BOTH,expand=True)
      
      subpanel1=tk.Frame(panel)
      subpanel1.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
      self.construir_lista(subpanel1)
      
      subpanel2=tk.Frame(panel)
      #subpanel2.pack(side=tk.RIGHT,fill=tk.BOTH)
      subpanel2.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
      self.construir_figura(subpanel2)
         
   def construir_lista(self,subpanel):
      label=tk.Label(subpanel,text='Atributos')
      label.pack(side=tk.TOP)
      # Crear una barra de deslizamiento con orientación vertical.
      scrollbar = tk.Scrollbar(subpanel)
      scrollbar.pack(side="right", fill="y")
      # Vincularla con la lista.
      self.listbox = tk.Listbox(subpanel,selectmode='browse',yscrollcommand=scrollbar.set)
      self.listbox.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
      self.listbox.bind('<<ListboxSelect>>', self.seleccionar_atributo )      
         
   def construir_figura(self,subpanel):    
      label=tk.Label(subpanel,text='Gráfico')
      label.pack(side=tk.TOP)
      self.figura = Figure()
      #ax = self.figura.add_subplot(111)
      self.canvas=FigureCanvasTkAgg(self.figura,subpanel)
      #self.canvas.get_tk_widget().pack(side=tk.RIGHT,fill=tk.BOTH)      
      self.canvas.get_tk_widget().pack(side=tk.LEFT,fill=tk.BOTH,expand=True)    
        
   def abrir(self):
      messagebox.showinfo("Información","Se sugiere usar un archivo con atributos discretizados para un buen funcionamiento")
      ruta = filedialog.askopenfilename(parent=ventana_ppal,title='Abrir archivo csv',filetypes=[('Archivo separado por comas', '.csv')],multiple=False)
      df=pd.read_csv(ruta)
      self.ventana_ppal.title("Monk - "+ruta)
      self.apriori=core.Data(df) ###########
      self.escenario=self.apriori
      self.color_apriori='tab:green'
      self.color_aposteriori='tab:red'
      self.color_escenario=self.color_apriori
      self.listbox.delete(0, tk.END)
      self.figura.clf()
      self.canvas.draw()
      self.botonGuardarArchivo.config(state=tk.DISABLED)
      self.botonEditarHallazgo.config(state=tk.DISABLED)
      self.mostrarAtributos(self.escenario,self.listbox) ###########

   def guardar(self):    
      ruta = filedialog.asksaveasfilename(parent=ventana_ppal,title='Guardar gráfico',filetypes=[('Imagen', '.jpg')])
      self.figura.savefig(ruta)

   def mostrarAtributos(self,datos,listbox):   
      for attribute_name in datos.attributes_names():
         listbox.insert(tk.END, attribute_name)  
      
   def seleccionar_atributo(self,evento):
      listbox = evento.widget 
      self.dibujar(self.escenario,listbox,self.color_escenario) ########### 
      self.botonGuardarArchivo.config(state=tk.NORMAL)
      self.botonEditarHallazgo.config(state=tk.NORMAL)
      
   def dibujar(self,datos,listbox,color_grafico):  
      #obtengo posicion del item seleccionado de la lista
      seleccion = listbox.curselection()
    
      #obtengo el texto correspondiente al elemento seleccionado en la lista 
      nombre_atributo = listbox.get(seleccion)
   
      atributo = datos.attribute(nombre_atributo)

      self.figura.clf()
      
      ax = self.figura.add_subplot(111)
    
      grafico=atributo.plot(kind='bar',table=True,ax=ax,title=datos.scenario_name(),color=color_grafico)
      self.figura.suptitle(nombre_atributo)
      grafico.axes.get_xaxis().set_visible(False)  
    
      self.canvas.draw()
      self.canvas.get_tk_widget().pack(side=tk.LEFT,fill=tk.BOTH,expand=True)

      #binding para detectar clic en el grafico
      self.canvas.mpl_connect('button_press_event', self.cliquear_grafico)   
      
   def cliquear_grafico(self,evento):
      self.editar_hallazgo()
      
   def editar_hallazgo(self):
      #obtengo posicion del item seleccionado de la lista
      seleccion = self.listbox.curselection()
      
      #obtengo el texto correspondiente al elemento seleccionado en la lista 
      nombre_atributo = self.listbox.get(seleccion)


      atributo = self.apriori.attribute(nombre_atributo) #*********#

      self.edicion = tk.Toplevel()
      self.edicion.wm_title("Editar hallazgo")
      
      label=tk.Label(self.edicion, text="               Seleccione una opción:              ")
      label.pack()

      opcion_elegida=tk.StringVar(value='a priori') 
      
      opcion=tk.Radiobutton(self.edicion, text='a priori', variable=opcion_elegida, value='a priori')
      opcion.pack()
      
      for valor in atributo.index.tolist():
         texto = nombre_atributo+'='+valor
         opcion=tk.Radiobutton(self.edicion, text=texto, variable=opcion_elegida, value=valor)
         opcion.pack()

      
      barra=tk.Frame(self.edicion)
      barra.pack()

      botonAceptar = tk.Button(barra, text="Aceptar", command=lambda: self.aceptar(nombre_atributo,opcion_elegida) )
      botonAceptar.pack(side=tk.LEFT)
      botonCancelar = tk.Button(barra, text="Cancelar", command=self.cancelar)
      botonCancelar.pack(side=tk.LEFT)
      
      self.edicion.resizable(False, False)
      self.edicion.wait_visibility() 
      self.edicion.grab_set()                 # define el dialogo como ventana en primer plano
      self.edicion.wait_window()              # en lugar de edicion.mainloop()

   def aceptar(self,nombre_atributo,opcion_elegida):
      if(opcion_elegida.get()!='a priori'):
        self.escenario=self.apriori.new_scenario(nombre_atributo,opcion_elegida.get()) #*********#  
        self.color_escenario=self.color_aposteriori
      else:
        self.escenario=self.apriori
        self.color_escenario=self.color_apriori
      self.dibujar(self.escenario,self.listbox,self.color_escenario) ########### 
      self.edicion.destroy()
      
   def cancelar(self):
      pass
      self.edicion.destroy()
   
   def consultar_ayuda(self):
      pass
      #TODO
      
ventana_ppal=tk.Tk()
aplicacion=Aplicacion(ventana_ppal)

# La siguiente línea hará que cuando se ejecute el programa
# construya y muestre la ventana, quedando a la espera de 
# que alguna persona interactúe con ella.

# Si la persona presiona sobre el botón Cerrar 'X', 
# el programa llegará a su fin.

aplicacion.mainloop()
