from flask import Blueprint, request, jsonify
from app.services.analysis_service import AnalysisService

bp = Blueprint('main', __name__)
analysis_service = AnalysisService()

@bp.route('/analyze/text', methods=['POST'])
def analyze_text():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Metin bulunamadı'}), 400
    
    result = analysis_service.analyze_text(data['text'])
    return jsonify(result) 