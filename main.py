#Importamos los otros archivos
#Este funciona como "archivo" para comprobar y ejecutar el programa principal

from clientes import Cliente
from servicios import ReservaSalas, AlquilerEquipos, AsesoriaEspecializada
#Importar logs para los registros de información y errores
import logs
import logging
#Listas para almacenar clientes y servicios registrados
clientes = []
servicios = []
#Bloque try-except para manejar errores y registrar información en logs
try:
#Intro del sistema y registro del cliente
    print("\nEmpresa Software FJ\n")
    print("Ingrese su nombre y correo para registrarse como cliente")
    
    nombre = input("Nombre: ")
    correo = input("Correo: ")
    
    cliente = Cliente(nombre, correo)
    clientes.append(cliente)
#Mostrar la información del cliente registrado y registrar el evento en logs
    print(f"Registrado exitosamente: {cliente.mostrar_info()}")
    logging.info(f"Cliente registrado: {cliente.mostrar_info()}")
#Mostrar opciones de servicios
    print(f"\nBienvenido {cliente.get_nombre()} por favor seleccione el servicio que desea")
    print("\nServicios")
    print("1. Reservar Sala")
    print("2. Alquiler de Equipos") 
    print("3. Asesoría Especializada")
#Solicitar al cliente que seleccione un servicio
    opcion = input("Seleccione un servicio (1-3): ")
    if opcion == "1":
        print("\nSalas disponibles")
        print("1. Sala de reuniones (Capacidad: 10 personas)")
        print("2. Sala audiovisual (Capacidad: 20 personas)")
        print("3. Sala privada (Capacidad: 30 personas)")
        sala = input("Seleccione una sala (1-3): ")
        if sala == "1":
#Mostrar la información del servicio seleccionado como: capacidad y precio, y registrar el evento en logs
            servicio = ReservaSalas("Sala de reuniones", 10, 1000)
            logging.info(f"Servicio seleccionado: {servicio.mostrar_info()}")
        elif sala == "2":
            servicio = ReservaSalas("Sala audiovisual", 20, 2000)
            logging.info(f"Servicio seleccionado: {servicio.mostrar_info()}")  
        elif sala == "3":
            servicio = ReservaSalas("Sala privada", 30, 3000)
            logging.info(f"Servicio seleccionado: {servicio.mostrar_info()}")
        else:
            raise ValueError("Opción no válida.")
        
        print(f"\n{servicio.mostrar_info()}")
        servicios.append(servicio)
#Solicitar al cliente la cantidad de horas en numero entero que desea reservar la sala
#Multiplicar el precio del servicio por la cantidad de horas y mostrar el total a pagar por la reserva
        horas = int(input("\nCuantas horas desea reservar en la sala?: "))
        total = servicio.precio * horas
        print(f"Total a pagar por la reserva: ${total}")
        logging.info(f"servicio reservado: {servicio.nombre}")
        logging.info(f"Total a pagar por la reserva: ${total}")
#Servicio de alquiler de equipos
    elif opcion == "2":
        print("\nEquipos disponibles")
        print("1. Proyector")
        print("2. Laptop")
        print("3. Auriculares")
        equipo = input("Seleccione un equipo (1-3): ")
        if equipo == "1":
            servicio = AlquilerEquipos("Proyector", 500)
            logging.info(f"Servicio seleccionado: {servicio.mostrar_info()}")
        elif equipo == "2":
            servicio = AlquilerEquipos("Laptop", 800)
            logging.info(f"Servicio seleccionado: {servicio.mostrar_info()}") 
        elif equipo == "3":
            servicio = AlquilerEquipos("Auriculares", 200)
            logging.info(f"Servicio seleccionado: {servicio.mostrar_info()}")
        else:
            raise ValueError("Opción no válida.")
        
        print(f"\n: {servicio.mostrar_info()}")
        servicios.append(servicio)
#Solicitar al cliente la cantidad de días en numero entero que desea alquilar el equipo
#Multiplicar el precio del servicio por la cantidad de días y mostrar el total a pagar por el alquiler del equipo
        dias = int(input("\nCuantos días desea alquilar el equipo?: "))
        total = servicio.precio * dias
        print(f"Total a pagar por el alquiler: ${total}")
        logging.info(f"servicio reservado: {servicio.nombre}")
        logging.info(f"Total a pagar por el alquiler: ${total}")
#Servicio de asesoría especializada
    elif opcion == "3":
        print("\nAsesoría Especializada")
        print("1. Soporte técnico")
        print("2. Consulta a un asesor")
        area = input("Seleccione un área de asesoría (1 o 2): ")
#Mostrar el costo por el servicio especializado
        if area == "1":
            servicio = AsesoriaEspecializada("Soporte técnico", 1500)
            logging.info(f"Servicio seleccionado: {servicio.mostrar_info()}")
        elif area == "2":
            servicio = AsesoriaEspecializada("Consulta con un asesor", 1000)
            logging.info(f"Servicio seleccionado: {servicio.mostrar_info()}")
        else:
            raise ValueError("Opción no válida.")
            
        print(f"\n {servicio.mostrar_info()}")
        servicios.append(servicio)
        
except Exception as e:
    print(f"Error: {e}")
    logging.error(e)

