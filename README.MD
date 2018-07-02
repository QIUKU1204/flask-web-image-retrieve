# flask-web-demo-keras-cnn-image-retrieve

## Describe

A very simple Flask app which accepts a image upload via a form, and then displays that similar images back to the user.

## Requirement

the webapp has been tested in the following environment

* Python (3.6)

## Virtualenv

First you create a virtual environment with `virtualenv venv` or `virtualenv -p python3.6 venv` in flask projcet folder.

Then enter `source venv/bin/activate` in order to active this virtual environment. 

Finally run `pip install -r requirements.txt` to install all dependencies libraries.

## Operation

#### 安装项目第三方库
- pip install -r requirements.txt

#### 建立图片特征索引集
- python creat_index.py -database static/database-few -index CNN_extracted_image_feature_few.h5

#### 本地图片库内检索
- python query_local.py -query static/database-few/1-001.jpg -index CNN_extracted_image_feature_few.h5 -result static/database-few

#### web在线图片检索
- run app.py

## Upadte

- 2018-4-28：done with the flask web demo in keras&cnn image retrieve.
- 2018-6-25：update and beautify html files of this flask web demo.
- 2018-6-28: Deploy in aliyun server.
- 2018-7-02: Do more in Deploy.

## Goal

- None.

## Deploy

#### [nginx + uwsgi + uwsgi emperor + virtualenv in aliyun](http://47.106.11.169:8080/image-retrieve)

#### nginx + uwsgi + supervisor + virtualenv in aliyun
