# config.py

# Cấu hình web scraping
WEB_URL = "https://hsgame.me/"
BOSS_LIST_SELECTOR = ".text-warning.font-bold.text-xs.tooltip"
WAIT_TIME = 180  # Thời gian chờ giữa các lần cào dữ liệu (giây)

# Cấu hình file
CSV_FILE_PATH = "data/boss_history.csv"

# Cấu hình tùy chọn browser
HEADLESS = True # Chạy ngầm (không hiển thị cửa sổ)
# HEADLESS = False # Chạy với cửa sổ hiển thị (có thể thay bằng False để debug)
