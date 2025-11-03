# app.py
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime, date, timedelta
from PIL import Image
import base64
import io
import pickle

# =============================
# Flask App Configuration
# =============================
app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =============================
# Philippines Time Helper Functions
# =============================
def get_ph_time():
    """Get current Philippines time"""
    return datetime.now()

def get_ph_date():
    """Get current Philippines date"""
    return get_ph_time().date()

def format_time_display(dt, format_type='12h'):
    """Consistent time formatting across the application"""
    if format_type == '12h':
        return dt.strftime('%I:%M %p')  # 12-hour format with AM/PM
    else:
        return dt.strftime('%H:%M')     # 24-hour format

# =============================
# Database Models - USING PHILIPPINES TIME
# =============================
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    department = db.Column(db.String(100))
    position = db.Column(db.String(100))
    face_encoding = db.Column(db.LargeBinary, nullable=False)
    image_path = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=get_ph_time)

    def __repr__(self):
        return f'<Employee {self.name} ({self.employee_id})>'

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    timestamp = db.Column(db.DateTime, default=get_ph_time, nullable=False)

    def __repr__(self):
        return f'<Attendance {self.employee_id} {self.status} at {self.timestamp}>'

# =============================
# Helper Functions
# =============================
def encode_face_encoding(encoding):
    """Convert numpy array to bytes for storage"""
    return pickle.dumps(encoding)

def decode_face_encoding(encoding_bytes):
    """Convert bytes back to numpy array"""
    if encoding_bytes:
        return pickle.loads(encoding_bytes)
    return None

def has_recent_attendance(employee_id, action, threshold_minutes=2):
    """Check if employee has recent attendance record to prevent duplicates"""
    ph_now = get_ph_time()
    threshold = ph_now - timedelta(minutes=threshold_minutes)
    
    recent_record = Attendance.query.filter(
        Attendance.employee_id == employee_id,
        Attendance.status == ("Time In" if action == "time_in" else "Time Out"),
        Attendance.timestamp >= threshold
    ).first()
    
    return recent_record is not None

# =============================
# Template Filters - SIMPLIFIED FOR LOCAL TIME
# =============================
@app.template_filter('format_time_display')
def template_format_time_display(time_str):
    """Format time string for display in templates"""
    if not time_str:
        return ""
    
    try:
        if isinstance(time_str, str) and ':' in time_str:
            # Handle "HH:MM:SS" format
            time_parts = time_str.split(':')
            if len(time_parts) >= 2:
                hours = int(time_parts[0])
                minutes = time_parts[1]
                
                if hours >= 12:
                    am_pm = "PM"
                    if hours > 12:
                        hours -= 12
                else:
                    am_pm = "AM"
                    if hours == 0:
                        hours = 12
                
                return f"{hours}:{minutes} {am_pm}"
        return str(time_str)
    except Exception as e:
        print(f"Time formatting error: {e}")
        return str(time_str)

@app.template_filter('format_time_24h')
def template_format_time_24h(time_str):
    """Format time string in 24-hour format for badges"""
    if not time_str:
        return ""
    
    try:
        if isinstance(time_str, str) and ':' in time_str:
            # Handle "HH:MM:SS" format - just take HH:MM part
            time_parts = time_str.split(':')
            if len(time_parts) >= 2:
                return f"{time_parts[0]}:{time_parts[1]}"
        return str(time_str)
    except Exception as e:
        print(f"Time formatting error: {e}")
        return str(time_str)

@app.template_filter('calculate_duration')
def calculate_duration(time_in_str, time_out_str):
    """Calculate duration between time in and time out"""
    if not time_in_str or not time_out_str:
        return ""
    
    try:
        # Parse times from "HH:MM:SS" format
        def parse_time(time_str):
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2]) if len(parts) > 2 else 0
            return hours, minutes, seconds
        
        h1, m1, s1 = parse_time(time_in_str)
        h2, m2, s2 = parse_time(time_out_str)
        
        # Calculate total minutes
        total_minutes1 = h1 * 60 + m1
        total_minutes2 = h2 * 60 + m2
        
        # Handle overnight shifts
        if total_minutes2 < total_minutes1:
            total_minutes2 += 24 * 60  # Add 24 hours
        
        duration_minutes = total_minutes2 - total_minutes1
        
        hours = duration_minutes // 60
        minutes = duration_minutes % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"
            
    except Exception as e:
        print(f"Duration calculation error: {e}")
        return "N/A"

