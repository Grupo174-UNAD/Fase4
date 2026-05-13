#Clase Cliente que hereda de la clase Entidad, con atributos privados id_cliente, nombre y correo.
#excepciones para validar el nombre y el correo
from entidades import Entidad
from excepciones import ClienteInvalidoError

class Cliente(Entidad):
#Contador de clientes para asignar un ID único a cada cliente
    contador_clientes = 1
    
    def __init__(self, nombre, correo):
        
        self.__id_cliente = Cliente.contador_clientes
        Cliente.contador_clientes += 1
        
        self.set_nombre(nombre)
        self.set_correo(correo)
#Uso de get y set para acceder y modificar los atributos 
    def get_id_cliente(self):
        return self.__id_cliente
    
    def get_nombre(self):
        return self.__nombre
    
    def get_correo(self):
        return self.__correo
    
    def set_nombre(self, nombre):
#Validación del nombre para que no esté vacío y no contenga números
        if not nombre.strip():
            raise ClienteInvalidoError("El nombre no puede estar vacío.")
        if not nombre.replace(" ", "").isalpha():
            raise ClienteInvalidoError("Aseguere de que el nombre no contenga numeros.")
        self.__nombre = nombre
#Validación del correo para que contenga el símbolo "@" y tenga un formato básico de correo electrónico
    def set_correo(self, correo):
        if "@" not in correo:
            raise ClienteInvalidoError("Correo incorrecto. Debe contener '@' ejemplo: usuario@abc")
        self.__correo = correo
#Mostrar la información del cliente
    def mostrar_info(self):
        return (f"id:{self.__id_cliente} {self.__nombre} ({self.__correo})")
    
    