from flask import Flask, render_template, redirect, url_for, flash, request, g
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from database import get_db, close_connection
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' # Change this for production
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg'}

# Register standard teardown
app.teardown_appcontext(close_connection)

from werkzeug.utils import secure_filename
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Class for Flask-Login
class User(UserMixin):
    def __init__(self, id, name, email, password, role, is_active=True, 
                 age=None, gender=None, blood_group=None, contact_number=None, 
                 address=None, medical_notes=None, specialization=None, 
                 experience_years=None, available_time=None, available_slots=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.active = is_active  # Renamed to avoid UserMixin conflict
        
        # Profile Fields
        self.age = age
        self.gender = gender
        self.blood_group = blood_group
        self.contact_number = contact_number
        self.address = address
        self.medical_notes = medical_notes
        
        # Doctor Specific
        self.specialization = specialization
        self.experience_years = experience_years
        self.available_time = available_time
        self.available_slots = available_slots

    @property
    def is_active(self):
        return self.active

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
        if not user:
            return None
        return User(
            id=user['id'], name=user['name'], email=user['email'], password=user['password'],
            role=user['role'], is_active=user['is_active'], age=user['age'], gender=user['gender'],
            blood_group=user['blood_group'], contact_number=user['contact_number'], address=user['address'],
            medical_notes=user['medical_notes'], specialization=user['specialization'],
            experience_years=user['experience_years'], available_time=user['available_time'],
            available_slots=user['available_slots']
        )
        
    @staticmethod
    def get_by_email(email):
        db = get_db()
        user = db.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()
        if not user:
            return None
        return User(
            id=user['id'], name=user['name'], email=user['email'], password=user['password'],
            role=user['role'], is_active=user['is_active'], age=user['age'], gender=user['gender'],
            blood_group=user['blood_group'], contact_number=user['contact_number'], address=user['address'],
            medical_notes=user['medical_notes'], specialization=user['specialization'],
            experience_years=user['experience_years'], available_time=user['available_time'],
            available_slots=user['available_slots']
        )

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

from werkzeug.security import generate_password_hash, check_password_hash

# ... (Imports remain, need to ensure werkzeug is imported)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        db = get_db()
        user_check = db.execute('SELECT id FROM user WHERE email = ?', (email,)).fetchone()
        
        if user_check:
            flash('Email already exists.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='scrypt')
        
        db.execute(
            'INSERT INTO user (name, email, password, role, is_active) VALUES (?, ?, ?, ?, ?)',
            (name, email, hashed_password, role, True)
        )
        db.commit()
        
        flash('Account created! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.get_by_email(email)

        if user and check_password_hash(user.password, password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact support.', 'danger')
                return redirect(url_for('login'))
                
            login_user(user)
            if user.role == 'admin': # Future proofing, though role might just be checked in dashboard
                 return redirect(url_for('admin_dashboard'))
            if user.role == 'doctor':
                return redirect(url_for('dashboard'))
            return redirect(url_for('dashboard')) # Patient also goes to dashboard
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'doctor':
        from datetime import date
        today = date.today().strftime('%Y-%m-%d')
        
        db = get_db()
        # Calculate Stats
        today_count = db.execute('SELECT COUNT(*) FROM appointment WHERE doctor_id = ? AND date = ?', (current_user.id, today)).fetchone()[0]
        pending_count = db.execute('SELECT COUNT(*) FROM appointment WHERE doctor_id = ? AND status = ?', (current_user.id, 'Pending')).fetchone()[0]
        completed_count = db.execute('SELECT COUNT(*) FROM appointment WHERE doctor_id = ? AND status = ?', (current_user.id, 'Completed')).fetchone()[0]
        
        return render_template('doctor_dashboard.html', 
                             today_count=today_count, 
                             pending_count=pending_count, 
                             completed_count=completed_count)
    return render_template('patient_dashboard.html')

@app.route('/appointments')
@login_required
def appointments():
    # Filter Logic
    status_filter = request.args.get('status')
    date_filter = request.args.get('date')
    search_query = request.args.get('q')

    db = get_db()
    query = "SELECT a.*, u.name as patient_name, d.name as doctor_name FROM appointment a JOIN user u ON a.patient_id = u.id JOIN user d ON a.doctor_id = d.id WHERE 1=1"
    params = []

    if status_filter:
        query += " AND a.status = ?"
        params.append(status_filter)
    if date_filter:
        query += " AND a.date = ?"
        params.append(date_filter)

    if current_user.role == 'doctor':
        query += " AND a.doctor_id = ?"
        params.append(current_user.id)
        if search_query:
            # Search by patient name
            query += " AND u.name LIKE ?"
            params.append(f'%{search_query}%')
        
        appointments_rows = db.execute(query, params).fetchall()
        # Convert rows to objects/dicts for template compatibility if needed, using row factory makes them dict-like
        return render_template('doctor_appointments.html', appointments=appointments_rows)
    
    # Patient Dashboard logic
    doctors = db.execute("SELECT * FROM user WHERE role = 'doctor'").fetchall()
    
    # My appointments
    patient_query = query + " AND a.patient_id = ?"
    patient_params = params + [current_user.id]
    my_appointments = db.execute(patient_query, patient_params).fetchall()
    
    # Check for notifications
    notifications = db.execute("SELECT * FROM appointment WHERE patient_id = ? AND notification_read = 0", (current_user.id,)).fetchall()
    for notif in notifications:
        if notif['notification_msg']:
            # We need to fetch doctor name. Since we didn't join in this simple query, let's just fetch it or use a better query.
            # actually let's just do a join here too or lazy load. 
            # For simplicity, let's fetch doctor name separate or rely on the previous logic if we change query.
            # But wait, notif is a Row object. 
            doctor_name = db.execute("SELECT name FROM user WHERE id = ?", (notif['doctor_id'],)).fetchone()['name']
            flash(f"Update on appointment with Dr. {doctor_name}: {notif['notification_msg']}", 'info')
        
        db.execute("UPDATE appointment SET notification_read = 1 WHERE id = ?", (notif['id'],))
    
    if notifications:
        db.commit()

    return render_template('patient_appointments.html', doctors=doctors, my_appointments=my_appointments)

@app.route('/book_appointment', methods=['POST'])
@login_required
def book_appointment():
    if current_user.role != 'patient':
        flash('Only patients can book appointments.', 'danger')
        return redirect(url_for('appointments'))

    doctor_id = request.form.get('doctor_id')
    date = request.form.get('date')
    time = request.form.get('time')

    db = get_db()
    
    # Slot Validation
    doctor = db.execute('SELECT * FROM user WHERE id = ?', (doctor_id,)).fetchone()
    if doctor['available_slots']:
        allowed_slots = [s.strip() for s in doctor['available_slots'].split(',')]
        if time not in allowed_slots:
            flash(f'Invalid time slot. Dr. {doctor["name"]} is available at: {doctor["available_slots"]}', 'danger')
            return redirect(url_for('appointments'))

    # Double Booking Prevention
    existing_appt = db.execute('SELECT id, status FROM appointment WHERE doctor_id = ? AND date = ? AND time = ?', (doctor_id, date, time)).fetchone()
    if existing_appt and existing_appt['status'] != 'Rejected':
        flash('This time slot is already booked. Please choose another.', 'danger')
        return redirect(url_for('appointments'))

    db.execute(
        'INSERT INTO appointment (patient_id, doctor_id, date, time, status, notification_read) VALUES (?, ?, ?, ?, ?, ?)',
        (current_user.id, doctor_id, date, time, 'Pending', 0)
    )
    db.commit()
    flash('Appointment request sent!', 'success')
    return redirect(url_for('appointments'))

@app.route('/update_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def update_appointment(appointment_id):
    if current_user.role != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('appointments'))

    db = get_db()
    appointment = db.execute('SELECT * FROM appointment WHERE id = ?', (appointment_id,)).fetchone()
    
    if not appointment:
        flash('Appointment not found.', 'danger')
        return redirect(url_for('appointments'))
        
    if appointment['doctor_id'] != current_user.id:
        flash('You cannot manage this appointment.', 'danger')
        return redirect(url_for('appointments'))

    status = request.form.get('status')
    reason = request.form.get('reason')
    
    # Init vars to update
    rejection_reason = None
    notification_msg = None
    symptoms = None
    diagnosis = None
    advice = None
    prescription_filename = None
    completed_at = None

    if status in ['Approved', 'Rejected', 'Completed']:
        if status == 'Rejected' and reason:
            rejection_reason = reason
            notification_msg = f'Rejected: {reason}'
        elif status == 'Approved':
            notification_msg = 'Approved'
        elif status == 'Completed':
             symptoms = request.form.get('symptoms')
             diagnosis = request.form.get('diagnosis')
             advice = request.form.get('advice')
             
             # Handle Prescription Upload
             if 'prescription' in request.files:
                 file = request.files['prescription']
                 if file and allowed_file(file.filename):
                     filename = secure_filename(file.filename)
                     # Unique filename: appt_<id>_<filename>
                     unique_filename = f"appt_{appointment_id}_{filename}"
                     file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                     # Ensure directory exists (redundant if created manually but good safety)
                     os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                     
                     full_path = os.path.join(app.root_path, file_path)
                     file.save(full_path)
                     prescription_filename = unique_filename
             
             from datetime import datetime
             completed_at = datetime.now()
             notification_msg = 'Consultation Completed'
        
        # Build Update Query dynamically or just update relevant fields
        # Ideally we update everything needed.
        
        query = '''
            UPDATE appointment 
            SET status = ?, rejection_reason = ?, notification_msg = ?, notification_read = 0
        '''
        params = [status, rejection_reason, notification_msg]
        
        if status == 'Completed':
            query += ', symptoms = ?, diagnosis = ?, advice = ?, prescription = ?, completed_at = ?'
            params.extend([symptoms, diagnosis, advice, prescription_filename, completed_at])
            
        query += ' WHERE id = ?'
        params.append(appointment_id)
        
        db.execute(query, params)
        db.commit()
        flash(f'Appointment {status}!', 'success')
    
    return redirect(url_for('appointments'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        db = get_db()
        if current_user.role == 'patient':
            age = request.form.get('age')
            gender = request.form.get('gender')
            blood_group = request.form.get('blood_group')
            contact_number = request.form.get('contact_number')
            address = request.form.get('address')
            
            db.execute('''
                UPDATE user 
                SET age=?, gender=?, blood_group=?, contact_number=?, address=? 
                WHERE id=?
            ''', (age, gender, blood_group, contact_number, address, current_user.id))
            
            # Update current_user object to reflect changes immediately in session if needed, 
            # though flask-login reloads user on next request usually.
            
        elif current_user.role == 'doctor':
            specialization = request.form.get('specialization')
            experience_years = request.form.get('experience_years')
            contact_number = request.form.get('contact_number')
            available_time = request.form.get('available_time')
            available_slots = request.form.get('available_slots')
            
            db.execute('''
                UPDATE user 
                SET specialization=?, experience_years=?, contact_number=?, available_time=?, available_slots=? 
                WHERE id=?
            ''', (specialization, experience_years, contact_number, available_time, available_slots, current_user.id))
        
        db.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html')

@app.route('/view_patient/<int:patient_id>')
@login_required
def view_patient_profile(patient_id):
    if current_user.role != 'doctor':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    db = get_db()
    # Fetch patient
    patient_row = db.execute('SELECT * FROM user WHERE id = ?', (patient_id,)).fetchone()
    if not patient_row:
        flash('Patient not found.', 'danger')
        return redirect(url_for('dashboard'))

    # Fetch all appointments for this patient (history)
    # We need doctor name for the template which expects appt.doctor.name. 
    # Let's join with doctor to get doctor name.
    appointments = db.execute('''
        SELECT a.*, d.name as doctor_name 
        FROM appointment a 
        JOIN user d ON a.doctor_id = d.id 
        WHERE a.patient_id = ? 
        ORDER BY a.date DESC
    ''', (patient_id,)).fetchall()
    
    # Template expects a User object or dict access. 
    # Our assignments are dict-like via sqlite3.Row so {{ patient.name }} works if we pass the row.
    # However, for appointments, template accesses {{ appt.doctor.name }}. 
    # The query returns `doctor_name`.
    # I need to update the template or transform the data.
    # Updating template is safer. But wait, I'm refactoring backend.
    # Let's mock the structure or update the template later?
    # Actually, in Jinja, {{ appt.doctor.name }} will fail on a Row object.
    # I should update the template to use {{ appt.doctor_name }} or similar.
    # OR I can construct a list of objects.
    # For now, let's keep it simple and just return the data, but I'll have to warn that templates might need adjustment.
    # Wait, the prompt implies "replace them with sqlite", but usually this implies keeping functionality.
    # If I break templates, it's bad.
    # Reviewing `patient_profile_view.html`: `{{ appt.doctor.name }}`
    # I can transform `appointments` list to have a nested structure or just `doctor_name`.
    # Let's transform it here to minimize template impact if possible, OR just update template.
    # Updating template is cleaner.
    
    return render_template('patient_profile_view.html', patient=patient_row, appointments=appointments)

# Admin Routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('dashboard'))
        
    db = get_db()
    total_patients = db.execute("SELECT COUNT(*) FROM user WHERE role='patient'").fetchone()[0]
    total_doctors = db.execute("SELECT COUNT(*) FROM user WHERE role='doctor'").fetchone()[0]
    total_appointments = db.execute("SELECT COUNT(*) FROM appointment").fetchone()[0]
    
    return render_template('admin_dashboard.html', 
                         total_patients=total_patients,
                         total_doctors=total_doctors,
                         total_appointments=total_appointments)

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('dashboard'))
    
    db = get_db()
    users = db.execute('SELECT * FROM user').fetchall()
    return render_template('admin_users.html', users=users)

@app.route('/admin/toggle_user/<int:user_id>')
@login_required
def toggle_user_status(user_id):
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('dashboard'))
        
    if user_id == current_user.id:
        flash('You cannot deactivate yourself.', 'warning')
        return redirect(url_for('admin_users'))
        
    db = get_db()
    # Toggle logic: fetch, flip, update
    user = db.execute('SELECT is_active, name FROM user WHERE id = ?', (user_id,)).fetchone()
    if user:
        new_status = not user['is_active']
        db.execute('UPDATE user SET is_active = ? WHERE id = ?', (new_status, user_id))
        db.commit()
        status_msg = 'activated' if new_status else 'deactivated'
        flash(f'User {user["name"]} has been {status_msg}.', 'success')
        
    return redirect(url_for('admin_users'))

if __name__ == '__main__':
    # Ensure init_db or similar if needed, but we assume DB exists
    app.run(debug=True)
