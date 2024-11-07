# Cào dữ liệu về thui

## Cấu trúc thư mục
    └───source
        ├───database
        │   └───mongodb
        ├───ecom_api
        ├───message_queue
        └───restful_api

## Mô tả chức năng
* source : Lưu trữ code của project
* source/database : Tạo kết nối đến các CSDL như mysql, mongodb, ...
* source/ecom_api : Phân tích các API từ web để thực hiện các chức năng crawl dữ liệu
* source/message_queue : Tạo kết nối đến các message queue như redis, kafka, ...
* source/restfull_api : Viết API để query dữ liệu, monitor, backups, ...

## Cài đặt Env
```bash
pip install -r requirements.txt
```

## Hội nghị

```
Paper: End-to-End System For Data Crawling, Monitoring, And Analyzation
Of E-Commerce Websites
Authors: Manh Quang Do, Thi Lan Nguyen, Dinh Duy Vu, Xuan Duc Tran, Thi
Quynh Nguyen, Ba Nghien Nguyen, Van Tinh Nguyen and Ngoc Anh
Nguyen
```

<a class="none" href="http://icta.hvu.edu.vn/wp-content/uploads/2024/10/ICTA2024_-Tentative-Program_web-2.pdf">
							<img decoding="async" width="749" height="708" src="https://icta.hvu.edu.vn/wp-content/uploads/2024/10/chuong-trinh-hoi-nghi.jpg" class="attachment-large size-large wp-image-7931" alt="" srcset="https://icta.hvu.edu.vn/wp-content/uploads/2024/10/chuong-trinh-hoi-nghi.jpg 749w, https://icta.hvu.edu.vn/wp-content/uploads/2024/10/chuong-trinh-hoi-nghi-300x284.jpg 300w" sizes="(max-width: 749px) 100vw, 749px">								</a>