# =============================
# ROUTES
# =============================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_webcam', methods=['POST'])
def register_webcam():
    data = request.get_json()
    name = data.get('name', '').strip()
    employee_id = data.get('employee_id', '').strip()
    department = data.get('department', '').strip()
    position = data.get('position', '').strip()
    image_data = data.get('image')

    # Validation
    if not name or not employee_id or not image_data:
        return jsonify({"status": "fail", "message": "Missing required fields!"}), 400

    # Decode base64 image
    try:
        img_bytes = base64.b64decode(image_data.split(',')[1])
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        image_np = np.array(img)
        rgb_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    except Exception as e:
        return jsonify({"status": "fail", "message": "Invalid image data!"}), 400

    # Encode face
    encodings = face_recognition.face_encodings(rgb_image)
    if len(encodings) == 0:
        return jsonify({"status": "fail", "message": "No face detected! Try again."}), 400
    
    if len(encodings) > 1:
        return jsonify({"status": "fail", "message": "Multiple faces detected! Please register one person at a time."}), 400
        
    face_encoding = encodings[0]

    # Save image
    image_path = os.path.join(UPLOAD_FOLDER, f"{employee_id}.jpg")
    
    try:
        img.save(image_path, 'JPEG', quality=95)
    except Exception as e:
        return jsonify({"status": "fail", "message": f"Failed to save image: {str(e)}"}), 500

    # Save employee to DB
    try:
        existing = Employee.query.filter_by(employee_id=employee_id).first()
        if existing:
            if os.path.exists(image_path):
                os.remove(image_path)
            return jsonify({"status": "fail", "message": "Employee ID already exists!"}), 400

        new_employee = Employee(
            name=name,
            employee_id=employee_id,
            department=department,
            position=position,
            face_encoding=encode_face_encoding(face_encoding),
            image_path=image_path
        )
        db.session.add(new_employee)
        db.session.commit()
        
        return jsonify({"status": "success", "message": f"Employee {name} registered successfully ✅"})
        
    except Exception as e:
        db.session.rollback()
        if os.path.exists(image_path):
            os.remove(image_path)
        return jsonify({"status": "fail", "message": f"Database error: {str(e)}"}), 500

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

# =============================
# ROUTE: Attendance Action - IMPROVED FACE RECOGNITION LOGIC
# =============================
@app.route('/attendance_action', methods=['POST'])
def attendance_action():
    data = request.get_json()
    action = data.get('action')
    image_data = data.get('image')

    if not action or action not in ['time_in', 'time_out']:
        return jsonify({"message": "Invalid action!"}), 400
        
    if not image_data:
        return jsonify({"message": "Image data missing!"}), 400

    # Use current Philippines time
    exact_ph_time = get_ph_time()

    # Decode image
    try:
        img_bytes = base64.b64decode(image_data.split(',')[1])
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        frame = np.array(img)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    except Exception as e:
        return jsonify({"message": "Invalid image data!"}), 400

    # Get all employees
    employees = Employee.query.all()
    if not employees:
        return jsonify({"message": "No registered employees!"}), 400

    # Prepare known face data
    known_encodings = []
    known_ids = []
    known_names = []
    
    for emp in employees:
        encoding = decode_face_encoding(emp.face_encoding)
        if encoding is not None:
            known_encodings.append(encoding)
            known_ids.append(emp.employee_id)
            known_names.append(emp.name)

    if not known_encodings:
        return jsonify({"message": "No valid face encodings found in database!"}), 400

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if len(face_encodings) == 0:
        current_time = format_time_display(exact_ph_time, '12h')
        no_face_message = f"No Face Detected\nPlease try again\n{current_time}"
        return jsonify({"message": no_face_message})  # REMOVED 400 status

    # STRICTER FACE RECOGNITION SETTINGS
    tolerance = 0.5  # Lower tolerance = more strict (default is 0.6)
    
    recognized_employees = []
    unknown_faces_detected = False
    match_found = False

    for face_encoding in face_encodings:
        # Calculate face distances to all known faces
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        
        if len(face_distances) == 0:
            continue
            
        # Find the best match (lowest distance)
        best_match_index = np.argmin(face_distances)
        best_distance = face_distances[best_match_index]
        
        # Convert distance to confidence (0-100%)
        confidence = (1 - best_distance) * 100
        
        print(f"Best match distance: {best_distance:.4f}, Confidence: {confidence:.2f}%")
        
        # STRICT MATCHING: Must meet tolerance threshold
        if best_distance <= tolerance:
            # Valid match found
            match_found = True
            emp_id = known_ids[best_match_index]
            emp_name = known_names[best_match_index]
            
            # Check for recent attendance to prevent duplicates
            if has_recent_attendance(emp_id, action):
                status_text = "Time In" if action == "time_in" else "Time Out"
                current_time = format_time_display(exact_ph_time, '12h')
                duplicate_message = f"Duplicate {status_text}\nfor {emp_name}\n{current_time}"
                recognized_employees.append(duplicate_message)
                continue
            
            status_text = "Time In" if action == "time_in" else "Time Out"
            current_time = format_time_display(exact_ph_time, '12h')
            
            # Save attendance
            try:
                new_log = Attendance(
                    employee_id=emp_id,
                    name=emp_name,
                    status=status_text,
                    timestamp=exact_ph_time
                )
                db.session.add(new_log)
                db.session.commit()
                
                success_message = f"{status_text}\nfor {emp_name}\n{current_time}"
                recognized_employees.append(success_message)
                
            except Exception as e:
                db.session.rollback()
                error_message = f"Error\nfor {emp_name}\n{current_time}"
                recognized_employees.append(error_message)
        else:
            # Face detected but doesn't match any registered employee
            unknown_faces_detected = True
            current_time = format_time_display(exact_ph_time, '12h')
            no_match_message = f"Face Not Recognized\nPlease register first\n{current_time}"
            # Don't add to recognized_employees yet

    # Process results
    if match_found and recognized_employees:
        # We have successful recognitions
        final_message = "\n\n".join(recognized_employees)
        return jsonify({"message": final_message})
    elif unknown_faces_detected:
        # Face detected but not recognized
        current_time = format_time_display(exact_ph_time, '12h')
        return jsonify({"message": f"Face Not Recognized\nPlease register first\n{current_time}"})
    elif recognized_employees:
        # Only duplicates or errors
        final_message = "\n\n".join(recognized_employees)
        return jsonify({"message": final_message})
    else:
        # No face matched or other issues
        current_time = format_time_display(exact_ph_time, '12h')
        return jsonify({"message": f"No Match\nNo employee found\n{current_time}"})

