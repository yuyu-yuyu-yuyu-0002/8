from flask import Blueprint, request, jsonify
from services.knowledge_service import knowledge_service

knowledge_bp = Blueprint('knowledge', __name__)

@knowledge_bp.route('/knowledge/<user_id>', methods=['GET'])
def get_knowledge_list(user_id):
    """獲取知識列表 API"""
    try:
        # 獲取查詢參數
        category = request.args.get('category')
        search = request.args.get('search')
        limit = int(request.args.get('limit', 50))
        
        # 獲取知識列表
        success, message, data = knowledge_service.get_knowledge_list(
            user_id=user_id,
            category=category,
            search_term=search,
            limit=limit
        )
        
        if success:
            return jsonify({
                'success': True,
                'data': data,
                'message': message
            })
        else:
            return jsonify({
                'success': False,
                'message': message,
                'data': []
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取知識列表時發生錯誤: {str(e)}',
            'data': []
        }), 500

@knowledge_bp.route('/knowledge/<user_id>', methods=['POST'])
def create_knowledge(user_id):
    """創建知識條目 API"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': '請提供知識內容'
            }), 400
        
        # 獲取必要欄位
        title = data.get('title')
        category = data.get('category', '未分類')
        tags = data.get('tags', [])
        content = data.get('content')
        
        if not title or not content:
            return jsonify({
                'success': False,
                'message': '標題和內容不能為空'
            }), 400
        
        # 創建知識條目
        success, message, knowledge_id = knowledge_service.create_knowledge(
            user_id=user_id,
            title=title,
            category=category,
            tags=tags,
            content=content
        )
        
        if success:
            return jsonify({
                'success': True,
                'knowledge_id': knowledge_id,
                'message': message
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'創建知識條目時發生錯誤: {str(e)}'
        }), 500

@knowledge_bp.route('/knowledge/<user_id>/<knowledge_id>', methods=['PUT'])
def update_knowledge(user_id, knowledge_id):
    """更新知識條目 API"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': '請提供更新內容'
            }), 400
        
        # 更新知識條目
        success, message = knowledge_service.update_knowledge(
            user_id=user_id,
            knowledge_id=knowledge_id,
            updates=data
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'更新知識條目時發生錯誤: {str(e)}'
        }), 500

@knowledge_bp.route('/knowledge/<user_id>/<knowledge_id>', methods=['DELETE'])
def delete_knowledge(user_id, knowledge_id):
    """刪除知識條目 API"""
    try:
        # 刪除知識條目
        success, message = knowledge_service.delete_knowledge(
            user_id=user_id,
            knowledge_id=knowledge_id
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'刪除知識條目時發生錯誤: {str(e)}'
        }), 500

@knowledge_bp.route('/knowledge/<user_id>/search', methods=['GET'])
def search_knowledge(user_id):
    """搜尋知識內容 API"""
    try:
        query = request.args.get('q')
        
        if not query:
            return jsonify({
                'success': False,
                'message': '請提供搜尋關鍵字',
                'data': []
            }), 400
        
        # 搜尋知識
        success, message, data = knowledge_service.search_knowledge(
            user_id=user_id,
            query=query
        )
        
        if success:
            return jsonify({
                'success': True,
                'data': data,
                'message': message
            })
        else:
            return jsonify({
                'success': False,
                'message': message,
                'data': []
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'搜尋知識時發生錯誤: {str(e)}',
            'data': []
        }), 500

@knowledge_bp.route('/categories', methods=['GET'])
def get_categories():
    """獲取所有分類 API"""
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': '請提供用戶ID',
                'data': []
            }), 400
        
        # 獲取分類列表
        success, message, data = knowledge_service.get_all_categories(user_id)
        
        if success:
            return jsonify({
                'success': True,
                'data': data,
                'message': message
            })
        else:
            return jsonify({
                'success': False,
                'message': message,
                'data': []
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取分類時發生錯誤: {str(e)}',
            'data': []
        }), 500