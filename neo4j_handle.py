# neo4j_handler.py

from neo4j import GraphDatabase

class Neo4jHandler:
    def __init__(self, uri, user, password):
        #  Khởi tạo và kết nối với cơ sở dữ liệu Neo4j. 
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()
            print("Kết nối Neo4j thành công!")
        except Exception as e:
            print(f"Lỗi kết nối Neo4j: {e}")
            self.driver = None
            raise # Ném lại ngoại lệ để main.py có thể bắt và xử lý

    def close(self):
        
      #  Đóng kết nối cơ sở dữ liệu Neo4j một cách an toàn.
      
        if self.driver:
            self.driver.close()
            print("Đã đóng kết nối Neo4j.")

    def execute_query(self, query, params=None):
        
        # Thực thi một truy vấn Cypher trong Neo4j và trả về kết quả.
        # params: Các tham số tùy chọn cho truy vấn.
        
        if not self.driver:
            # Nếu driver là None, nghĩa là kết nối ban đầu thất bại
            raise ConnectionError("Không có kết nối Neo4j hoạt động.")
        
        with self.driver.session() as session:
            try:
                result = session.run(query, params)
                return [record for record in result]
            except Exception as e:
                print(f"Lỗi khi thực thi truy vấn Cypher: {e}")
                return []