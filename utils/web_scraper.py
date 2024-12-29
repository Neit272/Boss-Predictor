# utils/web_scraper.py
from selenium import webdriver  #type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.support import expected_conditions as EC  # type: ignore
from selenium.webdriver.chrome.options import Options  # type: ignore
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # type: ignore
from bs4 import BeautifulSoup  # type: ignore
import time
from config import WEB_URL, HEADLESS

# Không cần BOSS_LIST_SELECTOR nữa vì ta sẽ dùng find_elements_by_css_selector trực tiếp


def get_boss_history():
    """Lấy lịch sử boss xuất hiện từ trang web."""
    driver = None  # Khởi tạo driver ngoài try để đảm bảo có thể quit() trong finally
    try:
        chrome_options = Options()
        if HEADLESS:
            chrome_options.add_argument("--headless")
        # Khởi tạo driver với tùy chọn
        driver = webdriver.Chrome(options=chrome_options)

        # Mở trang web
        driver.get(WEB_URL)

        # Đợi popup xuất hiện
        popup = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "dialog#wellcome"))
        )
        time.sleep(3)

        # Tìm và click nút đóng popup
        close_button = popup.find_element(By.CSS_SELECTOR, "div.modal-box button.btn")
        close_button.click()

        # Đợi cho đến khi popup hoàn toàn biến mất (hidden hoặc display: none)
        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "dialog#wellcome"))
        )

        # Đợi nút "Map Boss Sv2" xuất hiện và có thể click được
        boss_map_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Map Boss Sv2')]")
            )
        )
        # Click vào nút "Map Boss Sv2"
        boss_map_button.click()
        time.sleep(3)

        # Đợi cho đến khi các phần tử li chứa data-tip xuất hiện
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//ul/li/div[contains(@class,'tooltip')]")
            )
        )

        # Lấy source code sau khi đã click và các item đã load
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Tìm element cha chứa danh sách boss
        boss_list_parent = soup.select_one(
            "body > div.min-w-\\[300px\\].flex.flex-col.gap-5.py-5.px-2.transition-all > div:nth-child(3) > div > div.lg\\:col-start-1.lg\\:row-start-1.lg\\:row-span-2.card.shadow-xl.border.border-current.relative > div > ul"
        )

        # Tìm tất cả các thẻ li bên trong element cha
        boss_list_items = boss_list_parent.find_all("li")
        boss_list_items.reverse() # Đảo ngược danh sách để lần xuất hiện xa nhất lưu ở đầu

        history = []
        for item in boss_list_items:
            # Tìm thẻ div có class "tooltip" trong mỗi li
            tooltip_div = item.find("div", class_="tooltip")
            # Trích xuất thông tin từ thuộc tính data-tip và chuyển đổi sang binary
            boss_location = tooltip_div["data-tip"]
            if boss_location == "Đen":
                history.append(1)  # Đen = 1
            elif boss_location == "Đỏ":
                history.append(0)  # Đỏ = 0
            else:
                history.append(-1)  # Trường hợp khác (nếu có)

        return history

    except TimeoutException:
        print(f"Lỗi: Timeout khi đợi popup hoặc nút 'Map Boss Sv2' hoặc danh sách boss")
        return None
    except NoSuchElementException:
        print(
            f"Lỗi: Không tìm thấy button 'Map Boss Sv2' hoặc các item trong danh sách boss"
        )
        return None
    except Exception as e:
        print(f"Lỗi: {e}")
        return None
    finally:
        if driver:
            driver.quit()
