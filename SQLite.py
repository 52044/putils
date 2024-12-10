import sqlite3

try:
    from .Logger import Logger 
except ImportError:
    from Logger import Logger
class SQLite:
    def __init__(self, path: str, log_name="sqlite", ):
        """Class for SQLite interaction
        :param path: Path to the desired SQLite file
        :type path: str
        """
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def __enter__(self):
        """Enter the runtime context for the object."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context, ensuring the connection is closed."""
        self.Close()

    def Command(self, cmd: str, params=None):
        """Execute a command with optional parameters."""
        try:
            self.cursor.execute(cmd, params or ())
        except sqlite3.Error as e:
            print(f"SQLite Error: {e}")  # Replace with proper logging

    def Insert(self, table: str, values: dict):
        """Insert a row into a table."""
        columns = ', '.join(f'"{k}"' for k in values.keys())
        placeholders = ', '.join(['?'] * len(values))
        cmd = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.Command(cmd, tuple(values.values()))

    def FindRow(self, table: str, column: str, value):
        """Find a row by column and value."""
        cmd = f"SELECT * FROM {table} WHERE {column} = ?"
        self.Command(cmd, (value,))
        return self.cursor.fetchone()

    def Delete(self, table: str, column: str, value):
        """Delete rows matching a condition."""
        cmd = f"DELETE FROM {table} WHERE {column} = ?"
        self.Command(cmd, (value,))

    def Commit(self):
        """Commits the current transaction."""
        try:
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Commit Error: {e}")  # Replace with proper logging

    def Close(self):
        """Closes the database connection."""
        try:
            self.connection.close()

        except sqlite3.Error as e:
            print(f"Close Error: {e}")  # Replace with proper logging
