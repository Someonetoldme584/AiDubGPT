import logging

def configure_logging():
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def log_messages():
    logging.debug('Debug mesajı: Bu mesaj programın çalışmasında herhangi bir problem olmadığını belirtir.')
    logging.info('Info mesajı: Genel bilgi mesajıdır.')
    logging.warning('Warning mesajı: Programın çalışmasını durdurmayacak bir uyarıdır.')
    logging.error('Error mesajı: Programın çalışmasını etkileyen bir hatadır.')
    logging.critical('Critical mesajı: Programın çalışmasını durduran kritik bir hatadır.')
