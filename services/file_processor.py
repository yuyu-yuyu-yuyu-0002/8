import os
import PyPDF2
from docx import Document
from config import Config

class FileProcessor:
    def __init__(self):
        self.max_file_size = Config.MAX_FILE_SIZE
        self.allowed_extensions = Config.ALLOWED_EXTENSIONS
    
    def validate_file_format(self, filename):
        """驗證文件格式"""
        if not filename:
            return False, "文件名稱不能為空"
        
        if '.' not in filename:
            return False, "文件必須有副檔名"
        
        extension = filename.rsplit('.', 1)[1].lower()
        if extension not in self.allowed_extensions:
            return False, f"不支援的文件格式。支援格式: {', '.join(self.allowed_extensions)}"
        
        return True, "格式驗證通過"
    
    def check_file_size(self, file_content):
        """檢查文件大小"""
        if len(file_content) > self.max_file_size:
            max_size_mb = self.max_file_size / 1024 / 1024
            return False, f"文件大小超過限制 ({max_size_mb}MB)"
        
        return True, "大小檢查通過"
    
    def extract_text_from_pdf(self, file_content):
        """從 PDF 提取文字"""
        try:
            from io import BytesIO
            pdf_file = BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return True, text.strip()
        except Exception as e:
            return False, f"PDF 文字提取失敗: {str(e)}"
    
    def extract_text_from_word(self, file_content):
        """從 Word 文檔提取文字"""
        try:
            from io import BytesIO
            doc_file = BytesIO(file_content)
            doc = Document(doc_file)
            
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return True, text.strip()
        except Exception as e:
            return False, f"Word 文字提取失敗: {str(e)}"
    
    def extract_text_from_txt(self, file_content):
        """從 TXT 文件提取文字"""
        try:
            # 嘗試不同編碼
            encodings = ['utf-8', 'big5', 'gbk', 'cp1252']
            
            for encoding in encodings:
                try:
                    text = file_content.decode(encoding)
                    return True, text.strip()
                except UnicodeDecodeError:
                    continue
            
            return False, "無法解碼文字文件，請檢查文件編碼"
        except Exception as e:
            return False, f"TXT 文字提取失敗: {str(e)}"
    
    def process_file(self, file_content, filename):
        """處理文件並提取文字"""
        # 驗證文件格式
        is_valid, message = self.validate_file_format(filename)
        if not is_valid:
            return False, message, None
        
        # 檢查文件大小
        is_valid_size, size_message = self.check_file_size(file_content)
        if not is_valid_size:
            return False, size_message, None
        
        # 獲取文件擴展名
        extension = filename.rsplit('.', 1)[1].lower()
        
        # 根據文件類型提取文字
        if extension == 'pdf':
            success, content = self.extract_text_from_pdf(file_content)
        elif extension in ['doc', 'docx']:
            success, content = self.extract_text_from_word(file_content)
        elif extension in ['txt', 'md']:
            success, content = self.extract_text_from_txt(file_content)
        else:
            return False, f"不支援的文件格式: {extension}", None
        
        if success:
            file_info = {
                'original_name': filename,
                'file_type': extension,
                'file_size': len(file_content)
            }
            return True, "文件處理成功", {'content': content, 'file_info': file_info}
        else:
            return False, content, None  # content 在這裡是錯誤訊息

# 創建全域實例
file_processor = FileProcessor()