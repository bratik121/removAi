from flask import Flask, request, jsonify
import os
from iaModel.iaModel import process_video, model, model_input_size

app = Flask(__name__)

# Configuración de la carpeta de subida
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ruta principal para subir videos
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        # Guardar el archivo en la carpeta de subida
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return jsonify({'message': 'File uploaded successfully'}), 200

# Ruta para procesar el video
@app.route('/process_video', methods=['POST'])
def process_uploaded_video():
    # Verificar si se proporciona un archivo
    if 'filename' not in request.form:
        return jsonify({'error': 'No video filename provided'}), 400

    # Nombre del archivo de video
    video_filename = request.form['filename']

    # Verificar si el archivo existe en la carpeta de subida
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    if not os.path.exists(video_path):
        return jsonify({'error': 'Video file not found'}), 404

    # Nombre del video de salida
    output_video_filename = f"{os.path.splitext(video_filename)[0]}_processed.avi"
    output_video_path = os.path.join(app.config['UPLOAD_FOLDER'], output_video_filename)

    # Procesar el video
    process_video(video_path, output_video_path, model, model_input_size)

    return jsonify({'message': f'Video processed successfully. Output filename: {output_video_filename}'}), 200

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, port=3000)
