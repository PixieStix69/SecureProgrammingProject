import os
import sqlite3
from flask import Flask, render_template, request, Response, redirect, url_for, flash, session, send_from_directory, abort, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.secret_key = 'trump123'  # Set a secure secret key

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Configure the SQLite database
db_path = os.path.join(os.path.dirname(__file__), 'trump.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Example Model (Table)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Function to run the SQL script if database doesn't exist
def initialize_database():
    if not os.path.exists('trump.db'):
        with sqlite3.connect('trump.db') as conn:
            cursor = conn.cursor()
            with open('trump.sql', 'r') as sql_file:
                sql_script = sql_file.read()
            cursor.executescript(sql_script)
            print("Database initialized with script.")

# Existing routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quotes')
def quotes():
    return render_template('quotes.html')

@app.route('/sitemap')
def sitemap():
    return render_template('sitemap.html')
    
@app.route('/admin_panel')
def admin_panel():
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please log in to access the admin panel', 'error')
        return redirect(url_for('login'))
    
    return render_template('admin_panel.html')

# route to handle redirects based on the destination query parameter
@app.route('/redirect', methods=['GET'])
def redirect_handler():
    destination = request.args.get('destination')
    
    # whitelist of allowed domains
    allowed_domains = ['127.0.0.1:5000', 'localhost:5000']
    
    if destination:
        # parse the destination URL
        from urllib.parse import urlparse # import urlparse
        parsed = urlparse(destination) # parse the destination URL
        
        # only allow relative URLs or whitelisted domains 
        if not parsed.netloc:  # relative URL
            return redirect(destination)
        elif parsed.netloc in allowed_domains:  # whitelisted domain
            return redirect(destination)
        else:
            return "Unauthorized redirect attempt!", 403
    else:
        return "Invalid destination", 400


@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        username = request.form['username']
        comment_text = request.form['comment']

        # Insert comment into the database
        insert_comment_query = text("INSERT INTO comments (username, text) VALUES (:username, :text)")
        db.session.execute(insert_comment_query, {'username': username, 'text': comment_text})
        db.session.commit()
        return redirect(url_for('comments'))

    # Retrieve all comments to display
    comments_query = text("SELECT username, text FROM comments")
    comments = db.session.execute(comments_query).fetchall()
    return render_template('comments.html', comments=comments)

request_times = {}

@app.route('/download', methods=['GET'])
def download():
    # Rate Limitng - 10 requests per minute per IP
    ip = request.remote_addr
    current_time = time.time()

    # Get recent requests for this IP
    recent_requests = [t for t in request_times.get(ip, []) if current_time - t < 60]

    if len(recent_requests) >= 10:
        return "Too many requests, please try again later", 429

    # Add current request
    if ip not in request_times:
        request_times[ip] = []
    request_times[ip].append(current_time)

    # Get the filename from the query parameter
    file_name = request.args.get('file', '')

    # Set base directory to where your docs folder is located
    base_directory = os.path.join(os.path.dirname(__file__), 'docs')

    # Construct the file path to attempt to read the file
    file_path = os.path.abspath(os.path.join(base_directory, file_name))

    # Try to open the file securely, send_file is a more secure and memory efficient way to send files
    try:
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404
    except PermissionError:
        return "Permission denied while accessing the file", 403
        
@app.route('/downloads', methods=['GET'])
def download_page():
    return render_template('download.html')


@app.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Check if user is authorized to access this profile
    if session['user_id'] != user_id:
        return "Unauthorized access attempt!", 403
    
    query_user = text(f"SELECT * FROM users WHERE id = {user_id}")
    user = db.session.execute(query_user).fetchone()

    if user:
        query_cards = text(f"SELECT * FROM carddetail WHERE id = {user_id}")
        cards = db.session.execute(query_cards).fetchall()
        return render_template('profile.html', user=user, cards=cards)
    else:
        return "User not found or unauthorized access.", 403
from flask import request

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    return render_template('search.html', query=query)

@app.route('/forum')
def forum():
    return render_template('forum.html')

# Simple storage for failed attempts
failed_attempts = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ip = request.remote_addr
        current_time = datetime.now()
        
        # Check for too many attempts
        if ip in failed_attempts:
            last_attempt, attempts = failed_attempts[ip]
            if current_time - last_attempt < timedelta(minutes=10):
                if attempts >= 3:
                    return render_template('login.html', 
                                        error='Too many attempts. Please try again later.')
            else:
                # Reset counter if last attempt was more than 10 minutes ago
                failed_attempts[ip] = (current_time, 0)

        username = request.form['username']
        password = request.form['password']
        query = text(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
        user = db.session.execute(query).fetchone()

        if user:
            # Reset failed attempts on success
            if ip in failed_attempts:
                del failed_attempts[ip]
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('profile', user_id=user.id))
        else:
            # Record failed attempt
            if ip in failed_attempts:
                failed_attempts[ip] = (current_time, failed_attempts[ip][1] + 1)
            else:
                failed_attempts[ip] = (current_time, 1)
            
            # Error message
            return render_template('login.html', 
                                error='Invalid username or password')

    return render_template('login.html')





# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user session
    flash('You were successfully logged out', 'success')
    return redirect(url_for('index'))
    
from flask import session


if __name__ == '__main__':
    initialize_database()  # Initialize the database on application startup if it doesn't exist
    with app.app_context():
        db.create_all()  # Create tables based on models if they don't already exist
    app.run(debug=True)
