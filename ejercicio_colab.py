#Trabajo colaborativo - fase 4 componente practico

""

# Importamos lo necesario: ABC para clases abstractas, datetime para fechas
from abc import ABC, abstractmethod
import datetime

# Lista global que actúa como nuestro "archivo" de logs pero en memoria
registro_logs = []

# Función que guarda eventos en la lista y los muestra en pantalla
def log(tipo, mensaje):
    entrada = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [{tipo}] {mensaje}"
    registro_logs.append(entrada)
    print(entrada)


 #EXCEPCIONES PERSONALIZADAS  
# Creamos nuestros propios tipos de error para identificarlos mejor

class ErrorFJ(Exception):
    pass  # Excepción base del sistema, las demás heredan de aquí

class ErrorCliente(ErrorFJ):
    pass  # Para errores relacionados con datos del cliente

class ErrorServicio(ErrorFJ):
    pass  # Para errores cuando el servicio no está bien o no existe

class ErrorReserva(ErrorFJ):
    pass  # Para errores al momento de hacer o gestionar una reserva

class ErrorCosto(ErrorFJ):
    pass  # Para errores en el cálculo del precio


 #CLASE BASE ABSTRACTA  
# No se puede instanciar sola, solo sirve para que otras clases hereden de ella

class Entidad(ABC):
    def __init__(self, id_entidad):
        self._id = id_entidad  # Atributo protegido (con guion bajo = no tocar desde afuera)

    @property
    def id(self):
        return self._id  # Getter: forma segura de leer el id

    @abstractmethod
    def describir(self):
        pass  # Cada clase hija DEBE definir cómo se describe a sí misma

    def __str__(self):
        return self.describir()  # Cuando hacemos print(objeto), llama a describir()


 #CLASE CLIENTE  

class Cliente(Entidad):
    _contador = 1  # Variable compartida entre todos los clientes para generar IDs únicos

    def __init__(self, nombre, email, telefono, edad):
        super().__init__(f"CLI-{Cliente._contador:03d}")  # Ej: CLI-001, CLI-002...
        Cliente._contador += 1

        # Usamos setters para validar cada dato al momento de asignarlo
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.edad = edad
        self._reservas = []  # Lista privada de reservas del cliente

    # Cada propiedad tiene un getter y un setter con validación

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, v):
        if not v or len(v.strip()) < 2:
            raise ErrorCliente("Nombre inválido: debe tener al menos 2 caracteres.")
        self._nombre = v.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, v):
        if not v or "@" not in v or "." not in v:
            raise ErrorCliente(f"Email inválido: '{v}'.")
        self._email = v.lower().strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, v):
        t = str(v).replace(" ", "").replace("-", "")
        if not t.isdigit() or not (7 <= len(t) <= 15):
            raise ErrorCliente("Teléfono inválido: solo dígitos, entre 7 y 15.")
        self._telefono = t

    @property
    def edad(self):
        return self._edad

    @edad.setter
    def edad(self, v):
        if not isinstance(v, int) or not (18 <= v <= 120):
            raise ErrorCliente("Edad inválida: debe ser un entero entre 18 y 120.")
        self._edad = v

    def agregar_reserva(self, reserva):
        self._reservas.append(reserva)  # Añade una reserva a la lista del cliente

    def describir(self):
        return (f"Cliente {self._id}: {self._nombre} | {self._email} | "
                f"Tel: {self._telefono} | Edad: {self._edad} | "
                f"Reservas: {len(self._reservas)}")


 #CLASE ABSTRACTA SERVICIO  

class Servicio(Entidad, ABC):
    _contador = 1

    def __init__(self, nombre, precio_hora, disponible=True):
        super().__init__(f"SRV-{Servicio._contador:03d}")
        Servicio._contador += 1
        self._nombre = nombre
        self._precio = precio_hora
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, v):
        self._disponible = bool(v)

    def verificar_disponibilidad(self):
        # Si el servicio está desactivado, lanza error
        if not self._disponible:
            raise ErrorServicio(f"Servicio '{self._nombre}' no disponible.")

    @abstractmethod
    def calcular_costo(self, horas, **kw):
        pass  # Cada servicio calcula su costo de forma diferente (polimorfismo)

    @abstractmethod
    def describir(self):
        pass


 #SERVICIOS ESPECIALIZADOS  
# Cada uno hereda de Servicio e implementa calcular_costo() a su manera

