from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Estado de cada usuario (diccionario temporal)
usuarios = {}

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    phone = request.values.get('From', '')
    msg = request.values.get('Body', '').strip().lower()
    response = MessagingResponse()

    # Lista de marcas disponibles
    marcas = ["Toyota", "Nissan", "Honda", "Mitsubishi", "Kia"]

    # Obtener el estado actual del usuario
    estado = usuarios.get(phone, {"estado": "inicio"})

    if estado["estado"] == "inicio":
        mensaje = "👋 ¡Hola! Gracias por comunicarte con *SOL REPUESTOS JAPONESES*\n"
        mensaje += "📍 San Martín 2489, Rosario\n"
        mensaje += "🕗 Lunes a Viernes de 8:30 a 17:00\n\n"
        mensaje += "Por favor, elegí la marca:\n"
        for i, m in enumerate(marcas, 1):
            mensaje += f"{i}. {m}\n"
        mensaje += "\n(Ej: escribí *Toyota* o *1*)"
        estado["estado"] = "marca_elegida"

    elif estado["estado"] == "marca_elegida":
        if msg.isdigit() and 1 <= int(msg) <= len(marcas):
            marca = marcas[int(msg) - 1]
            estado["marca"] = marca
            estado["estado"] = "confirm_marca"
            mensaje = f"🚗 Tu marca es *{marca}*. ¿Querés volver al menú de marcas? (sí/no)"
        elif msg.capitalize() in marcas:
            marca = msg.capitalize()
            estado["marca"] = marca
            estado["estado"] = "confirm_marca"
            mensaje = f"🚗 Tu marca es *{marca}*. ¿Querés volver al menú de marcas? (sí/no)"
        else:
            mensaje = "❌ Por favor, ingresá un número válido (1 a 5) o el nombre de la marca."

    elif estado["estado"] == "confirm_marca":
        if msg in ['sí', 'si']:
            estado["estado"] = "marca_elegida"
            mensaje = "🔁 Volviendo al menú de marcas...\n"
            for i, m in enumerate(marcas, 1):
                mensaje += f"{i}. {m}\n"
            mensaje += "\n(Ej: escribí *Toyota* o *1*)"
        elif msg == 'no':
            estado["estado"] = "modelo"
            mensaje = f"🛠️ Marca seleccionada: *{estado['marca']}*\n"
            mensaje += "Por favor, indicá el modelo y año (ej: Civic 2015):"
        else:
            mensaje = "❌ Por favor, respondé con 'sí' o 'no'."

    elif estado["estado"] == "modelo":
        estado["modelo"] = msg
        estado["estado"] = "confirm_modelo"
        mensaje = f"📋 Recibido: *{estado['modelo']}*\n"
        mensaje += "¿Querés volver al menú de marcas? (sí/no)"

    elif estado["estado"] == "confirm_modelo":
        if msg in ['sí', 'si']:
            estado["estado"] = "marca_elegida"
            mensaje = "🔁 Volviendo al menú de marcas...\n"
            for i, m in enumerate(marcas, 1):
                mensaje += f"{i}. {m}\n"
            mensaje += "\n(Ej: escribí *Toyota* o *1*)"
        elif msg == 'no':
            mensaje = f"✅ Perfecto! Marca: *{estado['marca']}*, Modelo: *{estado['modelo']}*\n"
            mensaje += "✨ Aguarde unos minutos y será atendido a la brevedad."
            estado["estado"] = "finalizado"
        else:
            mensaje = "❌ Por favor, respondé con 'sí' o 'no'."

    elif estado["estado"] == "finalizado":
        if msg in ['hola', 'empezar', 'inicio']:
            estado = {"estado": "inicio"}  # reinicia
            mensaje = "🔁 Reiniciando conversación...\n"
            mensaje += "👋 ¡Hola! Gracias por comunicarte con *SOL REPUESTOS JAPONESES*\n"
            mensaje += "📍 San Martín 2489, Rosario\n"
            mensaje += "🕗 Lunes a Viernes de 8:30 a 17:00\n\n"
            mensaje += "Por favor, elegí la marca:\n"
            for i, m in enumerate(marcas, 1):
                mensaje += f"{i}. {m}\n"
            mensaje += "\n(Ej: escribí *Toyota* o *1*)"
            estado["estado"] = "marca_elegida"
        else:
            mensaje = "🙌 Gracias por tu consulta. Si querés empezar de nuevo, escribí *hola*."

    # Guardar el nuevo estado del usuario
    usuarios[phone] = estado
    response.message(mensaje)
    return str(response)

if __name__ == "__main__":
    app.run(port=5000)
