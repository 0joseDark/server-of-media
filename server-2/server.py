from flask import Flask, render_template, request, Response
import soundfile as sf
from threading import Thread
import time

app = Flask(__name__)

media_path = None
stream_audio = False

def generate_audio():
    """Transmite áudio em pequenos pacotes para o cliente."""
    global stream_audio, media_path
    if not media_path:
        yield b''
        return
    try:
        with sf.SoundFile(media_path) as audio_file:
            while stream_audio:
                data = audio_file.read(1024, dtype='int16')
                if not data:
                    break
                yield data.tobytes()
                time.sleep(0.01)  # Simula streaming em tempo real
    except Exception as e:
        print("Erro no streaming de áudio:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_media', methods=['POST'])
def set_media():
    global media_path, stream_audio
    data = request.json
    media_path = data.get('media_source')
    stream_audio = True
    return {"message": "Fonte de mídia atualizada"}

@app.route('/stop_media', methods=['POST'])
def stop_media():
    global stream_audio
    stream_audio = False
    return {"message": "Mídia parada"}

@app.route('/audio')
def audio():
    """Rota para streaming de áudio."""
    return Response(generate_audio(), mimetype="audio/wav")

if __name__ == '__main__':
    app.run(debug=True)
