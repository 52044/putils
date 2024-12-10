import logging

class Logger:
    def __init__(self, obj, level=2):
        """Initialaze new logger. The logger level is indicated by a number, where 1 - debug and 5 - error.

        :param level: Level of logger
        :type level: int (1 - 5) / str
        """
        self.logger = logging.getLogger(obj)
        self.logger.setLevel(self.__get_level__(level))
        
        self.handle = logging.StreamHandler()
        self.handle.setFormatter(logging.Formatter(f'%(asctime)s - {obj} - %(levelname)s - %(message)s'))
        self.logger.addHandler(self.handle)
    
    def __get_level__(self, level):
        if isinstance(level, str): level = level.lower()
        match level:
            case 1:         return logging.DEBUG
            case 'debug':   return logging.DEBUG
            case 2:         return logging.INFO
            case 'info':    return logging.INFO
            case 3:         return logging.WARNING
            case 'warning': return logging.WARNING
            case 'warn':    return logging.WARNING
            case 4:         return logging.ERROR
            case 'error':   return logging.ERROR
            case 5:         return logging.CRITICAL
            case 'critical':return logging.CRITICAL
            case _: raise ValueError(f"Logging level is incorrect - \"{level}\". Try 1 (debug) / 2 (info) / 3 (warning) / 4 (error) or 5 (critical)")

    def log(self, level, message):
        """Send new message
        
        :param level: Level of message
        :type level: int (1 - 5)
        :param message: Text information
        :type message: str
        """
        self.logger.log(self.__get_level__(level), message)