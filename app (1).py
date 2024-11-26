from flask import Flask, render_template, request, flash, redirect, url_for
from hoy_no_circula import hoy_no_circula
from database import Database  # Asegúrate de tener esta clase

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesario para usar flash

@app.route("/", methods=["GET", "POST"])
def index():
    dia = ""
    if request.method == "POST":
        placa = request.form.get("placa")
        if placa:
            dia = hoy_no_circula(placa)  # Llamamos a la función que determinamos en hoy_no_circula.py
    return render_template("index.html", dia=dia)

@app.route("/registro_cita", methods=["GET", "POST"])
def registro_cita():
    return render_template("registro_cita.html")

@app.route('/hoy_no_circula')
def hoy_no_circula_view():
    return render_template('hoy_no_circula.html')  # o la plantilla que estés usando

@app.route('/verificar_hoy_no_circula', methods=['POST'])
def verificar_hoy_no_circula():
    placa = request.form.get('placa')
    dia = request.form.get('dia').lower()

    if not placa or not dia:
        return "Por favor, proporciona la placa y el día para verificar."

    resultado = hoy_no_circula(placa, dia)

    if resultado is None:
        return "El día seleccionado no es válido o la placa proporcionada no es válida."
    elif resultado:
        return f"La placa {placa} **NO** puede circular el día {dia.capitalize()}."
    else:
        return f"La placa {placa} **SÍ** puede circular el día {dia.capitalize()}."

@app.route('/registrar_cita', methods=['POST'])
def registrar_cita():
    placa = request.form['placa']
    confirm_placa = request.form['confirm_placa']
    serie = request.form['serie']
    confirm_serie = request.form['confirm_serie']
    modelo = request.form['modelo']
    correo_electronico = request.form['correo_electronico']

    db = Database()
    db.insert_data(placa, confirm_placa, serie, confirm_serie, modelo, correo_electronico)

    flash('Cita registrada exitosamente.', 'success')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
