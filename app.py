from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_mail import Mail, Message
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# إعدادات البريد الإلكتروني
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # استخدم بريدك الإلكتروني
app.config['MAIL_PASSWORD'] = 'your_email_password'   # استخدم كلمة المرور الخاصة بك
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        if password != confirm_password:
            flash('كلمات المرور لا تتطابق.')
            return redirect(url_for('register'))

        # إرسال رمز التحقق إلى البريد الإلكتروني
        verification_code = random.randint(1000, 9999)
        msg = Message('رمز التحقق', sender='your_email@gmail.com', recipients=[email])
        msg.body = f'رمز التحقق الخاص بك هو: {verification_code}'
        mail.send(msg)

        # تخزين الرمز في الجلسة
        session['verification_code'] = verification_code
        session['email'] = email

        return render_template('verify.html', email=email)

    return render_template('register.html')

@app.route('/verify', methods=['POST'])
def verify():
    code = request.form['code']
    if code == str(session['verification_code']):
        flash('تم التحقق بنجاح! يمكنك الآن تسجيل الدخول.')
        return redirect(url_for('register'))  # إعادة توجيه إلى صفحة التسجيل
    else:
        flash('رمز التحقق غير صحيح!')
        return redirect(url_for('register'))

if __name__ == '__main__':
    app.run(debug=True)
