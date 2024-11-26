from flask import Flask, request, render_template

app = Flask(__name__)

# Función para verificar restricciones de "Hoy no circula"
def hoy_no_circula(placa, dia):
    restricciones = {
        "lunes": [1, 2],
        "martes": [3, 4],
        "miércoles": [5, 6],
        "jueves": [7, 8],
        "viernes": [9, 0]
    }
    try:
        # Extraer el último dígito de la placa
        ultimo_digito = int(placa[-1])
        # Verificar si el día es válido y el último dígito está restringido
        if dia in restricciones:
            return ultimo_digito in restricciones[dia]
        else:
            return None  # Día no válido
    except (ValueError, IndexError):
        return None  # Placa inválida (no termina en un número)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verificar_hoy_no_circula', methods=['POST'])
def verificar_hoy_no_circula():
    # Obtener los datos del formulario
    placa = request.form.get('placa')
    dia = request.form.get('dia').lower()  # Convertir el día a minúsculas para evitar errores

    if not placa or not dia:
        return "Por favor, proporciona la placa y el día para verificar."

    try:
        # Extraer el último dígito de la placa
        ultimo_digito = int(placa[-1])

        # Verificar si el último dígito está restringido para el día seleccionado
        if dia in hoy_no_circula:
            if ultimo_digito in hoy_no_circula[dia]:
                return f"La placa {placa} **NO** puede circular el día {dia.capitalize()}."
            else:
                return f"La placa {placa} **SÍ** puede circular el día {dia.capitalize()}."
        else:
            return "El día seleccionado no es válido. Por favor, elige un día entre lunes y viernes."
    except ValueError:
        return "Por favor, proporciona una placa válida (que termine en un dígito)."

if __name__ == '__main__':
    app.run(debug=True)