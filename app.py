from flask import Flask, render_template, request, redirect, url_for
import otp  # Import your otp.py file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_otp', methods=['POST'])
def generate_otp():
    phone_number = request.form['phone_number']
    otp.generate_and_send(phone_number)
    return redirect(url_for('verify_otp', phone_number=phone_number))

@app.route('/verify_otp/<phone_number>', methods=['GET', 'POST'])
def verify_otp(phone_number):
    if request.method == 'POST':
        user_entered_otp = request.form['otp']
        if otp.check(user_entered_otp):
            return "OTP verification successful!"
        else:
            return "Invalid OTP. Please try again."

    return render_template('verify_otp.html', phone_number=phone_number)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