@app.route('/admin')
def admin():
    try:
        employees = Employee.query.all()
        return render_template('admin.html', employees=employees)
    except Exception as e:
        print(f"Database error: {e}")
        return render_template('admin.html', employees=[])

# =============================
# ROUTE: Admin Dashboard - PROPER PH TIME LOGIC
# =============================
@app.route('/admin_dashboard')
def admin_dashboard():
    # Get today's Philippines date for filtering
    today = get_ph_date()
    
    # Calculate real-time statistics using Philippines time
    total_employees = Employee.query.count()
    
    # Count staff who have timed in today (using local time)
    present_today = db.session.query(Attendance.employee_id).filter(
        db.func.date(Attendance.timestamp) == today,
        Attendance.status == "Time In"
    ).distinct().count()
    
    # Count today's time ins and time outs
    time_in_count = Attendance.query.filter(
        db.func.date(Attendance.timestamp) == today,
        Attendance.status == "Time In"
    ).count()
    
    time_out_count = Attendance.query.filter(
        db.func.date(Attendance.timestamp) == today,
        Attendance.status == "Time Out"
    ).count()
    
    # Get recent activity for today with LOCAL time
    recent_activity = Attendance.query.filter(
        db.func.date(Attendance.timestamp) == today
    ).order_by(Attendance.timestamp.desc()).limit(10).all()
    
    # Get all attendance records and group by employee and date
    all_attendance = Attendance.query.order_by(Attendance.timestamp.asc()).all()
    attendance_dict = {}
    
    for record in all_attendance:
        # All times are already Philippines time
        record_date = record.timestamp.date()
        record_time = record.timestamp.strftime("%H:%M:%S")
        employee_key = f"{record.employee_id}_{record_date}"
        
        if employee_key not in attendance_dict:
            attendance_dict[employee_key] = {
                "employee_id": record.employee_id,
                "name": record.name,
                "date": record_date.strftime("%Y-%m-%d"),
                "time_in": None,
                "time_out": None
            }
        
        # Update time_in if this is a Time In record
        if record.status == "Time In":
            current_time_in = attendance_dict[employee_key]["time_in"]
            if current_time_in is None:
                attendance_dict[employee_key]["time_in"] = record_time
            else:
                # Keep the earliest time_in
                current_time = datetime.strptime(current_time_in, "%H:%M:%S").time()
                new_time = record.timestamp.time()
                if new_time < current_time:
                    attendance_dict[employee_key]["time_in"] = record_time
        
        # Update time_out if this is a Time Out record  
        elif record.status == "Time Out":
            current_time_out = attendance_dict[employee_key]["time_out"]
            if current_time_out is None:
                attendance_dict[employee_key]["time_out"] = record_time
            else:
                # Keep the latest time_out
                current_time = datetime.strptime(current_time_out, "%H:%M:%S").time()
                new_time = record.timestamp.time()
                if new_time > current_time:
                    attendance_dict[employee_key]["time_out"] = record_time
    
    # Convert to list for template
    attendance_data = list(attendance_dict.values())
    
    return render_template("admin_dashboard.html", 
                         attendance_data=attendance_data,
                         employees_count=total_employees,
                         present_today=present_today,
                         time_in_count=time_in_count,
                         time_out_count=time_out_count,
                         recent_activity=recent_activity)

