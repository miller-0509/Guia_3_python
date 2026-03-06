from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Bienvenido a mi primera aplicación Flask"

@app.route("/saludo")
def saludo():
    return "Hola, esta es otra página en Flask"

@app.route("/usuario/<nombre>")
def usuario(nombre):
    return f"Hola {nombre}, bienvenido a Flask"

@app.route("/suma/<int:a>/<int:b>")
def suma(a, b):
    resultado = a + b
    return f"La suma es {resultado}"

if __name__ == "__main__":
    app.run(debug=True)