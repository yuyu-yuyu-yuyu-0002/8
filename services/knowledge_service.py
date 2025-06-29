from services.firebase_service import firebase_service

class KnowledgeService:
    def __init__(self):
        self.firebase_service = firebase_service
    
    def create_knowledge(self, user_id, title, category, tags, content, file_info=None):
        """創建知識條目"""
        try:
            # 準備知識資料
            knowledge_data = {
                'title': title,
                'category': category,
                'tags': tags if isinstance(tags, list) else tags.split(','),
                'content': content
            }
            
            # 如果有文件資訊，加入到資料中
            if file_info:
                knowledge_data['file_info'] = file_info
            
            # 儲存到 Firebase
            knowledge_id = self.firebase_service.create_knowledge_entry(user_id, knowledge_data)
            
            if knowledge_id:
                return True, "知識條目創建成功", knowledge_id
            else:
                return False, "知識條目創建失敗", None
                
        except Exception as e:
            return False, f"創建知識條目時發生錯誤: {str(e)}", None
    
    def get_knowledge_list(self, user_id, category=None, search_term=None, limit=50):
        """獲取知識列表"""
        try:
            # 從 Firebase 獲取知識列表
            knowledge_list = self.firebase_service.get_knowledge_list(user_id, category, limit)
            
            # 如果有搜尋條件，進行篩選
            if search_term:
                filtered_list = []
                search_term = search_term.lower()
                
                for knowledge in knowledge_list:
                    # 在標題、內容、標籤中搜尋
                    if (search_term in knowledge.get('title', '').lower() or
                        search_term in knowledge.get('content', '').lower() or
                        any(search_term in tag.lower() for tag in knowledge.get('tags', []))):
                        filtered_list.append(knowledge)
                
                knowledge_list = filtered_list
            
            # 格式化回傳資料
            formatted_list = []
            for knowledge in knowledge_list:
                formatted_item = {
                    'id': knowledge['id'],
                    'title': knowledge.get('title', '未命名'),
                    'category': knowledge.get('category', '未分類'),
                    'tags': knowledge.get('tags', []),
                    'upload_date': knowledge.get('upload_date', '').strftime('%Y-%m-%d') if knowledge.get('upload_date') else '',
                    'file_size': self._format_file_size(knowledge.get('file_info', {}).get('file_size', 0))
                }
                formatted_list.append(formatted_item)
            
            return True, "獲取知識列表成功", formatted_list
            
        except Exception as e:
            return False, f"獲取知識列表時發生錯誤: {str(e)}", []
    
    def update_knowledge(self, user_id, knowledge_id, updates):
        """更新知識條目"""
        try:
            # 處理標籤格式
            if 'tags' in updates and isinstance(updates['tags'], str):
                updates['tags'] = updates['tags'].split(',')
            
            success = self.firebase_service.update_knowledge_entry(user_id, knowledge_id, updates)
            
            if success:
                return True, "知識條目更新成功"
            else:
                return False, "知識條目更新失敗"
                
        except Exception as e:
            return False, f"更新知識條目時發生錯誤: {str(e)}"
    
    def delete_knowledge(self, user_id, knowledge_id):
        """刪除知識條目"""
        try:
            success = self.firebase_service.delete_knowledge_entry(user_id, knowledge_id)
            
            if success:
                return True, "知識條目刪除成功"
            else:
                return False, "知識條目刪除失敗"
                
        except Exception as e:
            return False, f"刪除知識條目時發生錯誤: {str(e)}"
    
    def search_knowledge(self, user_id, query):
        """搜尋知識內容"""
        try:
            return self.get_knowledge_list(user_id, search_term=query)
        except Exception as e:
            return False, f"搜尋知識時發生錯誤: {str(e)}", []
    
    def get_all_categories(self, user_id):
        """獲取所有分類"""
        try:
            knowledge_list = self.firebase_service.get_knowledge_list(user_id, limit=1000)
            categories = set()
            
            for knowledge in knowledge_list:
                if 'category' in knowledge and knowledge['category']:
                    categories.add(knowledge['category'])
            
            return True, "獲取分類成功", list(categories)
            
        except Exception as e:
            return False, f"獲取分類時發生錯誤: {str(e)}", []
    
    def _format_file_size(self, size_bytes):
        """格式化文件大小"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s}{size_names[i]}"

# 創建全域實例
knowledge_service = KnowledgeService()