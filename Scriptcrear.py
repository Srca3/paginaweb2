import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Configurar la zona horaria a local
cursor.execute('PRAGMA foreign_keys=OFF;')
cursor.execute('PRAGMA timezone=LOCAL;')

# Creación de la tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        lluvia REAL,
        radiacion_uv REAL,
        temperatura REAL,
        humedad REAL
    )
''')

# Confirmar y cerrar la conexión
conn.commit()
conn.close()
