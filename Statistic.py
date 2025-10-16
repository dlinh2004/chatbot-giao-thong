import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

group_province = [
    {
        "name": "Một số chỉ tiêu tai nạn giao thông phân chia theo Địa phương, Năm và Chỉ tiêu 2022.xlsx",
        "year": 2022
    },
    {
        "name": "Một số chỉ tiêu tai nạn giao thông phân chia theo Địa phương, Năm và Chỉ tiêu 2023.xlsx",
        "year": 2023
    },
    {
        "name": "Một số chỉ tiêu tai nạn giao thông phân chia theo Địa phương, Năm và Chỉ tiêu 2024.xlsx",
        "year": 2024
    }
]

def top_10(file, index):
    # Đọc dữ liệu
    df = pd.read_excel(file[index]["name"])

    total_row = df[df['title'] == 'TỔNG SỐ']
    total_value = int(total_row['total_accidents'].values[0])
    current_year = file[index]["year"]

    # Lọc bỏ các dòng có giá trị không mong muốn trong cột 'title'
    df1 = df[~df["title"].isin(["TỔNG SỐ",
                               "Đồng bằng sông Hồng",
                               "Trung du và miền núi phía Bắc",
                               "Bắc Trung Bộ và Duyên hải miền Trung",
                               "Tây Nguyên",
                               "Đông Nam Bộ",
                               "Đồng bằng sông Cửu Long"
                               ])]

    # 1. Bar chart: so sánh số vụ theo tỉnh
    plt.figure(figsize=(12,6))
    df_sorted = df1.sort_values('total_accidents', ascending=False).head(10)
    plt.bar(df_sorted['title'], df_sorted['total_accidents'], color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.title(f"Top 10 tỉnh có số vụ tai nạn cao nhất năm {current_year}, Tổng số vụ: {total_value}")
    plt.xlabel("Tỉnh/Thành phố")
    plt.ylabel("Số vụ tai nạn")

    # thêm nhãn số
    for i, v in enumerate(df_sorted['total_accidents']):
        plt.text(i, v + 10, str(v), ha='center', fontsize=9)

    plt.tight_layout()
    plt.show()

top_10(group_province, 0)
top_10(group_province, 1)
top_10(group_province, 2)

#####################################################################################################################

# Đọc 3 file
df_2022 = pd.read_csv('group1_province_2022.csv', sep=";", encoding="utf-8")
df_2023 = pd.read_csv('group1_province_2023.csv', sep=";", encoding="utf-8")
df_2024 = pd.read_csv('group1_province_2024.csv', sep=";", encoding="utf-8")


# Lấy tổng số toàn quốc
def get_total(df, label):
    df.columns = df.columns.str.strip().str.lower()  # chuẩn hóa tên cột
    total_row = df[df['title'].str.contains('tổng', case=False, na=False)]
    total = int(total_row['total_accidents'].iloc[0])
    deaths = int(total_row['deaths'].iloc[0])
    injuries = int(total_row['injuries'].iloc[0])
    return {'year': label, 'total_accidents': total, 'deaths': deaths, 'injuries': injuries}

data = [
    get_total(df_2022, 2022),
    get_total(df_2023, 2023),
    get_total(df_2024, 2024)
]

trend_df = pd.DataFrame(data)
# dùng chuỗi (để Matplotlib coi là nhãn phân loại)
trend_df['year'] = trend_df['year'].astype(str)


# Vẽ biểu đồ xu hướng
plt.figure(figsize=(10,6))
plt.plot(trend_df['year'], trend_df['total_accidents'], marker='o', label='Số vụ tai nạn')
plt.plot(trend_df['year'], trend_df['deaths'], marker='o', label='Số người chết')
plt.plot(trend_df['year'], trend_df['injuries'], marker='o', label='Số người bị thương')

# hiển thị số cụ thể trên mỗi điểm
for i, row in trend_df.iterrows():
    plt.text(row['year'], row['total_accidents'], f"{row['total_accidents']:,}", ha='center', va='bottom', fontsize=9)
    plt.text(row['year'], row['deaths'], f"{row['deaths']:,}", ha='center', va='bottom', fontsize=9)
    plt.text(row['year'], row['injuries'], f"{row['injuries']:,}", ha='center', va='bottom', fontsize=9)

# --- Cài đặt hiển thị ---
plt.title('Xu hướng tai nạn giao thông giai đoạn 2022–2024')
plt.xlabel('Năm')
plt.ylabel('Số lượng')
plt.legend()
plt.grid(True)
plt.show()

#####################################################################################################################

# Đọc dữ liệu
df = pd.read_csv("group3_August_2425.csv", sep=";", encoding="utf-8")

# Nếu dữ liệu kiểu "8/2024" thì chuyển thành datetime để vẽ được
df['date'] = pd.to_datetime(df['month'], format='%m/%Y', errors='coerce')

# --- Biểu đồ 1: Xu hướng số vụ, chết, bị thương theo tháng ---
plt.figure(figsize=(8,5))
plt.plot(df['month'], df['total_accidents'], marker='o', label='Tổng số vụ')
plt.plot(df['month'], df['deaths'], marker='o', label='Số người chết')
plt.plot(df['month'], df['injuries'], marker='o', label='Số người bị thương')

# Thêm số lên từng điểm
for i, row in df.iterrows():
    plt.text(row['month'], row['total_accidents'], f"{row['total_accidents']:,}",
             ha='center', va='bottom', fontsize=8)
    plt.text(row['month'], row['deaths'], f"{row['deaths']:,}",
             ha='center', va='bottom', fontsize=8)
    plt.text(row['month'], row['injuries'], f"{row['injuries']:,}",
             ha='center', va='bottom', fontsize=8)

plt.title('Xu hướng tai nạn giao thông từ tháng 8/2024 đến 8/2025')
plt.xlabel('Tháng')
plt.ylabel('Số lượng')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Biểu đồ 2: So sánh tổng số vụ, chết, bị thương (tổng thể) ---
totals = {
    'Tổng số vụ': df['total_accidents'].sum(),
    'Người chết': df['deaths'].sum(),
    'Bị thương': df['injuries'].sum()
}
plt.figure(figsize=(6,4))

bars = plt.bar(totals.keys(), totals.values(), color=['skyblue','salmon','orange'])
# Thêm số trên đầu cột
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f"{int(height):,}",
             ha='center', va='bottom', fontsize=9)

plt.title('Tổng hợp tai nạn giao thông (toàn kỳ)')
plt.ylabel('Số lượng')
plt.tight_layout()
plt.show()

# --- Biểu đồ 3: Mối liên hệ giữa số vi phạm và tổng phạt tiền ---
plt.figure(figsize=(8,5))
plt.plot(df['month'], df['violations'], color='blue', marker='o', label='Số vi phạm')
plt.plot(df['month'], df['fines_amount_billion'], color='red', marker='o', label='Tiền phạt (tỷ đồng)')

# Thêm số lên từng điểm
for i, row in df.iterrows():
    plt.text(row['month'], row['violations'], f"{row['violations']:,}",
             ha='center', va='bottom', fontsize=8, color='blue')
    plt.text(row['month'], row['fines_amount_billion'], f"{row['fines_amount_billion']:,}",
             ha='center', va='bottom', fontsize=8, color='red')

plt.title('Số vi phạm và tiền phạt theo tháng')
plt.xlabel('Tháng')
plt.ylabel('Giá trị')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
