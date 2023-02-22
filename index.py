import openai
import streamlit as st
import sounddevice as sd
import numpy as np
import io
import speech_recognition as sr

# Configurar la API key de OpenAI
openai.api_key = ""

# Definir las opciones de modelo de OpenAI
models = ["davinci", "curie", "babbage", "ada", "text-davinci-002"]

# Crear una lista de comandos que Jarvis puede entender
commands = ["Abrir", "Cerrar", "Buscar", "Informar", "Reproducir"]

# Definir la función que genera la respuesta de OpenAI
def generate_response(prompt, model):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].text.strip()
    return message

# Definir la función que procesa el comando del usuario y genera la respuesta de Jarvis
def process_command(command, query, model):
    if command == "Abrir":
        response = f"Abriendo {query}..."
    elif command == "Cerrar":
        response = f"Cerrando {query}..."
    elif command == "Buscar":
        response = f"Buscando información sobre {query}..."
    elif command == "Informar":
        response = generate_response(f"Información sobre {query}", model)
    elif command == "Reproducir":
        response = f"Reproduciendo {query}..."
    else:
        response = "Lo siento, no entiendo ese comando."
    return response

# Definir la función que muestra la interfaz de usuario
def main():
    st.title("Jarvis")
    st.write("Pulsa el botón de grabar y di tu comando")

    fs = 44100
    duration = 5.0

    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()

    audio_bytes = io.BytesIO()
    np.savetxt(audio_bytes, myrecording, delimiter=',')
    audio_bytes.seek(0)

    r = sr.Recognizer()
    stt_text = st.empty()

    with sr.AudioFile(audio_bytes) as source:
        audio = r.record(source)

        try:
            text = r.recognize_google(audio, language="es-ES")
            stt_text.markdown(f"**Comando:** {text}")
        except sr.UnknownValueError:
            stt_text.markdown(f"**Comando:** (no se ha entendido)")

    # Obtener el comando y el objeto de la consulta
    words = text.split()
    command = words[0]
    query = " ".join(words[1:])

    if command in commands:
        if command == "Informar":
            response = generate_response(f"Información sobre {query}", models[0])
        else:
            response = process_command(command, query, models[0])

        st.write(f"Jarvis: {response}")
    else:
        st.write("Lo siento, no entiendo ese comando.")

if __name__ == "__main__":
    main()

