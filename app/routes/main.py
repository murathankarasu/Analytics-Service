from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from app.services.analysis_service import AnalysisService

bp = Blueprint('main', __name__)
analysis_service = AnalysisService()

ALLOWED_EXTENSIONS = {
    'image': {'png', 'jpg', 'jpeg'},
    'video': {'mp4', 'avi', 'mov'}
}

def allowed_file(filename, file_type):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[file_type]

@bp.route('/analyze/text', methods=['POST'])
def analyze_text():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Metin bulunamadı'}), 400
    
    result = analysis_service.analyze_text(data['text'])
    return jsonify(result)

@bp.route('/analyze/image', methods=['POST'])
def analyze_image():
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya bulunamadı'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi'}), 400
    
    if not allowed_file(file.filename, 'image'):
        return jsonify({'error': 'İzin verilmeyen dosya formatı'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads/images', filename)
    file.save(filepath)
    
    result = analysis_service.analyze_image(filepath)
    
    # Geçici dosyayı sil
    os.remove(filepath)
    
    return jsonify(result)

@bp.route('/analyze/video', methods=['POST'])
def analyze_video():
    if 'file' not in request.files:
        return jsonify({'error': 'Dosya bulunamadı'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi'}), 400
    
    if not allowed_file(file.filename, 'video'):
        return jsonify({'error': 'İzin verilmeyen dosya formatı'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads/videos', filename)
    file.save(filepath)
    
    result = analysis_service.analyze_video(filepath)
    
    # Geçici dosyayı sil
    os.remove(filepath)
    
    return jsonify(result) 