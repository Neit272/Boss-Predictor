# utils/data_loader.py
import csv
import time
import os
from config import CSV_FILE_PATH


def save_to_csv(data, filename=CSV_FILE_PATH):
    """Lưu dữ liệu vào file CSV."""

    with open(filename, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Ghi header nếu file rỗng
        if csvfile.tell() == 0:
            writer.writerow(["Lần xuất hiện", "Địa điểm (0: Đỏ, 1: Đen)"])

        # Ghi dữ liệu mới (nếu có), đảo ngược thứ tự của data
        for location in data:  # Duyệt ngược danh sách data
            current_time = time.strftime("%H:%M %d-%m-%Y")
            writer.writerow([current_time, location])


def load_existing_data(filename=CSV_FILE_PATH):
    """Tải dữ liệu đã lưu từ file CSV."""
    try:
        with open(filename, "r", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Bỏ qua header
            data = []
            for row in reader:
                data.append(int(row[1]))  # Chỉ lưu giá trị 0 hoặc 1
        return data
    except FileNotFoundError:
        return []
