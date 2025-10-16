import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import configparser

print("Bắt đầu quá trình huấn luyện...")

# Đọc cấu hình để biết cần dùng cột nào
config = configparser.ConfigParser()
config.read('config.ini')
COL_DESC = config['CSV_COLUMNS']['description']
COL_KEYWORDS = config['CSV_COLUMNS']['keywords']

# Tải dữ liệu từ file CSV
try:
    df = pd.read_csv('violations_clean.csv')
    # Xử lý trường hợp cột keywords có thể trống (NaN)
    df[COL_KEYWORDS] = df[COL_KEYWORDS].fillna('') 
    print("Tải dữ liệu thành công.")
except Exception as e:
    print(f"Lỗi khi tải dữ liệu: {e}")
    exit()

# Kết hợp mô tả và từ khóa để làm giàu "kiến thức"
df['training_text'] = df[COL_DESC] + ' ' + df[COL_KEYWORDS]
training_data = df['training_text'].str.lower().tolist()

# Tạo và huấn luyện TF-IDF Vectorizer trên dữ liệu đã kết hợp
print("Đang huấn luyện TF-IDF Vectorizer...")
vectorizer = TfidfVectorizer()
X_violations = vectorizer.fit_transform(training_data)
print("Huấn luyện hoàn tất.")

# Lưu các file model
joblib.dump(vectorizer, 'vectorizer.joblib')
print("Đã lưu vectorizer vào file 'vectorizer.joblib'")
joblib.dump(X_violations, 'violations_matrix.joblib')
print("Đã lưu ma trận TF-IDF vào file 'violations_matrix.joblib'")
print("\nQuá trình huấn luyện và lưu trữ đã hoàn tất thành công!")
