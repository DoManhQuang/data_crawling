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
