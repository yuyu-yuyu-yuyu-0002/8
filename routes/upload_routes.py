from flask import Blueprint, request, jsonify
from services.file_processor import file_processor
from services.knowledge_service import knowledge_service
from config import Config

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """文件上傳 API"""
    try:
        # 檢查是否有文件
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': '沒有選擇文件'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': '沒有選擇文件'
            }), 400
        
        # 獲取其他參數
        user_id = request.form.get('user_id')
        category = request.form.get('category', '未分類')
        tags = request.form.get('tags', '')
        title = request.form.get('title', file.filename)
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': '缺少用戶ID'
            }), 400
        
        # 檢查文件格式
        if not Config.is_allowed_file(file.filename):
            return jsonify({
                'success': False,
                'message': f'不支援的文件格式。支援格式: {", ".join(Config.ALLOWED_EXTENSIONS)}'
            }), 400
        
        # 讀取文件內容
        file_content = file.read()
        
        # 處理文件
        success, message, processed_data = file_processor.process_file(file_content, file.filename)
        
        if not success:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # 創建知識條目
        success, create_message, knowledge_id = knowledge_service.create_knowledge(
            user_id=user_id,
            title=title,
            category=category,
            tags=tags.split(',') if tags else [],
            content=processed_data['content'],
            file_info=processed_data['file_info']
        )
        
        if success:
            return jsonify({
                'success': True,
                'knowledge_id': knowledge_id,
                'message': '文件上傳成功'
            })
        else:
            return jsonify({
                'success': False,
                'message': create_message
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'上傳過程中發生錯誤: {str(e)}'
        }), 500

@upload_bp.route('/upload/batch', methods=['POST'])
def batch_upload():
    """批量文件上傳 API"""
    try:
        # 檢查是否有文件
        if 'files' not in request.files:
            return jsonify({
                'success': False,
                'message': '沒有選擇文件'
            }), 400
        
        files = request.files.getlist('files')
        user_id = request.form.get('user_id')
        category = request.form.get('category', '未分類')
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': '缺少用戶ID'
            }), 400
        
        results = []
        success_count = 0
        
        for file in files:
            if file.filename == '':
                continue
            
            try:
                # 檢查文件格式
                if not Config.is_allowed_file(file.filename):
                    results.append({
                        'filename': file.filename,
                        'success': False,
                        'message': '不支援的文件格式'
                    })
                    continue
                
                # 讀取文件內容
                file_content = file.read()
                
                # 處理文件
                success, message, processed_data = file_processor.process_file(file_content, file.filename)
                
                if not success:
                    results.append({
                        'filename': file.filename,
                        'success': False,
                        'message': message
                    })
                    continue
                
                # 創建知識條目
                success, create_message, knowledge_id = knowledge_service.create_knowledge(
                    user_id=user_id,
                    title=file.filename,
                    category=category,
                    tags=[],
                    content=processed_data['content'],
                    file_info=processed_data['file_info']
                )
                
                if success:
                    success_count += 1
                    results.append({
                        'filename': file.filename,
                        'success': True,
                        'knowledge_id': knowledge_id,
                        'message': '上傳成功'
                    })
                else:
                    results.append({
                        'filename': file.filename,
                        'success': False,
                        'message': create_message
                    })
            
            except Exception as e:
                results.append({
                    'filename': file.filename,
                    'success': False,
                    'message': f'處理文件時發生錯誤: {str(e)}'
                })
        
        return jsonify({
            'success': True,
            'message': f'批量上傳完成，成功: {success_count}/{len(results)}',
            'results': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'批量上傳過程中發生錯誤: {str(e)}'
        }), 500