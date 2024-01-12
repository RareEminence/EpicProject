from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'epicemmence@gmail.com' # Update with your email
app.config['MAIL_PASSWORD'] = 'uicf rdpd enff mmvt' # Update with your password
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Configure database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # SQLite database file in the current directory

mail = Mail(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    address = request.form.get('address')
    phone = request.form.get('phone')
    email = request.form.get('email')

    # Create a new User object and add it to the database
    new_user = User(name=name, address=address, phone=phone, email=email)
    db.session.add(new_user)
    db.session.commit()

    # Send welcome email
    # ... (same as before)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)