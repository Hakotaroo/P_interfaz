from flask import Flask, request, render_template
import re

app = Flask(__name__)

def validar_placa(placa):
    return re.fullmatch(r'[A-Za-z]{3}\d{1,4}', placa) is not None

def hoy_no_circula(placa, dia):
    restricciones = {
        "lunes": [1, 2],
        "martes": [3, 4],
        "miércoles": [5, 6],
        "jueves": [7, 8],
        "viernes": [9, 0]
    }
    try:
        ultimo_digito = int(placa[-1])
        return dia in restricciones and ultimo_digito in restricciones[dia]
    except (ValueError, IndexError):
        return None

@app.route('/')
def index():
    return render_template('index.html', message=None)

@app.route('/verificar_hoy_no_circula', methods=['POST'])
def verificar_hoy_no_circula():
    placa = request.form.get('placa')
    dia = request.form.get('dia').lower()

    if not placa or not dia:
        message = "Por favor, proporciona ambos: una placa válida y un día."
    elif not validar_placa(placa):
        message = "Por favor, introduce una placa válida (ejemplo: ABC1234)."
    else:
        resultado = hoy_no_circula(placa, dia)
        if resultado is None:
            message = "El día ingresado no es válido o la placa no termina en un número."
        elif resultado:
            message = f"La placa {placa} <strong>NO</strong> puede circular el día {dia.capitalize()}."
        else:
            message = f"La placa {placa} <strong>SÍ</strong> puede circular el día {dia.capitalize()}."

    return render_template('index.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)

