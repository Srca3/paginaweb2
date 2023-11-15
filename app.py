from flask import Flask, render_template, jsonify, request, Response
import sqlite3
import serial
import time
import random
from threading import Thread
import csv
import pandas as pd
from io import BytesIO


app = Flask(__name__)
#try:
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
#except:
#    ser = None
db_path = 'data.db'

# Función para crear la tabla en la base de datos
def fetch_all_records():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM weather_data')
    data = cursor.fetchall()

    conn.close()

    return data
def generate_csv():
    data = fetch_all_records()
    df = pd.DataFrame(data, columns=['id', 'timestamp', 'lluvia', 'radiacion_uv', 'temperatura', 'humedad'])
    csv_output = BytesIO()
    df.to_csv(csv_output, index=False)
    csv_output.seek(0)
    return csv_output

def generate_excel():
    data = fetch_all_records()
    df = pd.DataFrame(data, columns=['id', 'timestamp', 'lluvia', 'radiacion_uv', 'temperatura', 'humedad'])
    excel_output = BytesIO()
    df.to_excel(excel_output, index=False, sheet_name='Datos Meteorológicos')
    excel_output.seek(0)
    return excel_output



def fetch_all_records():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM weather_data')
    data = cursor.fetchall()

    conn.close()

    return data
    
def start_serial_reading():
    serial_thread = Thread(target=read_serial_and_write_to_db)
    serial_thread.daemon = True
    serial_thread.start()

def read_serial_and_write_to_db():

    while True:
        try:
    #        if ser:
            
            data = ser.readline().decode('utf-8').strip()
    #        else:
    #            data =f"PL:{random.uniform(0, 5):.2f},UV:{random.uniform(0, 10):.2f},TE:{random.uniform(20, 30):.2f},HU:{random.uniform(40, 60):.2f}"
            
            data_parts = data.split(',')
            print(data)
            data_dict = {}
            for part in data_parts:
                # Verifica si la parte tiene un ':'
                if ':' in part:
                    key, value = part.split(':')
                    data_dict[key.lower()] = float(value)
                else:
                    # Puedes manejar el caso en el que la parte no tiene ':', según tus necesidades
                    print(f"Error: La parte '{part}' no tiene el formato esperado.")

            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO weather_data (lluvia, radiacion_uv, temperatura, humedad)
                VALUES (?, ?, ?, ?)
            ''', (data_dict['pl'], data_dict['uv'], data_dict['te'], data_dict['hu']))
            conn.commit()
            conn.close()
        except:
            print("Error al recibir datos")
            pass
  # Ajusta según la frecuencia de los datos del puerto serial

def fetch_last_10_records():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 1')
    data = cursor.fetchall()

    conn.close()
    return data

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data')
def get_data():
    data = fetch_last_10_records()
    return jsonify(data)

@app.route('/acerca')
def about():
    return render_template('acerca.html')

@app.route('/contacto')
def contact():
    return render_template('contacto.html')

@app.route('/mediciones')
def real_time():
    return render_template('mediciones.html')
 
@app.route('/descargas')
def descargas():
    return render_template('descargas.html')


@app.route('/descargas/csv')
def download_csv():
    csv_output = generate_csv()
    return Response(
        csv_output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=weather_data.csv'}
    )

@app.route('/descargas/excel')
def download_excel():
    excel_output = generate_excel()
    return Response(
        excel_output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment;filename=weather_data.xlsx'}
    )



if __name__ == '__main__':
    start_serial_reading()
    app.run(host='0.0.0.0', port=5000)
