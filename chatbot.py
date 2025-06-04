from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json

app = Flask(__name__)

usuarios = {}

with open("respuestas.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

menu = datos["menu"]
respuestas = datos["respuestas"]
marcas = datos["marcas_disponibles"]

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    phone = request.values.get('From', '')
    msg_original = request.values.get('Body')

    # Evitamos errores si el cuerpo del mensaje es None
    if msg_original is None:
        msg_original = ''
    else:
        msg_original = msg_original.strip()

    msg = msg_original.lower()
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
        try:
            indice = int(msg) - 1
            if 0 <= indice < len(marcas):
                estado["marca"] = marcas[indice]
                mensaje = f"✅ Elegiste la marca *{estado['marca']}*. ¿Deseás volver a elegir otra marca? (si/no)"
                estado["estado"] = "confirmar_marca"
            else:
                mensaje = "❌ Número de marca no válido. Ingresá un número del listado o escribí el nombre."
        except ValueError:
            if any(m.lower() == msg for m in marcas):
                estado["marca"] = next(m for m in marcas if m.lower() == msg)
                mensaje = f"✅ Elegiste la marca *{estado['marca']}*. ¿Deseás volver a elegir otra marca? (si/no)"
                estado["estado"] = "confirmar_marca"
            else:
                mensaje = "❌ Marca no válida. Ingresá una marca válida (Ej: Toyota, Nissan)."

    elif estado["estado"] == "confirmar_marca":
        if msg in ['si', 'sí']:
            mensaje = respuestas["marca_prompt"]
            estado["estado"] = "marca"
        elif msg == 'no':
            mensaje = respuestas["modelo_prompt"]
            estado["estado"] = "modelo"
        else:
            mensaje = "❓ Por favor respondé con *sí* o *no*."

    elif estado["estado"] == "modelo":
        estado["modelo"] = msg_original
        mensaje = f"✅ Tu modelo es: *{estado['modelo']}*. ¿Deseás volver a elegir marca? (si/no)"
        estado["estado"] = "confirmar_modelo"

    elif estado["estado"] == "confirmar_modelo":
        if msg in ['si', 'sí']:
            mensaje = respuestas["marca_prompt"]
            estado["estado"] = "marca"
        elif msg == 'no':
            mensaje = "📅 Ingresá el año del vehículo."
            estado["estado"] = "año"
        else:
            mensaje = "❓ Por favor respondé con *sí* o *no*."

    elif estado["estado"] == "año":
        estado["año"] = msg_original
        mensaje = f"📋 Marca: *{estado.get('marca', 'N/A')}*, Modelo: *{estado.get('modelo', 'N/A')} {estado['año']}*\n"
        mensaje += respuestas["consulta_derivada"]
        mensaje += "\n\n¿Deseás volver al menú principal? (si/no)"
        estado["estado"] = "volver_menu"

    elif estado["estado"] == "volver_menu":
        if msg in ['si', 'sí']:
            mensaje = menu
            estado["estado"] = "esperando_opcion"
        elif msg == 'no':
            mensaje = respuestas["despedida"]
            estado["estado"] = "finalizado"
        else:
            mensaje = "❓ Por favor respondé con *sí* o *no*."

    elif estado["estado"] == "finalizado":
        if msg in ['hola', 'inicio', 'empezar']:
            mensaje = "🔁 Reiniciando conversación...\n" + menu
            estado = {"estado": "esperando_opcion"}
        else:
            mensaje = "🙌 Gracias por tu consulta. Si querés empezar de nuevo, escribí *hola*."

    usuarios[phone] = estado
    response.message(mensaje)

    # Logs en consola
    print(f"\n📩 Mensaje recibido: {msg_original}")
    print(f"🔁 Estado actual: {estado}")
    print(f"📤 Mensaje de respuesta: {mensaje}\n")

    return str(response)

if __name__ == "__main__":
    app.run(port=5000)