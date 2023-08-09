import boto3
from dotenv import load_dotenv
import os
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

load_dotenv()
def s3_connection():
    try:
        # s3 클라이언트 생성
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id = os.environ.get("aws_access_key_id"),
            aws_secret_access_key=os.environ.get("aws_secret_access_key"),
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!") 
        return s3
        
s3 = s3_connection()

# s3에 파일 업로드
# try:
#     # (로컬에서 올릴 이미지, 버킷이름, 버킷에 저장될 파일 이름)
#     s3.upload_file("./img/분홍토끼.png","group3artistimage","분홍토끼")
# except Exception as e:
#     print(e)

# 이미지파일 S3에 저장인데... 아직 하는 중...
# @app.route("/upload", methods=["POST"])
# def file_upload():
#     image_receive = request.form['image_give']

#     try:
#     # (로컬에서 올릴 이미지, 버킷이름, 버킷에 저장될 파일 이름)
#         s3.upload_file("./img/턱끈펭귄.jpg","group3artistimage","턱끈펭귄")
#     except Exception as e:
#         print(e)
#     return jsonify({'msg': '저장 완료!'})