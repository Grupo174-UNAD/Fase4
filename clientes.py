from entidades import Entidad
from excepciones import ClienteInvalidoError

class Cliente(Entidad):
    
    contador_clientes = 1
    
    def __init__(self, nombre, correo):
        
        self.__id_cliente = Cliente.contador_clientes
        Cliente.contador_clientes += 1
        
        self.set_nombre(nombre)
        self.set_correo(correo)
        
    def get_id_cliente(self):
        return self.__id_cliente
    
    def get_nombre(self):
        return self.__nombre
    
    def get_correo(self):
        return self.__correo
    
    def set_nombre(self, nombre):
        if not nombre.strip():
            raise ClienteInvalidoError("El nombre no puede estar vacío.")
        if not nombre.replace(" ", "").isalpha():
            raise ClienteInvalidoError("El nombre solo puede contener letras y espacios.")
        self.__nombre = nombre

    def set_correo(self, correo):
        if "@" not in correo or "." not in correo:
            raise ClienteInvalidoError("Correo inválido.")
        self.__correo = correo

    def mostrar_info(self):
        return f"Cliente {self.__id_cliente}: {self.__nombre} ({self.__correo})"