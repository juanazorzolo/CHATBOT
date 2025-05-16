from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)

# Estado de cada usuario
usuarios = {}

# Cargar respuestas desde el archivo JSON
with open("respuestas.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

menu = datos["menu"]
respuestas = datos["respuestas"]
marcas = datos["marcas_disponibles"]

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    phone = request.values.get('From', '')
    msg = request.values.get('Body', '').strip().lower()
    response = MessagingResponse()

    estado = usuarios.get(phone, {"estado": "inicio"})

    if estado["estado"] == "inicio":
        mensaje = menu
        estado["estado"] = "esperando_opcion"

    elif estado["estado"] == "esperando_opcion":
        if msg in ['1', '2', '3']:
            mensaje = respuestas[msg]
            mensaje += f"\n\n{respuestas['otra_consulta']}"
            estado["estado"] = "otra_consulta"
        elif msg == '4':
            mensaje = respuestas["marca_prompt"]
            estado["estado"] = "marca"
        else:
            mensaje = "❌ Opción no válida. Por favor elegí una opción del menú:\n" + menu

    elif estado["estado"] == "otra_consulta":
        if msg in ['si', 'sí']:
            mensaje = menu
            estado["estado"] = "esperando_opcion"
        elif msg == 'no':
            mensaje = respuestas["despedida"]
            estado["estado"] = "finalizado"
        else:
            mensaje = "❓ Por favor respondé con *sí* o *no*."

    elif estado["estado"] == "marca":
        if msg.capitalize() in marcas:
            estado["marca"] = msg.capitalize()
            mensaje = respuestas["modelo_prompt"]
            estado["estado"] = "modelo"
        else:
            mensaje = "❌ Marca no válida. Ingresá una marca válida (Ej: Toyota, Nissan)."

    elif estado["estado"] == "modelo":
        estado["modelo"] = msg
        mensaje = f"📋 Marca: *{estado['marca']}*, Modelo: *{estado['modelo']}*\n"
        mensaje += respuestas["consulta_derivada"]
        mensaje += f"\n\n{respuestas['otra_consulta']}"
        estado["estado"] = "otra_consulta"

    elif estado["estado"] == "finalizado":
        if msg in ['hola', 'inicio', 'empezar']:
            mensaje = "🔁 Reiniciando conversación...\n" + menu
            estado = {"estado": "esperando_opcion"}
        else:
            mensaje = "🙌 Gracias por tu consulta. Si querés empezar de nuevo, escribí *hola*."

    usuarios[phone] = estado
    response.message(mensaje)
    print(f"Mensaje recibido: {msg}")
    print(f"Estado actual: {estado}")
    print(f"Mensaje de respuesta: {mensaje}")
    return str(response)

if __name__ == "__main__":
    app.run(port=5000)