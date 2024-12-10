import configparser

class ConfigINI():
    def __init__(self, file):
        self._file = file
        self.config = configparser.ConfigParser()
        self.config.read(self._file)

    def save(self):
        with open(self._file, 'w') as out:
            self.config.write(out)

    def get(self, block, key, default=None):
        try:
            return(self.config.get(block, key))
        except:
            if default != None:
                self.set(block, key, default)
            return default       
    
    def set(self, block, key, value):
        if self.config.has_section(block): pass
        else: self.config.add_section(block)
        self.config.set(block, key, value)