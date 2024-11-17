from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os

# Inicializar o Flask e o SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Variáveis globais para o estado da media
media_source = None
is_playing = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_media', methods=['POST'])
def set_media():
    global media_source
    data = request.get_json()
    media_source = data.get('media_source')
    return jsonify({'status': 'ok', 'message': 'Media configurada com sucesso!'})

@socketio.on('play_media')
def play_media():
    global is_playing
    if media_source:
        is_playing = True
        emit('media_status', {'status': 'playing', 'media_source': media_source}, broadcast=True)

@socketio.on('stop_media')
def stop_media():
    global is_playing
    is_playing = False
    emit('media_status', {'status': 'stopped'}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
