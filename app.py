import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import configparser
import joblib # Thư viện để tải model

# --- 1. Đọc cấu hình (vẫn cần để biết tên cột khi trả lời) ---
config = configparser.ConfigParser()
config.read('config.ini')
COL_DESC = config['CSV_COLUMNS']['description']
COL_FINE_MIN = config['CSV_COLUMNS']['fine_min']
COL_FINE_MAX = config['CSV_COLUMNS']['fine_max']
COL_SUBJECT = config['CSV_COLUMNS']['subject']
COL_LAW_REF = config['CSV_COLUMNS']['law_ref']

# --- 2. Khởi tạo ứng dụng Flask ---
app = Flask(__name__)
CORS(app)

# --- 3. Tải dữ liệu và các mô hình đã được huấn luyện sẵn ---
try:
    # Tải dataframe chứa thông tin
    df = pd.read_csv('violations_clean.csv')
    
    # Tải vectorizer và ma trận đã được huấn luyện từ file
    vectorizer = joblib.load('vectorizer.joblib')
    X_violations = joblib.load('violations_matrix.joblib')
    
    print("Tải dữ liệu và mô hình đã huấn luyện thành công!")

except Exception as e:
    print(f"Lỗi khi tải dữ liệu hoặc mô hình: {e}")
    print("Vui lòng chạy file 'train.py' trước để tạo ra các file model.")
    df = None

# --- 4. Logic chatbot (Không thay đổi) ---
def find_most_similar_violation(user_message):
    if df is None:
        return "Xin lỗi, cơ sở dữ liệu lỗi hoặc mô hình chưa sẵn sàng."

    message_lower = user_message.lower()
    X_user = vectorizer.transform([message_lower])
    similarities = cosine_similarity(X_user, X_violations)
    
    most_similar_index = np.argmax(similarities)
    max_similarity = similarities[0, most_similar_index]
    
    SIMILARITY_THRESHOLD = 0.2
    
    if max_similarity > SIMILARITY_THRESHOLD:
        violation_info = df.iloc[most_similar_index]
        
        muc_phat_min_str = f"{int(violation_info[COL_FINE_MIN]):,}".replace(',', '.')
        muc_phat_max_str = f"{int(violation_info[COL_FINE_MAX]):,}".replace(',', '.')
        
        answer = (
            f"Lỗi vi phạm tương tự nhất tôi tìm thấy là: '{violation_info[COL_DESC]}'.\n"
            f"-> Mức phạt: Từ {muc_phat_min_str} VNĐ đến {muc_phat_max_str} VNĐ.\n"
            f"-> Đối tượng áp dụng: {violation_info[COL_SUBJECT]}.\n"
            f"-> Căn cứ pháp lý: {violation_info[COL_LAW_REF]}."
        )
        return answer
    
    return "Xin lỗi, tôi không tìm thấy thông tin về lỗi vi phạm bạn đã hỏi."

# --- 5. API Endpoint  ---
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'Không nhận được tin nhắn.'}), 400
    bot_response = find_most_similar_violation(user_message)
    return jsonify({'answer': bot_response})

# --- 6. Chạy ứng dụng  ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)
