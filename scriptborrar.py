import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Creación de la tabla si no existe
cursor.execute('''
   DELETE FROM weather_data
    
''')

# Confirmar y cerrar la conexión
conn.commit()
conn.close()