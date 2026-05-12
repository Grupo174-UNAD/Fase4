from clientes import Cliente

try:
    print("Empresa Software FJ\n")
    print("Cliente")
    
    nombre = input("Nombre: ")
    correo = input("Correo: ")
    
    cliente = Cliente(nombre, correo)
    
    print("Cliente creado")
    print(cliente.mostrar_info())
    
except Exception as e:
    print(f"Error: {e}")
    