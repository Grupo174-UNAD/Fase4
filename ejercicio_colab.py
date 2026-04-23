#Trabajo colaborativo - fase 4 componente practico

class Cliente: #
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        
    def mostrar_informacion(self):
        print(f"Cliente {self.id}: {self.nombre}") 