class Sala(Servicio):
    def __init__(self, nombre, precio_hora, capacidad, proyector=False):
        super().__init__(nombre, precio_hora)
        self._capacidad = capacidad
        self._proyector = proyector  # Si ya incluye proyector o no

    def calcular_costo(self, horas, **kw):
        # kw puede traer: personas, con_proyector, descuento, impuesto
        try:
            personas = kw.get("personas", 1)
            if personas > self._capacidad:
                raise ErrorReserva(f"Capacidad máxima: {self._capacidad}. Solicitadas: {personas}.")
            descuento = kw.get("descuento", 0)
            impuesto = kw.get("impuesto", 0.19)
            extra_proyector = 50000 if kw.get("con_proyector") and not self._proyector else 0
            subtotal = (self._precio * horas + extra_proyector) * (1 - descuento / 100)
            return round(subtotal * (1 + impuesto), 2)
        except ErrorReserva:
            raise
        except Exception as e:
            raise ErrorCosto(f"Error calculando costo de sala: {e}") from e

    def describir(self):
        return (f"Sala {self._id}: '{self._nombre}' | Cap: {self._capacidad} | "
                f"Proyector: {'Sí' if self._proyector else 'No'} | ${self._precio:,}/h")


class Equipo(Servicio):
    def __init__(self, nombre, precio_hora, tipo, stock):
        super().__init__(nombre, precio_hora)
        self._tipo = tipo
        self._stock = stock  # Cuántas unidades hay disponibles

    def calcular_costo(self, horas, **kw):
        try:
            cantidad = kw.get("cantidad", 1)
            if cantidad > self._stock:
                raise ErrorServicio(f"Stock insuficiente. Disponibles: {self._stock}.")
            seguro = kw.get("seguro", False)
            descuento = kw.get("descuento", 0)
            impuesto = kw.get("impuesto", 0.19)
            base = self._precio * horas * cantidad
            subtotal = (base + base * 0.1 * seguro) * (1 - descuento / 100)
            # Si hay seguro se agrega un 10% extra al costo base
            return round(subtotal * (1 + impuesto), 2)
        except ErrorServicio:
            raise
        except Exception as e:
            raise ErrorCosto(f"Error calculando costo de equipo: {e}") from e

    def describir(self):
        return (f"Equipo {self._id}: '{self._nombre}' | Tipo: {self._tipo} | "
                f"Stock: {self._stock} | ${self._precio:,}/h")


class Asesoria(Servicio):
    _niveles = {"junior": 1.0, "senior": 1.5, "experto": 2.0}
    # Los niveles definen cuánto se multiplica el precio base

    def __init__(self, nombre, precio_hora, area, nivel="junior"):
        super().__init__(nombre, precio_hora)
        self._area = area
        self._nivel = nivel

    def calcular_costo(self, horas, **kw):
        try:
            nivel = kw.get("nivel", self._nivel)
            if nivel not in self._niveles:
                raise ErrorCosto(f"Nivel '{nivel}' inválido. Use: {list(self._niveles)}")
            urgente = kw.get("urgente", False)
            descuento = kw.get("descuento", 0)
            impuesto = kw.get("impuesto", 0.19)
            base = self._precio * horas * self._niveles[nivel]
            subtotal = (base + base * 0.25 * urgente) * (1 - descuento / 100)
            # Si es urgente se cobra 25% adicional
            return round(subtotal * (1 + impuesto), 2)
        except ErrorCosto:
            raise
        except Exception as e:
            raise ErrorCosto(f"Error calculando costo de asesoría: {e}") from e

    def describir(self):
        return (f"Asesoría {self._id}: '{self._nombre}' | Área: {self._area} | "
                f"Nivel: {self._nivel} | ${self._precio:,}/h")


 #CLASE RESERVA  

