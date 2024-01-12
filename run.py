from flask import Flask, render_template, request
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'epicemmence@gmail.com'
app.config['MAIL_PASSWORD'] = 'uicf rdpd enff mmvt'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Configure database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'  # Change the database name if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mail = Mail(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)

# Create tables within the application context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    address = request.form.get('address')
    phone = request.form.get('phone')
    email = request.form.get('email')

    # Store data in the database
    new_user = User(name=name, address=address, phone=phone, email=email)
    db.session.add(new_user)
    db.session.commit()

    # Send welcome email
    msg = Message('Welcome!', sender='epicemmence@gmail.com', recipients=[email])
    msg.html = f'''
        <p>Hi {name},</p>
        <p>Welcome to our platform! Here are your details:</p>
        <ul>
            <li><strong>Name:</strong> {name}</li>
            <li><strong>Address:</strong> {address}</li>
            <li><strong>Phone:</strong> {phone}</li>
            <li><strong>Email:</strong> {email}</li>
        </ul>
        <p>Thank you for signing up!</p>
    '''
    mail.send(msg)

    return 'Data stored and email sent successfully!'

if __name__ == '__main__':
    app.run(debug=True)
