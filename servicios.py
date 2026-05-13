#Archivos de las clases de cada servicio, con sus respectivos atributos y métodos
from abc import ABC, abstractmethod
from entidades import Entidad
from excepciones import ServicioInvalidoError
#Clase abstracta Servicio que hereda de la clase Entidad
class Servicio(Entidad, ABC):
    
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
        self.validar_servicio()
        
    @abstractmethod
    def mostrar_info(self):
        pass
#Método para validar que el servicio tenga un nombre y un precio válido
    def validar_servicio(self):
        if not self.nombre or self.precio <= 0:
            raise ServicioInvalidoError("El servicio es inválido.")
#Clases de los servicios cada uno con diferentes atributos y métodos para mostrar la información del servicio
class ReservaSalas(Servicio):
    
    def __init__(self, nombre, capacidad, precio):
        super().__init__(nombre, precio)
        self.capacidad = capacidad
#Mostrar la información de cada servicio seleccionado
    def mostrar_info(self):
        return f"La reserva de {self.nombre} con capacidad de {self.capacidad} personas tiene un costo de {self.precio}"
    
class AlquilerEquipos(Servicio):
    
    def __init__(self, nombre, precio):
        super().__init__(nombre, precio)
        
    def mostrar_info(self):
        return f"El alquiler de {self.nombre} tiene un costo de {self.precio}"
    
class AsesoriaEspecializada(Servicio):
    
    def __init__(self, area, precio):
        super().__init__(area, precio)
        self.area = area
        
    def mostrar_info(self):
        return f"El servicio de {self.area} tiene un costo de {self.precio}"