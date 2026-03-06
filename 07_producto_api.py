import os
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

class Producto:
    def __init__(self, id: int, nombre: str, precio: float, stock: int):
        self.__id = id
        self.__nombre = nombre
        self.__precio = precio
        self.__stock = stock

    def aplicar_descuento(self, porcentaje: float) -> None:
        """Reduce el precio según el porcentaje dado."""
        if 0 < porcentaje < 100:
            self.__precio = round(self.__precio * (1 - porcentaje / 100), 2)

    def reducir_stock(self, cantidad: int) -> bool:
        """Reduce el stock si hay suficiente disponible. Retorna True si tuvo éxito."""
        if cantidad <= self.__stock:
            self.__stock -= cantidad
            return True
        return False

    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "nombre": self.__nombre,
            "precio": self.__precio,
            "stock": self.__stock
        }

productos_db: list[Producto] = [
    Producto(1, "Laptop Pro", 1200.00, 10),
    Producto(2, "Mouse Inalámbrico", 25.99, 50),
    Producto(3, "Teclado Mecánico", 89.99, 30),
]

@app.route('/api/productos', methods=['GET'])
def obtener_productos() -> tuple[Response, int]:
    data = [p.to_dict() for p in productos_db]
    return jsonify({
        "total_registros": len(data),
        "data": data
    }), 200

@app.route('/api/productos/<int:id_producto>', methods=['GET'])
def obtener_producto(id_producto: int) -> tuple[Response, int]:
    for producto in productos_db:
        if producto.to_dict()["id"] == id_producto:
            return jsonify(producto.to_dict()), 200
    return jsonify({"error": "Producto no encontrado"}), 404

@app.route('/api/productos', methods=['POST'])
def crear_producto() -> tuple[Response, int]:
    datos: dict = request.get_json()

    if not datos or "nombre" not in datos or "precio" not in datos:
        return jsonify({"error": "Faltan campos requeridos: 'nombre' y 'precio'"}), 400

    nuevo_id = len(productos_db) + 1
    nuevo_producto = Producto(
        id=nuevo_id,
        nombre=datos["nombre"],
        precio=float(datos["precio"]),
        stock=int(datos.get("stock", 0))
    )
    productos_db.append(nuevo_producto)

    return jsonify({
        "mensaje": "Producto creado exitosamente",
        "data": nuevo_producto.to_dict()
    }), 201

if __name__ == '__main__':
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
