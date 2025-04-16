import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.static_folder = 'uploads'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'webm', 'ogg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    video_files = os.listdir(app.config['UPLOAD_FOLDER']) if os.path.exists(app.config['UPLOAD_FOLDER']) else []
    return render_template('index.html', videos=video_files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video_file' not in request.files:
        return 'No file part'
    file = request.files['video_file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Video uploaded successfully'
    return 'Invalid file type'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
