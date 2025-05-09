# 1. Nhập các thư viện cần thiết
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from PIL import Image
import pytesseract
from io import BytesIO
import schedule
import time
import datetime

# 2. Đặt đường dẫn đến Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Python\tracuuphatnguoi\tesseract\tesseract.exe'

# 3. Hàm nhận diện captcha
def doc_captcha(driver):
    try:
        captcha = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "imgCaptcha")))
        location = captcha.location
        size = captcha.size
        screenshot = driver.get_screenshot_as_png()

        img = Image.open(BytesIO(screenshot))
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']
        captcha_img = img.crop((left, top, right, bottom))

        captcha_img = captcha_img.convert("L").resize((captcha_img.width*3, captcha_img.height*3))
        text = pytesseract.image_to_string(captcha_img, config='--psm 8').strip()
        return ''.join(filter(str.isalnum, text))
    except:
        return ""

# 4. Hàm tra cứu phạt nguội
def tra_cuu(bien_so, loai_xe):
    print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Đang kiểm tra: {bien_so}")

    options = Options()
    options.add_argument('--headless')  # không mở cửa sổ trình duyệt
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    try:
        # 1. Vào website đã chọn
        driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html")

        # 2. Nhập các thông tin Biển số xe, chọn loại phương tiện
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "BienKiemSoat"))).send_keys(bien_so)
        loai_xe_dropdown = driver.find_element(By.NAME, "LoaiXe")
        for option in loai_xe_dropdown.find_elements(By.TAG_NAME, "option"):
            if option.text.strip() == loai_xe:
                option.click()
                break

        # 3. Trích xuất mã bảo mật bằng thư viện pytesseract và nhập vào ô Input
        captcha_text = doc_captcha(driver)
        if len(captcha_text) < 4:
            print("Captcha không đọc được, thử lại...")
            driver.refresh()
            return

        driver.find_element(By.NAME, "txt_captcha").send_keys(captcha_text)
        driver.find_element(By.CLASS_NAME, "btnTraCuu").click()

        # 4. Kiểm tra kết quả phạt nguội
        try:
            ket_qua = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "bodyPrint123"))).text
            if "Biển kiểm soát" in ket_qua:
                print(" Có vi phạm:")
                print(ket_qua)
            else:
                print("Không vi phạm hoặc sai captcha.")
        except:
            print("Không có dữ liệu.")
            driver.refresh()
    finally:
        driver.quit()

# 5. Đặt lịch chạy tự động
def job():
    tra_cuu("92C41470", "Xe máy")

if __name__ == "__main__":
    schedule.every().day.at("06:00").do(job)
    schedule.every().day.at("12:00").do(job)

    print("Đang được thực hiện... Vui lòng đợi đến lúc 6h hoặc 12h để kiểm tra.")
    while True:
        schedule.run_pending()
        time.sleep(2)