class Reserva(Entidad):
    _contador = 1
    PENDIENTE, CONFIRMADA, CANCELADA, COMPLETADA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "COMPLETADA"

    def __init__(self, cliente, servicio, horas, **kw):
        super().__init__(f"RES-{Reserva._contador:03d}")
        Reserva._contador += 1

        # Validamos que los objetos y las horas sean correctos antes de guardar
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("Cliente inválido.")
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("Servicio inválido.")
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ErrorReserva("Las horas deben ser un número positivo.")

        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._kw = kw           # Parámetros opcionales para calcular el costo
        self._estado = self.PENDIENTE
        self._costo = None

    @property
    def estado(self):
        return self._estado

    @property
    def id_reserva(self):
        return self._id

    def confirmar(self):
        # Intenta confirmar la reserva validando disponibilidad y calculando costo
        try:
            if self._estado != self.PENDIENTE:
                raise ErrorReserva(f"No se puede confirmar en estado '{self._estado}'.")
            self._servicio.verificar_disponibilidad()
            self._costo = self._servicio.calcular_costo(self._horas, **self._kw)
            self._estado = self.CONFIRMADA
            self._cliente.agregar_reserva(self)
            log("INFO", f"{self._id} CONFIRMADA | {self._cliente._nombre} | "
                        f"{self._servicio.nombre} | {self._horas}h | ${self._costo:,}")
        except (ErrorReserva, ErrorServicio, ErrorCosto) as e:
            log("ERROR", f"Fallo confirmando {self._id}: {e}")
            raise

    def cancelar(self, motivo="Sin motivo"):
        try:
            if self._estado in (self.CANCELADA, self.COMPLETADA):
                raise ErrorReserva(f"No se puede cancelar en estado '{self._estado}'.")
            self._estado = self.CANCELADA
            log("AVISO", f"{self._id} CANCELADA | Motivo: {motivo}")
        except ErrorReserva as e:
            log("ERROR", f"Fallo cancelando {self._id}: {e}")
            raise

    def completar(self):
        try:
            if self._estado != self.CONFIRMADA:
                raise ErrorReserva(f"Solo se completan reservas confirmadas. Estado: {self._estado}")
            self._estado = self.COMPLETADA
            log("INFO", f"{self._id} COMPLETADA.")
        except ErrorReserva as e:
            log("ERROR", f"Fallo completando {self._id}: {e}")
            raise

    def describir(self):
        costo = f"${self._costo:,}" if self._costo else "pendiente"
        return (f"Reserva {self._id} | {self._estado} | "
                f"{self._cliente._nombre} | {self._servicio.nombre} | "
                f"{self._horas}h | {costo}")


 #GESTOR DEL SISTEMA  
# Clase principal que coordina todo: clientes, servicios y reservas

class SistemaFJ:
    def __init__(self):
        self._clientes = {}   # Diccionario id -> objeto cliente
        self._servicios = {}  # Diccionario id -> objeto servicio
        self._reservas = {}   # Diccionario id -> objeto reserva
        log("INFO", "Sistema Software FJ iniciado.")

    def registrar_cliente(self, nombre, email, telefono, edad):
        try:
            c = Cliente(nombre, email, telefono, edad)
        except ErrorCliente as e:
            log("ERROR", f"Cliente inválido ({nombre}): {e}")
            return None
        else:
            # El bloque else solo se ejecuta si NO hubo excepción en el try
            self._clientes[c.id] = c
            log("INFO", f"Registrado: {c.describir()}")
            return c
        finally:
            pass  # finally siempre se ejecuta; aquí no hay nada que cerrar

    def agregar_servicio(self, servicio):
        try:
            if not isinstance(servicio, Servicio):
                raise ErrorServicio("Objeto no es un servicio válido.")
            self._servicios[servicio.id] = servicio
            log("INFO", f"Servicio agregado: {servicio.describir()}")
        except ErrorServicio as e:
            log("ERROR", f"No se pudo agregar servicio: {e}")

    def crear_reserva(self, id_cliente, id_servicio, horas, **kw):
        try:
            c = self._clientes.get(id_cliente)
            s = self._servicios.get(id_servicio)
            if not c:
                raise ErrorReserva(f"Cliente '{id_cliente}' no encontrado.")
            if not s:
                raise ErrorReserva(f"Servicio '{id_servicio}' no encontrado.")
            r = Reserva(c, s, horas, **kw)
            r.confirmar()  # Puede lanzar excepciones propias
            self._reservas[r.id] = r
            return r
        except (ErrorReserva, ErrorServicio, ErrorCosto) as e:
            log("ERROR", f"Reserva fallida ({id_cliente}/{id_servicio}): {e}")
            return None

    def cancelar_reserva(self, id_reserva, motivo="Sin motivo"):
        try:
            r = self._reservas.get(id_reserva)
            if not r:
                raise ErrorReserva(f"Reserva '{id_reserva}' no encontrada.")
            r.cancelar(motivo)
        except (ErrorReserva, KeyError) as e:
            log("ERROR", f"No se pudo cancelar {id_reserva}: {e}")

    def completar_reserva(self, id_reserva):
        try:
            r = self._reservas.get(id_reserva)
            if not r:
                raise ErrorReserva(f"Reserva '{id_reserva}' no encontrada.")
            r.completar()
        except ErrorReserva as e:
            log("ERROR", f"No se pudo completar {id_reserva}: {e}")

    def resumen(self):
        estados = {}
        for r in self._reservas.values():
            estados[r.estado] = estados.get(r.estado, 0) + 1
        print(f"\n{'='*50}\nRESUMEN: {len(self._clientes)} clientes | "
              f"{len(self._servicios)} servicios | "
              f"{len(self._reservas)} reservas\nEstados: {estados}\n{'='*50}\n")


 #SIMULACIÓN DE LAS 10 OPERACIONES  

