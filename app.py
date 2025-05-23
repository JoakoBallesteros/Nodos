from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)
DATA_FILE = 'data/reportes.csv'

@app.route('/reporte', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        datos = {
            "usuario": request.form['usuario'],
            "sn_equipo": request.form['sn_equipo'],
            "mac_equipo": request.form['mac_equipo'],
            "nodo": request.form['nodo'],
            "region": request.form['region'],
            "ip": request.form['ip'],
            "dni": request.form['dni'],
            "contacto": request.form['contacto'],
            "servicio": request.form['servicio'],
            "inconveniente": request.form['inconveniente'],
            "direccion": request.form['direccion']
        }

        guardar_datos(datos)
        return redirect('/gracias')

    return render_template("formulario.html")

@app.route('/gracias')
def gracias():
    return render_template("gracias.html")

from collections import Counter

from collections import defaultdict, Counter

@app.route('/admin')
def ver_reportes():
    reportes_por_nodo = defaultdict(list)
    conteo_nodos = Counter()

    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                nodo = row["nodo"]
                reportes_por_nodo[nodo].append(row)
                conteo_nodos[nodo] += 1

    return render_template('admin.html', reportes_por_nodo=reportes_por_nodo, conteo_nodos=conteo_nodos)



def guardar_datos(data):
    os.makedirs('data', exist_ok=True)
    archivo_existe = os.path.isfile(DATA_FILE)
    with open(DATA_FILE, 'a', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=data.keys())
        if not archivo_existe:
            writer.writeheader()
        writer.writerow(data)

if __name__ == '__main__':
    app.run(debug=True)
