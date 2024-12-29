# main.py
from utils.data_loader import load_existing_data, save_to_csv
from utils.web_scraper import get_boss_history
from config import CSV_FILE_PATH, WAIT_TIME
import time


def main():
    """Hàm chính."""
    last_saved_data = load_existing_data(CSV_FILE_PATH)[-20:]

    if len(last_saved_data) > 0:
        print("Đã load được data cũ!")
    else:
        print("Chưa có data nào được lưu. Tiến hành thu thập data mới...")

    while True:
        current_data = get_boss_history()

        if current_data:
            if not last_saved_data:  # Nếu danh sách rỗng (lần đầu tiên)
                print("Lần chạy đầu tiên, lưu tất cả data.")
                save_to_csv(current_data, CSV_FILE_PATH)
                last_saved_data = current_data
            else:
                new_items = []

                # Lấy 10 phần tử cuối cùng của last_saved_data (hoặc tất cả nếu ít hơn 10)
                last_11_saved = last_saved_data[-11:]
                print(f"Data cập nhật lần cuối: {last_11_saved}")
                print(f"Data hiện tại: {current_data}")

                # So sánh và loại bỏ phần tử đầu tiên của last_11_saved cho đến khi rỗng
                while last_11_saved:
                    if current_data and current_data[0] == last_11_saved[0]:
                        current_data.pop(0)
                        last_11_saved.pop(0)
                    else:
                        last_11_saved.pop(0)

                # Các phần tử còn lại trong current_data là dữ liệu mới
                new_items = current_data

                if new_items:
                    print(f"Phát hiện {len(new_items)} data mới: {new_items}")
                    save_to_csv(new_items, CSV_FILE_PATH)
                    last_saved_data = (
                        last_saved_data + new_items
                    )  # Thêm data mới lên đầu

        print(f"Đang chờ {WAIT_TIME} giây cho đến lần thu thập data tiếp theo...")
        time.sleep(WAIT_TIME)


if __name__ == "__main__":
    main()
