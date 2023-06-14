import os
import logging


def logs():
    logs_dir = '../logs'
    log_file = 'archivo.log'

    # Verificar si la carpeta de logs existe, de lo contrario, crearla
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Ruta completa del archivo de logs
    log_path = os.path.join(logs_dir, log_file)

    logging.basicConfig(filename=log_path, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Registros
    logging.debug('Este es un mensaje de depuración')
    logging.info('Esta es una información general')
    logging.warning('Este es un mensaje de advertencia')
    logging.error('Este es un mensaje de error')
    logging.critical('Este es un mensaje crítico')


logs()
