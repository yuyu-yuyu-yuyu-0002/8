from services.firebase_service import firebase_service
from datetime import datetime, timedelta

class StatisticsService:
    def __init__(self):
        self.firebase_service = firebase_service
    
    def get_user_statistics(self, user_id):
        """獲取用戶統計資料"""
        try:
            # 獲取基本統計
            basic_stats = self.firebase_service.get_user_statistics(user_id)
            
            if basic_stats is None:
                return False, "無法獲取統計資料", None
            
            # 獲取詳細統計
            detailed_stats = self._get_detailed_statistics(user_id)
            
            # 合併統計資料
            stats = {
                **basic_stats,
                **detailed_stats
            }
            
            return True, "統計資料獲取成功", stats
            
        except Exception as e:
            return False, f"獲取統計資料時發生錯誤: {str(e)}", None
    
    def _get_detailed_statistics(self, user_id):
        """獲取詳細統計資料"""
        try:
            # 獲取所有知識條目
            knowledge_list = self.firebase_service.get_knowledge_list(user_id, limit=1000)
            
            if not knowledge_list:
                return {
                    'today_uploads': 0,
                    'weekly_uploads': 0,
                    'monthly_uploads': 0,
                    'category_distribution': {},
                    'upload_trend': []
                }
            
            # 計算時間相關統計
            now = datetime.now()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            week_start = today_start - timedelta(days=7)
            month_start = today_start - timedelta(days=30)
            
            today_uploads = 0
            weekly_uploads = 0
            monthly_uploads = 0
            category_count = {}
            
            for knowledge in knowledge_list:
                # 統計上傳時間
                upload_date = knowledge.get('upload_date')
                if upload_date:
                    if isinstance(upload_date, str):
                        # 如果是字串，嘗試解析
                        try:
                            upload_date = datetime.fromisoformat(upload_date.replace('Z', '+00:00'))
                        except:
                            continue
                    
                    if upload_date >= today_start:
                        today_uploads += 1
                    if upload_date >= week_start:
                        weekly_uploads += 1
                    if upload_date >= month_start:
                        monthly_uploads += 1
                
                # 統計分類
                category = knowledge.get('category', '未分類')
                category_count[category] = category_count.get(category, 0) + 1
            
            # 生成上傳趨勢（最近7天）
            upload_trend = self._generate_upload_trend(knowledge_list)
            
            return {
                'today_uploads': today_uploads,
                'weekly_uploads': weekly_uploads,
                'monthly_uploads': monthly_uploads,
                'category_distribution': category_count,
                'upload_trend': upload_trend
            }
            
        except Exception as e:
            print(f"獲取詳細統計時發生錯誤: {e}")
            return {}
    
    def _generate_upload_trend(self, knowledge_list):
        """生成最近7天的上傳趨勢"""
        try:
            trend = []
            now = datetime.now()
            
            for i in range(7):
                date = now - timedelta(days=i)
                date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
                date_end = date_start + timedelta(days=1)
                
                count = 0
                for knowledge in knowledge_list:
                    upload_date = knowledge.get('upload_date')
                    if upload_date:
                        if isinstance(upload_date, str):
                            try:
                                upload_date = datetime.fromisoformat(upload_date.replace('Z', '+00:00'))
                            except:
                                continue
                        
                        if date_start <= upload_date < date_end:
                            count += 1
                
                trend.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'count': count
                })
            
            return list(reversed(trend))  # 反轉使日期從舊到新
            
        except Exception as e:
            print(f"生成上傳趨勢時發生錯誤: {e}")
            return []
    
    def get_category_statistics(self, user_id):
        """獲取分類統計"""
        try:
            knowledge_list = self.firebase_service.get_knowledge_list(user_id, limit=1000)
            
            category_stats = {}
            total_count = len(knowledge_list)
            
            for knowledge in knowledge_list:
                category = knowledge.get('category', '未分類')
                if category not in category_stats:
                    category_stats[category] = {
                        'count': 0,
                        'percentage': 0
                    }
                category_stats[category]['count'] += 1
            
            # 計算百分比
            if total_count > 0:
                for category in category_stats:
                    category_stats[category]['percentage'] = round(
                        (category_stats[category]['count'] / total_count) * 100, 2
                    )
            
            return True, "分類統計獲取成功", category_stats
            
        except Exception as e:
            return False, f"獲取分類統計時發生錯誤: {str(e)}", {}
    
    def get_file_type_statistics(self, user_id):
        """獲取文件類型統計"""
        try:
            knowledge_list = self.firebase_service.get_knowledge_list(user_id, limit=1000)
            
            file_type_stats = {}
            
            for knowledge in knowledge_list:
                file_info = knowledge.get('file_info', {})
                file_type = file_info.get('file_type', '未知')
                
                if file_type not in file_type_stats:
                    file_type_stats[file_type] = 0
                file_type_stats[file_type] += 1
            
            return True, "文件類型統計獲取成功", file_type_stats
            
        except Exception as e:
            return False, f"獲取文件類型統計時發生錯誤: {str(e)}", {}

# 創建全域實例
statistics_service = StatisticsService()