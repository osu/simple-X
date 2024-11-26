# db.py (for connection of database)
import sqlite3
import os.path
from tkinter import messagebox
import sys
from exceptions import NonexistentDatabaseException

def connect_db():
    """
    Connects to the SQLite database provided as a command-line argument.
    Enables foreign key support and attempts to load the regexp extension.
    Raises:
        NonexistentDatabaseException: If the database file does not exist.
        sqlite3.Error: If there's an error connecting to the database.
    Returns:
        sqlite3.Connection: The database connection object.
    """
    if len(sys.argv) != 2:
        messagebox.showerror("Error", "Usage: python main.py database.db")
        sys.exit(1)

    db_name = sys.argv[1]
    try:
        if not os.path.isfile(db_name):
            raise NonexistentDatabaseException(invalid_path=db_name)
        conn = sqlite3.connect(db_name)
        conn.enable_load_extension(True)
        conn.execute("PRAGMA foreign_keys = ON;")
        
        # Cross-platform handling for loading `regexp` extension
        import platform
        system = platform.system()
        try:
            if system == "Darwin":
                conn.load_extension("./regexp.dylib")
            elif system == "Linux":
                conn.load_extension("./regexp.so")
            elif system == "Windows":
                conn.load_extension("./regexp.dll")
        except sqlite3.OperationalError as e:
            print(f"Optional: Could not load regexp extension: {e}")
        
        return conn
    except NonexistentDatabaseException as e:
        messagebox.showerror("Database Error", f"Database does not exist: {e}")
        sys.exit(1)
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error connecting to database: {e}")
        sys.exit(1)

