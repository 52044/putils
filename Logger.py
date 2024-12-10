import logging
from logging.handlers import RotatingFileHandler

class Logger:
    __default__ = {
        'level': 2,
        'file': None, 
        'file_level': 2,
        'file_size': 10**6,
        'file_backups': 3,
    }

    def __init__(self, name, **kwargs):
        """Initialaze new logger. The logger level is indicated by a number, where 1 - debug and 5 - error.

        :param name: Logger name (usually module or class name).
        :type name: str
        :param level: Level of logger
        :type level: int (1 - 5) / str
        :param file: Optional path to the log file.
        :type file: str / None
        """
        cfg = {**Logger.__default__, **kwargs}

        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.__get_level__(1))
        
        cmd_handler = logging.StreamHandler()
        cmd_handler.setLevel(self.__get_level__(cfg['level']))
        cmd_handler.setFormatter(logging.Formatter(f'%(asctime)s - {name} - %(levelname)s - %(message)s'))
        self.logger.addHandler(cmd_handler)

        if cfg['file']:
            file_handler = RotatingFileHandler(cfg['file'], maxBytes=cfg['file_size'], backupCount=cfg['file_backups'])
            file_handler.setLevel(self.__get_level__(cfg['file_level']))
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(file_handler)
    
    def __get_level__(self, level):
        if isinstance(level, str): level = level.lower()
        levels = {
            1: logging.DEBUG,   'debug': logging.DEBUG,
            2: logging.INFO,    'info': logging.INFO,
            3: logging.WARNING, 'warning': logging.WARNING, 'warn': logging.WARNING,
            4: logging.ERROR,   'error': logging.ERROR, 'err': logging.ERROR,
            5: logging.CRITICAL,'critical': logging.CRITICAL, 'crit': logging.CRITICAL
        }
        if level not in levels:
            raise ValueError(f"Invalid logging level: '{level}'. Use 1-5 or debug/info/warning/error/critical.")
        return levels[level]
    
    def log(self, level, message):
        """Send new message
        
        :param level: Level of message
        :type level: int (1 - 5)
        :param message: Text information
        :type message: str
        """
        self.logger.log(self.__get_level__(level), message)