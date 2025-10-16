Chatbot Giao Thông Việt Nam

Chatbot Giao Thông là một ứng dụng hỗ trợ người dùng tra cứu mức xử phạt vi phạm giao thông tại Việt Nam bằng cách trò chuyện tự nhiên (chat). Hệ thống gồm Backend (Flask + Machine Learning) và Frontend giao diện chat hiện đại (Next.js/V0 by Vercel).

🚦 Chức năng chính

💬 Hỏi chatbot về lỗi vi phạm giao thông (tốc độ, chưa đội mũ bảo hiểm, vượt đèn đỏ…)

📎 Trả về mô tả lỗi, mức phạt tiền tối thiểu – tối đa, điều luật liên quan.

🤖 Mô hình Machine Learning được huấn luyện từ dữ liệu luật CSV.

🖥️ Giao diện chat hiện đại, hỗ trợ tiếng Việt.

🛠 Cấu trúc dự án
project/
├── chatbotgiaothong/        # Giao diện Frontend (Next.js / V0)
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   └── package.json
├── app.py                   # Flask API Backend
├── train.py                 # Huấn luyện mô hình
├── violations_clean.csv     # Dữ liệu vi phạm giao thông
├── vectorizer.joblib
├── violations_matrix.joblib
└── requirements.txt

📦 1️⃣ Cài đặt Backend (Flask + ML)

Yêu cầu: Python 3.9+

Mở Terminal tại thư mục gốc dự án:

# 1. Cài đặt thư viện
pip install -r requirements.txt

# 2. Huấn luyện mô hình trước (chỉ cần chạy 1 lần)
py train.py

# 3. Chạy API Flask
py app.py


✅ API sẽ chạy tại: http://127.0.0.1:5000

💻 2️⃣ Cài đặt Frontend (Chat UI - V0/Next.js)

Mở terminal mới, chuyển vào thư mục chatbotgiaothong (hoặc nơi chứa giao diện):

# 1. Cài các package
npm install --legacy-peer-deps

# 2. Chạy giao diện
npm run dev


Sau khi chạy thành công, mở trình duyệt vào:
👉 http://localhost:3000

🔗 3️⃣ Kết nối Chatbot

Frontend sẽ gửi yêu cầu đến API bằng endpoint:

POST http://127.0.0.1:5000/chat

🧪 Ví dụ để test Chatbot

"Tôi chạy xe máy vượt đèn đỏ bị phạt bao nhiêu?"
"Ô tô vượt quá tốc độ 10km/h"
"Không đội mũ bảo hiểm phạt sao?"
"Quên mang bằng lái thì bị xử lý như thế nào?"

