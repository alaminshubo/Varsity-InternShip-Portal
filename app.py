from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# ডাটাবেজ কনফিগারেশন
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///internship.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ডাটাবেজ মডেল (টেবিল স্ট্রাকচার)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False) # ইমেইল ইউনিক
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # student অথবা company
    student_id = db.Column(db.String(50), unique=True, nullable=True) # এখানে unique=True করা হলো, যাতে এক ID দুইবার না বসে
    department = db.Column(db.String(100), nullable=True)

# টেবিল তৈরি করার লজিক
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email, password=password).first()
        
        if user:
            session['logged_in'] = True
            session['user_id'] = user.id
            session['user_name'] = user.fullname
            session['user_type'] = user.role
            flash("Login successful!")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password. Please try again.")
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form.get('role')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        student_id = request.form.get('student_id')
        department = request.form.get('department')
        
        if email and password:
            # ১. ইমেইলটি ডাটাবেজে আগে থেকে আছে কি না চেক করা
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email already exists! Try another one.")
                return redirect(url_for('register'))
            
            # ২. স্টুডেন্ট রোল হলে, Student ID আগে থেকেই ডাটাবেজে আছে কি না চেক করা
            if role == 'student' and student_id:
                existing_sid = User.query.filter_by(student_id=student_id).first()
                if existing_sid:
                    flash("This Student ID is already registered! Please use your own ID.")
                    return redirect(url_for('register'))
            
            # রোল অনুযায়ী ডেটা সেট করে অবজেক্ট তৈরি করা
            if role == 'student':
                new_user = User(
                    fullname=fullname,
                    email=email,
                    password=password,
                    role='student',
                    student_id=student_id,
                    department=department
                )
            elif role == 'company':
                new_user = User(
                    fullname=fullname,
                    email=email,
                    password=password,
                    role='company'
                )
            
            # ডেটা সেভ করা হচ্ছে
            db.session.add(new_user)
            db.session.commit()
            
            flash("Account created successfully! Please sign in.")
            return redirect(url_for('login'))
            
    return render_template('register.html')

# === নতুন যোগ করা ড্যাশবোর্ড রুট ===
@app.route('/student')
def student():
    # সিকিউরিটি চেক: লগইন না থাকলে লগইন পেজে রিডাইরেক্ট করবে
    if not session.get('logged_in'):
        flash("Please login first to view your dashboard!")
        return redirect(url_for('login'))
    
    # dashboard.html এর {{ session['user'] }} ভ্যারিয়েবলের সাথে মিল রাখার জন্য সেশন ডাটা সেট করা
    session['user'] = session.get('user_name')
    
    return render_template('student.html')

@app.route('/logout')
def logout():
    session.clear()   
    return redirect(url_for('home')) 
 
@app.route('/company')
def company():
    # কোম্পানি ড্যাশবোর্ড পেজ রেন্ডার করবে
    return render_template('company.html')

if __name__ == '__main__':
    app.run(debug=True)
