import csv
import random

# --- CÁC THÔNG TIN MẪU ĐỂ TẠO DỮ LIỆU ---

# Danh sách các hành vi vi phạm (bạn có thể thêm nhiều hơn)
violation_templates = [
    "Không chấp hành hiệu lệnh của {light_or_sign}",
    "Điều khiển xe chạy quá tốc độ quy định từ {speed_min} km/h đến {speed_max} km/h",
    "Đi không đúng phần đường hoặc làn đường quy định",
    "Chuyển làn không có tín hiệu báo trước",
    "Dừng xe, đỗ xe tại nơi có biển cấm dừng, cấm đỗ",
    "Sử dụng điện thoại di động khi đang điều khiển xe",
    "Nồng độ cồn trong máu hoặc hơi thở vượt quá quy định nhưng chưa tới mức {alcohol_level}",
    "Không có Giấy phép lái xe",
    "Không có Giấy đăng ký xe",
    "Không có bảo hiểm trách nhiệm dân sự của chủ xe cơ giới",
    "Đi vào đường cấm, khu vực cấm",
    "Vượt xe tại nơi có biển báo cấm vượt",
    "Chở quá số người quy định",
    "Không nhường đường cho xe ưu tiên"
]

# Các biến thể để làm phong phú mô tả
light_or_sign_options = ["đèn tín hiệu giao thông", "biển báo hiệu", "vạch kẻ đường"]
speed_ranges = [(5, 10), (10, 20), (20, 35)]
alcohol_levels = ["50 miligam/100 mililít máu", "0,25 miligam/1 lít khí thở"]

# Mức phạt và đối tượng
subject_fines = {
    "Ô tô": {
        "min": 2000000,
        "max": 12000000,
        "step": 1000000
    },
    "Xe máy": {
        "min": 200000,
        "max": 6000000,
        "step": 200000
    },
    "Xe đạp điện": {
        "min": 100000,
        "max": 600000,
        "step": 100000
    }
}

# --- HÀM TẠO DỮ LIỆU ---

def generate_violation_data(num_rows):
    """Tạo ra một danh sách dữ liệu vi phạm giả."""
    data = []
    headers = ['violation_description', 'fine_min', 'fine_max', 'subject_type', 'law_reference']
    data.append(headers)

    for i in range(num_rows):
        # Chọn ngẫu nhiên một mẫu vi phạm
        template = random.choice(violation_templates)
        
        # Điền các chi tiết ngẫu nhiên vào mẫu
        description = template.format(
            light_or_sign=random.choice(light_or_sign_options),
            speed_min=random.choice(speed_ranges)[0],
            speed_max=random.choice(speed_ranges)[1],
            alcohol_level=random.choice(alcohol_levels)
        )
        
        # Chọn ngẫu nhiên đối tượng và mức phạt
        subject = random.choice(list(subject_fines.keys()))
        fine_config = subject_fines[subject]
        
        fine_min = random.randrange(fine_config["min"], fine_config["max"], fine_config["step"])
        fine_max = fine_min + random.randrange(1, 5) * fine_config["step"]

        # Tạo tham chiếu luật giả
        dieu = random.randint(5, 12)
        khoan = random.randint(1, 10)
        diem = random.choice('abcdefghiklmn')
        nghi_dinh = random.choice(["100/2019/NĐ-CP", "123/2021/NĐ-CP"])
        law_ref = f"Điểm {diem}, Khoản {khoan}, Điều {dieu} Nghị định {nghi_dinh}"
        
        # Thêm dòng dữ liệu
        data.append([description, fine_min, fine_max, subject, law_ref])
        
    return data

def write_to_csv(data, filename="violations_clean.csv"):
    """Ghi dữ liệu vào file CSV."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    print(f"Đã tạo thành công file '{filename}' với {len(data) - 1} dòng dữ liệu.")

# --- CHẠY CHƯƠNG TRÌNH ---
if __name__ == "__main__":
    # Bạn muốn tạo bao nhiêu dòng dữ liệu?
    number_of_violations_to_generate = 5000 
    
    generated_data = generate_violation_data(number_of_violations_to_generate)
    write_to_csv(generated_data)
