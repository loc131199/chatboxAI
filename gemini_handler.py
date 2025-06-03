# gemini_handler.py

import os
import google.generativeai as genai
import config # Import file config.py để lấy cấu hình

class GeminiHandler:
    def __init__(self):
        
        #Khởi tạo Gemini API.
        
        try:
            # Ưu tiên lấy từ biến môi trường
            if "GEMINI_API_KEY" in os.environ:
                genai.configure(api_key=os.environ["GEMINI_API_KEY"])
            # Hoặc nếu bạn đã gán trực tiếp trong config.py (chỉ dùng để thử nghiệm)
            elif hasattr(config, 'GEMINI_API_KEY_DIRECT'):
                 genai.configure(api_key=config.GEMINI_API_KEY_DIRECT)
            else:
                raise KeyError("GEMINI_API_KEY chưa được đặt trong biến môi trường hoặc config.py.")

            self.model_embedding = config.MODEL_EMBEDDING
            self.model_llm = config.MODEL_LLM
            self.llm_model_instance = genai.GenerativeModel(self.model_llm)
            print("Cấu hình Gemini API thành công!")

        except KeyError as e:
            print(f"Lỗi: {e}")
            print("Vui lòng đặt biến môi trường GEMINI_API_KEY.")
            exit()
        except Exception as e:
            print(f"Lỗi cấu hình Gemini API: {e}")
            print("Vui lòng kiểm tra lại API Key của bạn hoặc kết nối mạng.")
            exit()

    def get_embedding(self, text):
       
        #Tạo vector embedding cho một đoạn văn bản bằng mô hình Gemini Embedding.
       
        if not text:
            return None
        try:
            response = genai.embed_content(model=self.model_embedding, content=text)
            return response['embedding']
        except Exception as e:
            print(f"Lỗi khi tạo embedding bằng Gemini: {e}")
            return None

    def generate_response(self, user_question, context):
        
        #Tạo phản hồi bằng mô hình ngôn ngữ lớn (LLM) Gemini Pro.
        
        prompt = f"""
        Bạn là một trợ lý thông minh chuyên cung cấp thông tin về các chương trình đào tạo và điều kiện tốt nghiệp từ một đồ thị tri thức.
        Sử dụng thông tin sau đây (nếu có) từ đồ thị tri thức để trả lời câu hỏi của người dùng một cách chính xác, đầy đủ và thân thiện.
        Nếu thông tin từ đồ thị không đủ để trả lời hoàn chỉnh, hãy nói rõ điều đó và đề xuất các thông tin bạn có thể cung cấp.

        Thông tin từ đồ thị tri thức:
        {context}

        Câu hỏi của người dùng:
        {user_question}

        Trả lời:
        """
        try:
            response = self.llm_model_instance.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Lỗi khi tạo phản hồi từ Gemini: {e}")
            return "Xin lỗi, tôi không thể tạo phản hồi lúc này do lỗi hệ thống AI."