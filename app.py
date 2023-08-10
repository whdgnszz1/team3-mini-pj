from flask import Flask, render_template
from login import *
from signup import *
from detail import *
from oauth import google_oauth, kakao_oauth
import os
from flask_oauthlib.client import OAuth
import jwt

# Flask 객체 인스턴스 생성
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
oauth = OAuth(app)

app.register_blueprint(google_oauth.google_bp)
app.register_blueprint(kakao_oauth.kakao_bp)


# 메인페이지 렌더링
@app.route('/', methods = ['GET'])
def get_main_page():
    return render_template('index.html')

# 로그인페이지 렌더링
@app.route('/login', methods = ['GET'])
def get_login_page():
    return render_template('login.html')

# 상세 페이지 렌더링
@app.route('/detail/<id>', methods=['GET'])
def get_detail_page(id):
    return render_template('detail.html')

@app.route('/create-post', methods = ['GET'])
def get_createPost_page():
    return render_template('createPost.html')

# 로그인 기능
@app.route('/login', methods=['POST'])
def login():
    return user_login()


# 회원 인증 기능
@app.route('/auth/verify', methods=['POST'])
def verify_token():
    # 쿠키에서 AccessToken을 가져옵니다.
    token = request.cookies.get('AccessToken')
    
    if not token:
        return jsonify({"message": "토큰이 존재하지 않습니다.", "authenticated": False}), 401

    # 토큰이 구글 토큰인지 확인
    if token.startswith('google_'):
        print('구글 토큰')
        return jsonify({"message": "OK", "authenticated": True}), 200
    
    # 토큰이 카카오 토큰인지 확인
    if token.startswith('kakao_'):
        print('카카오 토큰')
        return jsonify({"message": "OK", "authenticated": True}), 200

    
    try:
        # 일반 토큰 검증
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"message": "OK", "authenticated": True}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "만료된 토큰입니다.", "authenticated": False}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "올바르지 않은 토큰입니다.", "authenticated": False}), 401



# 로그아웃 기능
@app.route('/logout', methods = ['POST'])
def logout():
    return user_logout()

# 회원가입
@app.route('/signup', methods = ['GET'])
def get_signup_page():
    return render_template('signup.html')

# 회원가입 기능
@app.route('/signup', methods=['POST'])
def signup():
    return user_signup()

# 이메일 유효성 검증
@app.route('/email-verification', methods=['POST'])
def email_verification():
    return verify_email()

# 이메일 인증 요청
@app.route('/send-email', methods=['POST'])
def send_verification_email():
    return send_email()
# 인증번호 검증
@app.route('/verify_auth_code', methods=['POST'])
def verify_auth_code():
    return email_auth()

# 상세페이지 게시글 조회
@app.route('/api/detail/<post_id>', methods=['GET'])
def detail(post_id):
    post = get_post_detail(post_id)
    if post:
        return jsonify(post)
    else:
        return jsonify({"message": "존재하지 않는 게시글입니다."}), 404

# 댓글 추가
@app.route('/detail/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    comment = request.json.get('comment')
    if not comment:
        return jsonify({"message": "올바르지 않은 형식입니다."}), 400
    if add_comment_to_db(post_id, comment):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 400

# 댓글 조회
@app.route('/detail/<post_id>/comments', methods=['GET'])
def get_comments(post_id):
    comments = fetch_comments_from_db(post_id)
    return jsonify({"comments": comments})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)