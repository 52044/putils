import sqlite3

try:
    from .Logger import Logger 
except ImportError:
    from Logger import Logger
class SQLite:
    def __init__(self, path: str, index='id', log_lvl='warn'):
        self.logger = Logger('SQLite', log_lvl)
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.Index = index

    def Command(self, cmd:str):
        self.cursor.execute(cmd)

    def Insert(self, table:str, values: dict):   
        data = {f'"{k}"': f'"{v}"' if v is not None else "NULL" for k, v in values.items()}

        cmd = f"INSERT INTO {table} ({', '.join(data.keys())}) VALUES ({', '.join(map(str, data.values()))})"
        self.cursor.execute(cmd)
        self.logger.log('info', f"Data sucsessfuly inserted: {data}")

    def Update(self, table:str, row_id: int, values: dict):
        data = {f'"{k}"': f'"{v}"' if v is not None else "NULL" for k, v in values.items()}
        if self.IsIdExist(table, row_id):
            cmd = f"UPDATE {table} SET {', '.join([f'{key} = {val}' for key, val in data.items()])} WHERE {self.Index} = {row_id}"
        else:
            cmd = f"INSERT INTO {table} ({self.Index}, {', '.join(data.keys())}) VALUES ({row_id}, {', '.join(map(str, data.values()))})"
        self.cursor.execute(cmd)
        self.logger.log('info', f"Data sucsessfuly updated: {data}")

    def IsIdExist(self, table:str, id_row:int) -> bool:
        cmd = f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {self.Index} = {id_row})"
        self.cursor.execute(cmd)
        return self.cursor.fetchone()[0] == 1

    def CallTable(self, table:str, values:list):
         self.cursor.execute(f"SELECT {', '.join(values)} FROM {table}")
         return self.cursor.fetchall()

    def Delete(self, table:str, id_row:int):
        cmd = f"DELETE FROM {table} WHERE {self.Index} = {id_row}"
        self.cursor.execute(cmd)
        self.logger.log('info', f"Data sucsessfuly deleted @{self.Index} = {id_row}")

    def Commit(self):
        """Commits the current transaction."""
        self.connection.commit()
        self.logger.log('info', "Database changes committed.")

    def Close(self):
        """Closes the database connection."""
        self.connection.close()