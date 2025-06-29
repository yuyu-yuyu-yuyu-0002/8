import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

class FirebaseService:
    def __init__(self):
        self._init_firebase()
        self.db = firestore.client()
    
    def _init_firebase(self):
        """初始化 Firebase"""
        firebase_key_json = os.environ.get("FIREBASE_CREDENTIALS")
        if not firebase_key_json:
            raise ValueError("❌ 環境變數 'FIREBASE_CREDENTIALS' 沒有設定")
        
        cred_dict = json.loads(firebase_key_json)
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
    
    def get_user_profile(self, user_id):
        """獲取用戶資料"""
        try:
            user_ref = self.db.collection('line_users').document(user_id)
            profile_ref = user_ref.collection('profile').document('info')
            profile_doc = profile_ref.get()
            
            if profile_doc.exists:
                return profile_doc.to_dict()
            return None
        except Exception as e:
            print(f"獲取用戶資料錯誤: {e}")
            return None
    
    def create_user_profile(self, user_id, profile_data):
        """創建用戶資料"""
        try:
            user_ref = self.db.collection('line_users').document(user_id)
            profile_ref = user_ref.collection('profile').document('info')
            
            profile_data.update({
                'created_at': datetime.now(),
                'last_active': datetime.now()
            })
            
            profile_ref.set(profile_data)
            return True
        except Exception as e:
            print(f"創建用戶資料錯誤: {e}")
            return False
    
    def create_knowledge_entry(self, user_id, knowledge_data):
        """創建知識條目"""
        try:
            user_ref = self.db.collection('line_users').document(user_id)
            knowledge_ref = user_ref.collection('knowledge_base').document()
            
            knowledge_data.update({
                'upload_date': datetime.now(),
                'last_modified': datetime.now(),
                'status': 'completed'
            })
            
            knowledge_ref.set(knowledge_data)
            return knowledge_ref.id
        except Exception as e:
            print(f"創建知識條目錯誤: {e}")
            return None
    
    def get_knowledge_list(self, user_id, category=None, limit=50):
        """獲取知識列表"""
        try:
            user_ref = self.db.collection('line_users').document(user_id)
            query = user_ref.collection('knowledge_base').order_by('upload_date', direction=firestore.Query.DESCENDING)
            
            if category:
                query = query.where('category', '==', category)
            
            docs = query.limit(limit).stream()
            
            knowledge_list = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                knowledge_list.append(data)
            
            return knowledge_list
        except Exception as e:
            print(f"獲取知識列表錯誤: {e}")
            return []
    
    def update_knowledge_entry(self, user_id, knowledge_id, updates):
        """更新知識條目"""
        try:
            user_ref = self.db.collection('line_users').document(user_id)
            knowledge_ref = user_ref.collection('knowledge_base').document(knowledge_id)
            
            updates['last_modified'] = datetime.now()
            knowledge_ref.update(updates)
            return True
        except Exception as e:
            print(f"更新知識條目錯誤: {e}")
            return False
    
    def delete_knowledge_entry(self, user_id, knowledge_id):
        """刪除知識條目"""
        try:
            user_ref = self.db.collection('line_users').document(user_id)
            knowledge_ref = user_ref.collection('knowledge_base').document(knowledge_id)
            knowledge_ref.delete()
            return True
        except Exception as e:
            print(f"刪除知識條目錯誤: {e}")
            return False
    
    def get_user_statistics(self, user_id):
        """獲取用戶統計資料"""
        try:
            user_ref = self.db.collection('line_users').document(user_id)
            
            # 獲取知識總數
            knowledge_docs = user_ref.collection('knowledge_base').stream()
            total_knowledge = len(list(knowledge_docs))
            
            # 獲取分類統計
            categories = set()
            knowledge_docs = user_ref.collection('knowledge_base').stream()
            for doc in knowledge_docs:
                data = doc.to_dict()
                if 'category' in data:
                    categories.add(data['category'])
            
            return {
                'total_knowledge': total_knowledge,
                'categories_count': len(categories),
                'today_uploads': 0,  # 簡化版本
                'weekly_uploads': 0,  # 簡化版本
                'knowledge_completion': 100  # 簡化版本
            }
        except Exception as e:
            print(f"獲取統計資料錯誤: {e}")
            return None

# 創建全域實例
firebase_service = FirebaseService()