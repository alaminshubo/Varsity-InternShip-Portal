from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# ডাটাবেজ কনফিগারেশন
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///internship.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ১. User ডাটাবেজ মডেল (টেবিল স্ট্রাকচার)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # student অথবা company
    student_id = db.Column(db.String(50), unique=True, nullable=True)
    department = db.Column(db.String(100), nullable=True)

# ২. Internship ডাটাবেজ মডেল
class Internship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    stipend = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)

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
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email already exists! Try another one.")
                return redirect(url_for('register'))
            
            if role == 'student' and student_id:
                existing_sid = User.query.filter_by(student_id=student_id).first()
                if existing_sid:
                    flash("This Student ID is already registered! Please use your own ID.")
                    return redirect(url_for('register'))
            
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
            
            db.session.add(new_user)
            db.session.commit()
            
            flash("Account created successfully! Please sign in.")
            return redirect(url_for('login'))
            
    return render_template('register.html')

@app.route('/student')
def student():
    if not session.get('logged_in'):
        flash("Please login first to view your dashboard!")
        return redirect(url_for('login'))
    
    session['user'] = session.get('user_name')
    return render_template('student.html')

@app.route('/company')
def company():
    return render_template('company.html')

@app.route('/logout')
def logout():
    session.clear()   
    return redirect(url_for('home')) 

@app.route("/post-internship", methods=["POST"])
def post_internship():
    if not session.get('logged_in') or session.get('user_type') != 'company':
        flash("Unauthorized action!")
        return redirect(url_for('login'))

    internship = Internship(
        title=request.form["title"],
        company_name=session["user_name"],   
        location=request.form["location"],
        stipend=request.form["stipend"],
        description=request.form["description"]
    )

    db.session.add(internship)
    db.session.commit()
    flash("Internship posted successfully!")
    return redirect(url_for('company'))

# একমাত্র এবং সঠিক /internship রুট (ডুপ্লিকেট রিমুভ করা হয়েছে)
@app.route("/internships")
def internship():
    search = request.args.get("search", "")

    if search:
        internships = Internship.query.filter(
            (Internship.company_name.contains(search)) |
            (Internship.title.contains(search))
        ).order_by(Internship.id.desc()).all()
    else:
        internships = Internship.query.order_by(Internship.id.desc()).all()

    return render_template(
        "internship.html",
        internships=internships
    )

if __name__ == '__main__':
    app.run(debug=True)
