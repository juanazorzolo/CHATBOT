# 🤖 Chatbot - Sol Repuestos

Este es un chatbot desarrollado para **Sol Repuestos**, un negocio dedicado a la venta de repuestos automotores. Su objetivo es asistir a los clientes de forma automatizada, brindando información sobre productos, horarios, formas de contacto, ubicación y respuestas frecuentes.

## 👤 Autor

Juana Zorzolo Rubio

📊 Estudiante avanzada de Tecnicatura Universitaria en IA

✉️ Contacto:

Si querés saber más o tenés alguna consulta, podés escribir a:
- juanazorzolo266@gmail.com
- solrepuestosjaponeses@gmail.com


## 🛠️ Funcionalidades

- Responde preguntas frecuentes (FAQ) sobre:
  - Horarios de atención
  - Medios de pago
  - Ubicación y contacto
- Puede derivar la conversación a un operador humano si el cliente lo solicita


## 💻 Tecnologías utilizadas
- Lenguaje: Python
- Framework / Librerías: Flask (para crear la API web del chatbot)
- Integración: ngrok para exponer localmente el servidor y poder probar con WhatsApp
- Frontend: No tiene frontend propio, se usa WhatsApp para la interacción con el bot

## 🧪 Ejemplos de uso
- Cliente: ¿Dónde están ubicados?
- Chatbot: Nuestra dirección es Av. San Martín 2489, Rosario, Santa Fe. ¡Te esperamos!

## 📝 Personalización
se pueden modificar fácilmente las respuestas del bot desde el archivo respuestas.json o directamente desde el código en la sección de lógica de respuestas.

## 📂 Estructura del proyecto
chatbot-sol-repuestos/

│

├── chatbot.py / index.js             # Archivo principal

├── respuestas.json               # Base de conocimiento simple

└── README.md                     # Este archivo


💡 Este chatbot fue creado para modernizar la atención al cliente de Sol Repuestos y facilitar el acceso a información útil de manera rápida y automatizada.
