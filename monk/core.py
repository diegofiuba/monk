import pandas as pd
import matplotlib.pyplot as plt

class Data():    
            
    def __init__(self,df,scenario='a priori'):
        self.el_escenario=scenario
        self.dataframe=df
        casosTotales=len(self.dataframe.index)
        self.dic_atributos={}
        for column in self.dataframe.columns:
           #ocurrencias=round(df[column].value_counts()/casosTotales,2)
           ocurrencias=( (self.dataframe[column].value_counts()/casosTotales)*100 ).round().astype(int)
           self.dic_atributos[column]=ocurrencias
    
    def scenario_name(self):
        return self.el_escenario
    
    def attributes_names(self):
        return self.dataframe.columns.tolist()
    
    def attribute(self,attribute_name):
        return self.dic_atributos[attribute_name]
    
    ###
    
    def scenario(self):
        print(self.el_escenario)
    
    def attributes(self):
        for atributo in self.dic_atributos:
            print(atributo)
    
    def proba_func(self,attribute_name):
        print(self.dic_atributos[attribute_name]) 
        
    def proba(self,attribute_name,value):
        print(self.dic_atributos[attribute_name][value])         
                    
    def proba_func_attributes(self):
        for atributo in self.dic_atributos:
            print(self.dic_atributos[atributo])

    def plot_proba_func(self,attribute_name):
        atributo=self.dic_atributos[attribute_name]     
        grafico=atributo.plot(kind='bar',table=True,title=self.el_escenario)#,color=self.color)
        plt.suptitle(attribute_name)
        grafico.axes.get_xaxis().set_visible(False)        
        plt.show()
        
    def plot_proba_func_attributes(self):
        for nombre_atributo in self.dic_atributos:
            self.plot_proba_func(nombre_atributo)            
    
    def export_proba_func(self,attribute_name,path):
        #self.dic_atributos[nombre_atributo].to_csv(ruta,header=['prob'],index_label=nombre_atributo)
        self.dic_atributos[attribute_name].to_csv(path,header=[self.el_escenario],index_label=attribute_name)

    def new_scenario(self,attribute_name,value):
        #filtra para quedarse con las filas que contengan la evidencia
        df2=self.dataframe.loc[self.dataframe[attribute_name]==value,:]
        return Data(df2,f'{attribute_name}={value}')
   
    def compare(self,data_list,attribute_name):
        comparacion = pd.DataFrame()
        comparacion[self.el_escenario]=self.dic_atributos[attribute_name]
        comparacion.index.name=attribute_name
        for datos in data_list:
            comparacion[datos.el_escenario]=datos.dic_atributos[attribute_name]
        print(comparacion)           

    def plot_compare(self,data_list,attribute_name):
        comparacion = pd.DataFrame()
        comparacion[self.el_escenario]=self.dic_atributos[attribute_name]
        comparacion.index.name=attribute_name
        escenarios=self.el_escenario
        for datos in data_list:
            comparacion[datos.el_escenario]=datos.dic_atributos[attribute_name]
            escenarios=escenarios+' vs. '+datos.el_escenario
            
        grafico=comparacion.plot(kind='bar',table=True,title=escenarios)
        plt.suptitle(attribute_name)
        grafico.axes.get_xaxis().set_visible(False)
		#plt.show()
        plt.show(block=True)
        plt.interactive(False)

    def export_compare(self,data_list,attribute_name,path):
        comparacion = pd.DataFrame()
        comparacion[self.el_escenario]=self.dic_atributos[attribute_name]
        comparacion.index.name=attribute_name
        for datos in data_list:
            comparacion[datos.el_escenario]=datos.dic_atributos[attribute_name]
        comparacion.to_csv(path,header=comparacion.columns.tolist(),index_label=attribute_name)