def simular():
    print("\n" + "="*50)
    print("       SIMULACIÓN SISTEMA SOFTWARE FJ")
    print("="*50)

    s = SistemaFJ()

    # Op 1: Clientes válidos
    print("\n-- Op 1: Clientes válidos --")
    c1 = s.registrar_cliente("Juan Pérez",   "juan@mail.com",   "3001234567", 30)
    c2 = s.registrar_cliente("María López",  "maria@mail.co",   "3119876543", 25)
    c3 = s.registrar_cliente("Carlos Ruiz",  "carlos@mail.com", "6014567890", 45)

    # Op 2: Clientes inválidos (el sistema no debe caerse)
    print("\n-- Op 2: Clientes inválidos --")
    s.registrar_cliente("", "ok@mail.com", "3001111111", 22)         # nombre vacío
    s.registrar_cliente("Pedro", "sin-arroba.com", "3002222222", 35) # email malo
    s.registrar_cliente("Ana",   "ana@ok.com", "123", 28)            # teléfono corto
    s.registrar_cliente("Luis",  "luis@ok.com", "3003333333", 15)    # menor de edad

    # Op 3: Servicios
    print("\n-- Op 3: Creando servicios --")
    sala_a  = Sala("Sala Ejecutiva",    80000,  capacidad=10, proyector=True)
    sala_b  = Sala("Sala Conferencias", 120000, capacidad=30, proyector=False)
    laptop  = Equipo("Laptop HP",       25000,  "Laptop",    stock=5)
    camara  = Equipo("Cámara Sony",     40000,  "Cámara",   stock=2)
    legal   = Asesoria("Asesoría Legal",150000, "Legal",     nivel="senior")
    ti      = Asesoria("Asesoría TI",   100000, "Tecnología",nivel="experto")

    for srv in (sala_a, sala_b, laptop, camara, legal, ti):
        s.agregar_servicio(srv)

    # Op 4: Reservas válidas
    print("\n-- Op 4: Reservas válidas --")
    r1 = s.crear_reserva(c1.id, sala_a.id, 3, personas=8, descuento=10)
    r2 = s.crear_reserva(c2.id, laptop.id, 4, cantidad=2, seguro=True)
    r3 = s.crear_reserva(c3.id, legal.id,  2, urgente=True)

    # Op 5: Reservas inválidas
    print("\n-- Op 5: Reservas inválidas --")
    s.crear_reserva(c1.id, sala_a.id, 2, personas=20) # excede capacidad
    s.crear_reserva("CLI-999", sala_b.id, 2)          # cliente no existe
    s.crear_reserva(c2.id, "SRV-999", 2)              # servicio no existe
    s.crear_reserva(c3.id, camara.id, -1)             # horas negativas

    # Op 6: Servicio desactivado
    print("\n-- Op 6: Servicio desactivado --")
    ti.disponible = False
    s.crear_reserva(c1.id, ti.id, 3)  # falla porque está desactivado
    ti.disponible = True

    # Op 7: Completar reserva válida
    print("\n-- Op 7: Completar reserva --")
    if r1:
        s.completar_reserva(r1.id)

    # Op 8: Cancelar reserva
    print("\n-- Op 8: Cancelar reserva --")
    if r2:
        s.cancelar_reserva(r2.id, "El cliente cambió de planes")

    # Op 9: Cancelar lo que ya está cancelado (debe fallar)
    print("\n-- Op 9: Doble cancelación --")
    if r2:
        s.cancelar_reserva(r2.id, "Segundo intento")

    # Op 10: Completar reserva cancelada (debe fallar)
    print("\n-- Op 10: Completar cancelada --")
    if r2:
        s.completar_reserva(r2.id)

    s.resumen()

    # Mostramos todos los logs guardados en memoria
    print("\n  REGISTRO DE EVENTOS EN MEMORIA  ")
    for entrada in registro_logs:
        print(entrada)


if __name__ == "__main__":
    simular()

