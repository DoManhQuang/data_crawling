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
DOI: [End-to-End System For Data Crawling, Monitoring, And Analyzation
Of E-Commerce Websites](https://link.springer.com/chapter/10.1007/978-3-031-80943-9_107)

```
Paper: End-to-End System For Data Crawling, Monitoring, And Analyzation
Of E-Commerce Websites
Authors: Manh Quang Do, Thi Lan Nguyen, Dinh Duy Vu, Xuan Duc Tran, Thi
Quynh Nguyen, Ba Nghien Nguyen, Van Tinh Nguyen and Ngoc Anh
Nguyen
```
### Cite
```
@InProceedings{10.1007/978-981-96-4282-3_18,
author="Nguyen, Thanh Long
and Do, Manh Quang
and Nguyen, Ba Nghien",
editor="Buntine, Wray
and Fjeld, Morten
and Tran, Truyen
and Tran, Minh-Triet
and Huynh Thi Thanh, Binh
and Miyoshi, Takumi",
title="MEPC: Multi-level Product Category Recognition Image Dataset",
booktitle="Information and Communication Technology",
year="2025",
publisher="Springer Nature Singapore",
address="Singapore",
pages="216--225",
abstract="Multi-level product category prediction is a problem for businesses providing online retail sector systems. Accurate Multi-level prediction supports the system in avoiding the need for sellers to fill in product category information, saving time and reducing the cost of listing products online. This is an open research problem, which always attracts researchers. Deep learning techniques have shown promising results for category recognition problems. A neat and clean dataset is an elementary requirement for building accurate and robust deep-learning models for category prediction. This article introduces a new image dataset of the multi-level product, called MEPC. MEPC dataset has +164.000 images in the processed format available in the dataset. We evaluate the MEPC dataset with popular deep learning models, benchmark results in a top-1 accuracy score of 92.055{\%} with 10 classes and a top-5 accuracy score of 57.36{\%} with 1000 classes. The proposed dataset is good for training, validation, and testing for hierarchical image classification to improve predict multi-level categories in the online retail sector systems. Data and code will be released at https://huggingface.co/datasets/sherlockvn/MEPC.",
isbn="978-981-96-4282-3"
}
```
