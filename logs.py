#Importacion del módulo logging
#para registrar automáticamente como informacion y errores en un archivo de texto llamado logs.txt
import logging

logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
