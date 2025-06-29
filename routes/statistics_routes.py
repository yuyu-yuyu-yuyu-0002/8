from flask import Blueprint, request, jsonify
from services.statistics_service import statistics_service

statistics_bp = Blueprint('statistics', __name__)

@statistics_bp.route('/statistics/<user_id>', methods=['GET'])
def get_user_statistics(user_id):
    """獲取用戶統計資料 API"""
    try:
        # 獲取統計資料
        success, message, data = statistics_service.get_user_statistics(user_id)
        
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
                'data': None
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取統計資料時發生錯誤: {str(e)}',
            'data': None
        }), 500

@statistics_bp.route('/statistics/<user_id>/category', methods=['GET'])
def get_category_statistics(user_id):
    """獲取分類統計 API"""
    try:
        # 獲取分類統計
        success, message, data = statistics_service.get_category_statistics(user_id)
        
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
                'data': {}
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取分類統計時發生錯誤: {str(e)}',
            'data': {}
        }), 500

@statistics_bp.route('/statistics/<user_id>/filetype', methods=['GET'])
def get_file_type_statistics(user_id):
    """獲取文件類型統計 API"""
    try:
        # 獲取文件類型統計
        success, message, data = statistics_service.get_file_type_statistics(user_id)
        
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
                'data': {}
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取文件類型統計時發生錯誤: {str(e)}',
            'data': {}
        }), 500

@statistics_bp.route('/statistics/<user_id>/dashboard', methods=['GET'])
def get_dashboard_data(user_id):
    """獲取儀表板數據 API"""
    try:
        # 獲取基本統計
        success, message, basic_stats = statistics_service.get_user_statistics(user_id)
        if not success:
            return jsonify({
                'success': False,
                'message': message,
                'data': None
            }), 500
        
        # 獲取分類統計
        success, _, category_stats = statistics_service.get_category_statistics(user_id)
        if not success:
            category_stats = {}
        
        # 獲取文件類型統計
        success, _, file_type_stats = statistics_service.get_file_type_statistics(user_id)
        if not success:
            file_type_stats = {}
        
        # 合併所有統計資料
        dashboard_data = {
            'basic_statistics': basic_stats,
            'category_statistics': category_stats,
            'file_type_statistics': file_type_stats
        }
        
        return jsonify({
            'success': True,
            'data': dashboard_data,
            'message': '儀表板數據獲取成功'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取儀表板數據時發生錯誤: {str(e)}',
            'data': None
        }), 500