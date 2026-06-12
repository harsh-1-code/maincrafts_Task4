from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from functools import wraps # NEW: Required for building custom security decorators

app = Flask(__name__)
app.secret_key = "secure-secret-key"

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# NEW: THE ADMIN BOUNCER (DECORATOR)
# ==========================================
# This acts as a security checkpoint to ensure only admins can pass
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Kick them out if they aren't logged in OR if their role isn't 'admin'
        if 'user' not in session or session.get('role') != 'admin':
            return redirect('/dashboard')
        return f(*args, **kwargs)
    return wrapper

# ==========================================
# TASK 2: AUTHENTICATION ROUTES
# ==========================================

@app.route('/')
def home():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        db = get_db()
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        db.commit()
        return redirect('/login')
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", 
            (username,)
        ).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user'] = user['username']
            session['role'] = user['role'] # NEW: Save their role into the session!
            
            # Direct admins to their special dashboard, normal users to the regular one
            if session['role'] == 'admin':
                return redirect('/admin')
            return redirect('/dashboard')
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.clear() # Clears all session data, including the role
    return redirect('/login')

# ==========================================
# NEW: ADMIN DASHBOARD
# ==========================================

@app.route('/admin')
@admin_required # Only admins can access this!
def admin_dashboard():
    db = get_db()
    users = db.execute("SELECT id, username, role FROM users").fetchall()
    return render_template('admin.html', users=users)

# ==========================================
# TASK 3: CRUD ROUTES (STUDENT MANAGEMENT)
# ==========================================

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if 'user' not in session:
        return redirect('/login')
        
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']
        
        db = get_db()
        db.execute(
            "INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
            (name, email, course)
        )
        db.commit()
        return redirect('/students')
        
    return render_template('add_student.html')

@app.route('/students')
def students():
    if 'user' not in session:
        return redirect('/login')
        
    db = get_db()
    data = db.execute("SELECT * FROM students").fetchall()
    return render_template('students.html', students=data, role=session.get('role'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'user' not in session:
        return redirect('/login')
        
    db = get_db()
    student = db.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchone()
    
    if request.method == 'POST':
        db.execute(
            "UPDATE students SET name=?, email=?, course=? WHERE id=?",
            (request.form['name'], request.form['email'], request.form['course'], id)
        )
        db.commit()
        return redirect('/students')
        
    return render_template('edit_student.html', student=student)

# NEW: We added the @admin_required decorator here. Normal users cannot delete records anymore!
@app.route('/delete/<int:id>')
@admin_required 
def delete_student(id):
    db = get_db()
    db.execute("DELETE FROM students WHERE id=?", (id,))
    db.commit()
    return redirect('/students')

# ==========================================
# NEW: REST API ENDPOINTS
# ==========================================

# API 1: Get All Students (READ)
@app.route('/api/students', methods=['GET'])
def api_get_students():
    db = get_db()
    students = db.execute("SELECT * FROM students").fetchall()
    # Convert SQLite row objects into a list of Python dictionaries, then into JSON
    return jsonify([dict(row) for row in students])

# API 2: Add a New Student (CREATE)
@app.route('/api/students', methods=['POST'])
def api_add_student():
    data = request.get_json() # Extract the JSON data sent by the client
    db = get_db()
    db.execute(
        "INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
        (data['name'], data['email'], data['course'])
    )
    db.commit()
    return jsonify({"message": "Student added successfully"})

# API 3: Update a Student (UPDATE)
@app.route('/api/students/<int:id>', methods=['PUT'])
def api_update_student(id):
    data = request.get_json()
    db = get_db()
    db.execute(
        "UPDATE students SET name=?, email=?, course=? WHERE id=?",
        (data['name'], data['email'], data['course'], id)
    )
    db.commit()
    return jsonify({"message": "Student updated"})

# API 4: Delete a Student (DELETE)
@app.route('/api/students/<int:id>', methods=['DELETE'])
def api_delete_student(id):
    db = get_db()
    db.execute("DELETE FROM students WHERE id=?", (id,))
    db.commit()
    return jsonify({"message": "Student deleted"})

if __name__ == '__main__':
    app.run(debug=True)