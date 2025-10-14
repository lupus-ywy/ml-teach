from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 用于session加密

# 首页
@app.route('/')
def index():
    return redirect(url_for('login'))  # flask重定向网站的固定用法 ： redirect(url_for(其他函数名))

# 登录路由
@app.route('/login', methods=['POST', 'GET'])
def login():
    # error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = '用户名或密码错误！'

    return render_template('login.html')


# # 简单的用户验证函数
def valid_login(username, password):
    # 这里应该是数据库查询，暂时用硬编码演示
    valid_users = {
        'admin': '123456',
        'user1': 'password1',
        'test': 'test123'
    }
    return username in valid_users and valid_users[username] == password
#
#
# 登录成功后的处理函数
def log_the_user_in(username):
    # 将用户名存入session
    session['username'] = username
    return redirect(url_for('dashboard'))  # 跳转到仪表板页面
#
#
#
#
#
# 登录成功后的仪表板页面
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))  # 未登录则跳转到登录页

    return f'''
    <div class="container mt-5">
        <h2>欢迎, {session['username']}!</h2>
        <p>登录成功！</p>
        <a href="/logout22222" class="btn btn-secondary">退出登录</a>
    </div>
    '''
#
#
# 退出登录
@app.route('/logout22222')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)