# =============================
# API Endpoints - PHILIPPINES TIME ONLY
# =============================
@app.route('/api/dashboard_stats')
def api_dashboard_stats():
    today = get_ph_date()
    
    stats = {
        'total_employees': Employee.query.count(),
        'present_today': db.session.query(Attendance.employee_id).filter(
            db.func.date(Attendance.timestamp) == today,
            Attendance.status == "Time In"
        ).distinct().count(),
        'time_in_count': Attendance.query.filter(
            db.func.date(Attendance.timestamp) == today,
            Attendance.status == "Time In"
        ).count(),
        'time_out_count': Attendance.query.filter(
            db.func.date(Attendance.timestamp) == today,
            Attendance.status == "Time Out"
        ).count(),
        'current_time': get_ph_time().strftime('%Y-%m-%d %I:%M:%S %p')
    }
    
    return jsonify(stats)

@app.route('/api/recent_activity')
def api_recent_activity():
    today = get_ph_date()
    recent_activity = Attendance.query.filter(
        db.func.date(Attendance.timestamp) == today
    ).order_by(Attendance.timestamp.desc()).limit(10).all()
    
    activity_list = []
    for activity in recent_activity:
        activity_list.append({
            'employee_id': activity.employee_id,
            'name': activity.name,
            'status': activity.status,
            'timestamp': activity.timestamp,
            'time_display': format_time_display(activity.timestamp, '12h')
        })
    
    return jsonify(activity_list)

@app.route('/delete_employee/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        employee = Employee.query.filter_by(employee_id=employee_id).first()
        if not employee:
            return jsonify({"status": "fail", "message": "Employee not found!"}), 404
        
        # Delete associated attendance records
        Attendance.query.filter_by(employee_id=employee_id).delete()
        
        # Delete image file
        if employee.image_path and os.path.exists(employee.image_path):
            try:
                os.remove(employee.image_path)
            except Exception as e:
                print(f"Warning: Could not delete image file: {e}")
        
        db.session.delete(employee)
        db.session.commit()
        
        return jsonify({"status": "success", "message": "Employee deleted successfully"})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "fail", "message": f"Error deleting employee: {str(e)}"}), 500

@app.route('/export')
def export():
    try:
        import pandas as pd
        from flask import send_file
        
        records = Attendance.query.all()
        
        # Convert times to proper Philippines time format for export
        data = []
        for r in records:
            # All times are already Philippines time, format them properly
            data.append({
                "Employee ID": r.employee_id,
                "Name": r.name,
                "Date": r.timestamp.strftime('%Y-%m-%d'),
                "Time": r.timestamp.strftime('%I:%M:%S %p'),
                "Status": r.status
            })

        df = pd.DataFrame(data)
        
        # Create exports directory if it doesn't exist
        export_dir = "exports"
        os.makedirs(export_dir, exist_ok=True)
        
        # Generate filename with timestamp
        export_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_filename = f"attendance_export_{export_timestamp}.xlsx"
        export_path = os.path.join(export_dir, export_filename)
        
        # Export to Excel
        df.to_excel(export_path, index=False, sheet_name='Attendance Records')
        
        # Return the file for download
        return send_file(export_path, as_attachment=True, download_name=export_filename)
        
    except ImportError:
        return "Export failed: pandas or openpyxl not installed. Install with: pip install pandas openpyxl", 500
    except Exception as e:
        print(f"Export error: {e}")
        return f"Export failed: {str(e)}", 500

# =============================
# Initialize database when app starts
# =============================
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

# =============================
# ROUTE: Database Viewer
# =============================
@app.route('/view_database')
def view_database():
    """Simple database viewer to see all data"""
    try:
        employees = Employee.query.all()
        attendance = Attendance.query.order_by(Attendance.timestamp.desc()).all()
        
        # Get statistics
        total_employees = len(employees)
        total_attendance = len(attendance)
        
        return render_template('database_viewer.html', 
                             employees=employees, 
                             attendance=attendance,
                             total_employees=total_employees,
                             total_attendance=total_attendance)
    except Exception as e:
        return f"Error accessing database: {str(e)}", 500

# =============================
# Run App
# =============================
if __name__ == "__main__":
    app.run(debug=True)