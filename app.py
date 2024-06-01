from flask import Flask, jsonify, request
from video_manager.upload_video import upload_video
from video_manager.delete_video import delete_video
import os

app = Flask(__name__)

# Configuración de la carpeta de subida
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def process_video_hd(filename):
    # Lógica para procesar el video HD
    # Aquí se procesaría el video (por ejemplo, remover el fondo)
    return f"Processed HD video: {filename}"

def process_video_non_hd(filename):
    # Lógica para procesar el video no HD
    # Aquí se procesaría el video (por ejemplo, remover el fondo)
    return f"Processed non-HD video: {filename}"

@app.route('/upload_hd', methods=['POST'])
def upload_hd():
    filename, response = upload_video()
    if filename:
        process_result = process_video_hd(filename)
        delete_response = delete_video(filename)
        return jsonify({'message': response.json['message'], 'processing_result': process_result}), 200
    return response

@app.route('/upload_non_hd', methods=['POST'])
def upload_non_hd():
    filename, response = upload_video()
    if filename:
        process_result = process_video_non_hd(filename)
        delete_response = delete_video(filename)
        return jsonify({'message': response.json['message'], 'processing_result': process_result}), 200
    return response

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
