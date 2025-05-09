•	# BaiTapLon_TDH
•	Bài tập tự động tra cứu phạt nguội

•	Thư viện được sử dụng:
•	selenium
•	webdriver-manager
•	pytesseract
•	schedule
•	Pillow

•	Quy trình hoạt động của chương trình
•	Mở trình duyệt Chrome tự động bằng selenium.
•	Truy cập trang web: https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html.
•	Nhập biển số xe và chọn loại phương tiện.
•	Tải ảnh CAPTCHA từ website.
•	Tiền xử lý ảnh bằng Pillow:
  o	Chuyển ảnh sang đen trắng
  o	Đảo màu
  o	Tăng độ tương phản
  o	Resize ảnh để dễ đọc hơn
•	Đọc mã CAPTCHA sử dụng pytesseract với nhiều cấu hình khác nhau để tăng độ chính xác.
•	Gửi form và kiểm tra kết quả vi phạm.
•	Nếu CAPTCHA sai hoặc không có kết quả:
  o	Tự động thử lại tối đa 10 lần.
•	Nếu tìm được thông tin vi phạm:
  o	Hiển thị thông tin
  o	Tạm dừng chương trình và chờ đến giờ tiếp theo theo lịch đã đặt bằng schedule.

•	Yêu cầu trước khi chạy chương trình
•	cài đặt thư viện trong file requirements.txt: pip install requirements.txt
•	cài đặt Tesseract OCR (đã có 1 file trong thư mục tesseract1, chỉ cần chạy file rồi lấy đường dẫn đến thư mục đã cài đặt) Sau khi cài đặt xong các thư viện thì chỉ cần chạy chương trình nữa là hoàn tất# BaiTapLon_TDHQT
