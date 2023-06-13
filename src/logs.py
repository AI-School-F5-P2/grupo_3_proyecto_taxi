import logging


def logs():
    logging.basicConfig(filename='../logs/archivo.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

    # registros
    logging.debug('Este es un mensaje de depuración')
    logging.info('Esta es una información general')
    logging.warning('Este es un mensaje de advertencia')
    logging.error('Este es un mensaje de error')
    logging.critical('Este es un mensaje crítico')
