from flask import Flask, render_template, redirect, url_for, request, session, jsonify 
from werkzeug.security import generate_password_hash, check_password_hash 

from models import Student, Enrollment, Course, db
app = Flask(__name__) 
app.secret_key = '123456' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sliman:123456@localhost/student_portal' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app)

# Routes 
@app.route('/') 
def index():     
    return render_template('index.html')  

@app.route('/register', methods=['GET', 'POST']) 
def register():     
    if request.method == 'POST':         
        name = request.form['full_name']         
        email = request.form['email']         
        password = request.form['password']         
        hashed_password = generate_password_hash(password)         
        new_student = Student(name=name, email=email, password_hash=hashed_password)         
        db.session.add(new_student)         
        db.session.commit()         
        return redirect(url_for('login'))     
    return render_template('register.html')  

@app.route('/login', methods=['GET', 'POST']) 
def login():     
    if request.method == 'POST':         
        email = request.form['email']         
        password = request.form['password']         
        student = Student.query.filter_by(email=email).first()         
        if student and check_password_hash(student.password_hash, password):             
            session['user_id'] = student.id
            return redirect(url_for('dashboard'))     
    return render_template('login.html')  
    
@app.route('/dashboard') 
def dashboard():     
    if 'user_id' not in session:         
        return redirect(url_for('login'))     
    student = Student.query.get(session['user_id'])     
    enrollments = Enrollment.query.filter_by(student_id=student.id).all()     
    return render_template('dashboard.html', student=student, enrollments=enrollments)  

@app.route('/courses') 
def courses():     
    all_courses = Course.query.all()     
    return render_template('courses.html', courses=all_courses) 

@app.route('/api/courses') 
def api_courses():     
    courses = Course.query.all()     
    return jsonify([{'id': c.id, 'title': c.title, 'description': c.description} for c in courses])  

@app.route('/ajax/enroll', methods=['POST']) 
def enroll():     
    if 'user_id' not in session:         
        return jsonify({'status': 'fail', 'message': 'Not logged in'})     
    course_id = request.json['course_id']     
    new_enrollment = Enrollment(student_id=session['user_id'], course_id=course_id)     
    db.session.add(new_enrollment)     
    db.session.commit()     
    return jsonify({'status': 'success'})  

@app.route('/logout') 
def logout():     
    session.pop('user_id', None)     
    return redirect(url_for('index'))  


app.config['TEMPLATES_AUTO_RELOAD'] = True


if __name__ == '__main__':    
    with app.app_context():
        db.create_all()     
    app.run(debug=True)