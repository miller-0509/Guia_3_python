from flask import Flask

app = Flask(__name__)

@app.route('/api/temperatura/<float:grados_c>')
def convertir_temperatura(grados_c: float):
    grados_f = (grados_c * 9/5) + 32
    return (
        f"{grados_c}°C equivale a {grados_f}°F"
    )

if __name__ == '__main__':
    app.run(debug=True)
