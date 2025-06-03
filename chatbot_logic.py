# chatbot_logic.py

from neo4j_handle import Neo4jHandler
from gemini_handler import GeminiHandler

class ChatbotLogic:
    def __init__(self, neo4j_handler: Neo4jHandler, gemini_handler: GeminiHandler):
        """
        Khởi tạo logic chatbot với các handler đã được cung cấp.
        """
        self.neo4j_handler = neo4j_handler
        self.gemini_handler = gemini_handler

    def query_neo4j_for_context(self, user_question):
        """
        Truy vấn đồ thị tri thức Neo4j để lấy thông tin liên quan dựa trên câu hỏi của người dùng.
        Phần này vẫn dựa trên việc so sánh từ khóa.
        """
        context = []
        lower_question = user_question.lower()

        # Trường hợp 1: Hỏi về điều kiện tốt nghiệp chung
        if any(keyword in lower_question for keyword in ["điều kiện tốt nghiệp", "tốt nghiệp cần gì", "quy định tốt nghiệp"]):
            query = """
            MATCH (dk:DieuKienTotNghiep)
            RETURN dk.dieu_kien_chung AS dieu_kien
            LIMIT 1
            """
            results = self.neo4j_handler.execute_query(query)
            if results:
                context.append(f"**Điều kiện tốt nghiệp chung:** {results[0]['dieu_kien']}")
            else:
                context.append("Không tìm thấy thông tin về điều kiện tốt nghiệp chung trong đồ thị.")

        # Trường hợp 2: Hỏi về thông tin chương trình đào tạo cụ thể
        program_name = None
        if "công nghệ chế tạo máy" in lower_question:
            program_name = "Công nghệ chế tạo máy"
        elif "cơ khí hàng không" in lower_question:
            program_name = "Cơ khí hàng không"
        elif "kỹ thuật cơ điện tử" in lower_question or "cơ điện tử" in lower_question:
            program_name = "Kỹ thuật Cơ Điện tử"
        
        if program_name:
            query = f"""
            MATCH (ct:ChuongTrinhDaoTao {{ten_chuong_trinh: '{program_name}'}})
            RETURN ct.ten_chuong_trinh AS ten, ct.noi_dung AS noi_dung,
                   ct.ma_chuong_trinh AS ma, ct.tong_so_tin_chi_yeu_cau AS tin_chi
            """
            results = self.neo4j_handler.execute_query(query)
            if results:
                for res in results:
                    context.append(f"**Thông tin chương trình '{res['ten']}':**")
                    context.append(f"- Nội dung: {res['noi_dung']}")
                    context.append(f"- Mã chương trình: {res['ma']}")
                    context.append(f"- Tổng số tín chỉ yêu cầu: {res['tin_chi']}")
            else:
                context.append(f"Không tìm thấy thông tin cho chương trình '{program_name}' trong đồ thị.")

        # Trường hợp 3: Hỏi về danh sách các chương trình
        if any(keyword in lower_question for keyword in ["các chương trình", "những ngành học", "danh sách chương trình", "có ngành nào"]):
            query = """
            MATCH (ct:ChuongTrinhDaoTao)
            RETURN ct.ten_chuong_trinh AS ten
            ORDER BY ct.ten_chuong_trinh
            """
            results = self.neo4j_handler.execute_query(query)
            if results:
                program_names = [res['ten'] for res in results]
                context.append(f"Các chương trình đào tạo hiện có: {', '.join(program_names)}.")
            else:
                context.append("Hiện tại không có chương trình đào tạo nào trong đồ thị.")

        if not context:
            return "Không có thông tin cụ thể từ đồ thị cho câu hỏi này. Bạn có thể thử hỏi về 'điều kiện tốt nghiệp' hoặc tên một 'chương trình đào tạo' cụ thể (ví dụ: 'Công nghệ chế tạo máy')."

        return "\n".join(context)

    def chat(self, question):
        """
        Xử lý một lượt trò chuyện:
        1. Lấy ngữ cảnh từ Neo4j.
        2. Tạo phản hồi bằng LLM dựa trên ngữ cảnh và câu hỏi.
        """
        # Bước 1: Lấy ngữ cảnh từ Neo4j
        context = self.query_neo4j_for_context(question)
        print(f"\n--- Ngữ cảnh từ Đồ thị Tri thức ---\n{context}\n----------------------------------\n")

        # Bước 2: Tạo phản hồi bằng LLM, sử dụng ngữ cảnh đã lấy
        response = self.gemini_handler.generate_response(question, context)
        return response