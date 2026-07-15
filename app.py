from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database initialization
DATABASE = 'news.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database"""
    conn = get_db()
    c = conn.cursor()
    
    # Create categories table
    c.execute('''CREATE TABLE IF NOT EXISTS categories
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create news table
    c.execute('''CREATE TABLE IF NOT EXISTS news
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  description TEXT NOT NULL,
                  image TEXT,
                  category_id INTEGER NOT NULL,
                  author TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  is_breaking BOOLEAN DEFAULT 0,
                  is_featured BOOLEAN DEFAULT 0,
                  FOREIGN KEY(category_id) REFERENCES categories(id))''')
    
    conn.commit()
    conn.close()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize database on app start
with app.app_context():
    init_db()
    # Add default categories if they don't exist
    conn = get_db()
    c = conn.cursor()
    default_categories = [
        'Breaking News', 'National News', 'International News', 'Politics',
        'Crime', 'Business', 'Technology', 'Sports', 'Entertainment',
        'Education', 'Health'
    ]
    for category in default_categories:
        try:
            c.execute('INSERT INTO categories (name) VALUES (?)', (category,))
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()

# Routes

@app.route('/')
def home():
    """Home page"""
    conn = get_db()
    c = conn.cursor()
    
    # Get breaking news (limit 3)
    c.execute('''SELECT n.*, c.name as category_name FROM news n
                 JOIN categories c ON n.category_id = c.id
                 WHERE n.is_breaking = 1
                 ORDER BY n.created_at DESC LIMIT 3''')
    breaking_news = c.fetchall()
    
    # Get featured news (limit 6)
    c.execute('''SELECT n.*, c.name as category_name FROM news n
                 JOIN categories c ON n.category_id = c.id
                 WHERE n.is_featured = 1
                 ORDER BY n.created_at DESC LIMIT 6''')
    featured_news = c.fetchall()
    
    # Get latest news (limit 8)
    c.execute('''SELECT n.*, c.name as category_name FROM news n
                 JOIN categories c ON n.category_id = c.id
                 ORDER BY n.created_at DESC LIMIT 8''')
    latest_news = c.fetchall()
    
    # Get trending news - most recent from each category
    c.execute('''SELECT n.*, c.name as category_name FROM news n
                 JOIN categories c ON n.category_id = c.id
                 ORDER BY n.created_at DESC LIMIT 5''')
    trending_news = c.fetchall()
    
    conn.close()
    
    return render_template('index.html',
                         breaking_news=breaking_news,
                         featured_news=featured_news,
                         latest_news=latest_news,
                         trending_news=trending_news)

@app.route('/category/<int:category_id>')
def category(category_id):
    """Category page"""
    conn = get_db()
    c = conn.cursor()
    
    # Get category name
    c.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
    category_obj = c.fetchone()
    
    if not category_obj:
        conn.close()
        return redirect(url_for('home'))
    
    # Get news for this category
    c.execute('''SELECT n.*, c.name as category_name FROM news n
                 JOIN categories c ON n.category_id = c.id
                 WHERE n.category_id = ?
                 ORDER BY n.created_at DESC''', (category_id,))
    news_list = c.fetchall()
    
    conn.close()
    
    return render_template('category.html', category=category_obj, news_list=news_list)

@app.route('/news/<int:news_id>')
def news_detail(news_id):
    """News detail page"""
    conn = get_db()
    c = conn.cursor()
    
    # Get news
    c.execute('''SELECT n.*, c.name as category_name FROM news n
                 JOIN categories c ON n.category_id = c.id
                 WHERE n.id = ?''', (news_id,))
    news = c.fetchone()
    
    if not news:
        conn.close()
        return redirect(url_for('home'))
    
    # Get related news
    c.execute('''SELECT n.*, c.name as category_name FROM news n
                 JOIN categories c ON n.category_id = c.id
                 WHERE n.category_id = ? AND n.id != ?
                 ORDER BY n.created_at DESC LIMIT 4''', (news['category_id'], news_id))
    related_news = c.fetchall()
    
    conn.close()
    
    return render_template('news_detail.html', news=news, related_news=related_news)

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    conn = get_db()
    c = conn.cursor()
    
    # Get statistics
    c.execute('SELECT COUNT(*) as count FROM news')
    total_news = c.fetchone()['count']
    
    c.execute('SELECT COUNT(*) as count FROM categories')
    total_categories = c.fetchone()['count']
    
    # Get recent news
    c.execute('''SELECT n.*, c.name as category_name FROM news n
                 JOIN categories c ON n.category_id = c.id
                 ORDER BY n.created_at DESC LIMIT 10''')
    recent_news = c.fetchall()
    
    # Get all categories
    c.execute('SELECT * FROM categories ORDER BY name')
    categories = c.fetchall()
    
    conn.close()
    
    return render_template('admin/dashboard.html',
                         total_news=total_news,
                         total_categories=total_categories,
                         recent_news=recent_news,
                         categories=categories)

@app.route('/admin/news/add', methods=['GET', 'POST'])
def admin_add_news():
    """Add news"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        author = request.form.get('author')
        is_breaking = request.form.get('is_breaking') == 'on'
        is_featured = request.form.get('is_featured') == 'on'
        
        # Handle file upload
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S_')
                filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename
        
        # Insert into database
        conn = get_db()
        c = conn.cursor()
        c.execute('''INSERT INTO news (title, description, image, category_id, author, is_breaking, is_featured)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (title, description, image_filename, category_id, author, is_breaking, is_featured))
        conn.commit()
        conn.close()
        
        return redirect(url_for('admin_dashboard'))
    
    # Get categories
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM categories ORDER BY name')
    categories = c.fetchall()
    conn.close()
    
    return render_template('admin/add_news.html', categories=categories)

@app.route('/admin/news/edit/<int:news_id>', methods=['GET', 'POST'])
def admin_edit_news(news_id):
    """Edit news"""
    conn = get_db()
    c = conn.cursor()
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        author = request.form.get('author')
        is_breaking = request.form.get('is_breaking') == 'on'
        is_featured = request.form.get('is_featured') == 'on'
        
        # Get existing news
        c.execute('SELECT * FROM news WHERE id = ?', (news_id,))
        news = c.fetchone()
        image_filename = news['image']
        
        # Handle file upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                # Delete old image
                if image_filename and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], image_filename)):
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
                
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S_')
                filename = timestamp + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_filename = filename
        
        # Update database
        c.execute('''UPDATE news SET title = ?, description = ?, image = ?, category_id = ?, author = ?, is_breaking = ?, is_featured = ?
                     WHERE id = ?''',
                  (title, description, image_filename, category_id, author, is_breaking, is_featured, news_id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('admin_dashboard'))
    
    # Get news
    c.execute('SELECT * FROM news WHERE id = ?', (news_id,))
    news = c.fetchone()
    
    if not news:
        conn.close()
        return redirect(url_for('admin_dashboard'))
    
    # Get categories
    c.execute('SELECT * FROM categories ORDER BY name')
    categories = c.fetchall()
    conn.close()
    
    return render_template('admin/edit_news.html', news=news, categories=categories)

@app.route('/admin/news/delete/<int:news_id>')
def admin_delete_news(news_id):
    """Delete news"""
    conn = get_db()
    c = conn.cursor()
    
    # Get news
    c.execute('SELECT * FROM news WHERE id = ?', (news_id,))
    news = c.fetchone()
    
    if news:
        # Delete image
        if news['image'] and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], news['image'])):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], news['image']))
        
        # Delete from database
        c.execute('DELETE FROM news WHERE id = ?', (news_id,))
        conn.commit()
    
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/category/add', methods=['GET', 'POST'])
def admin_add_category():
    """Add category"""
    if request.method == 'POST':
        name = request.form.get('name')
        
        conn = get_db()
        c = conn.cursor()
        try:
            c.execute('INSERT INTO categories (name) VALUES (?)', (name,))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        conn.close()
        
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/add_category.html')

@app.route('/admin/category/delete/<int:category_id>')
def admin_delete_category(category_id):
    """Delete category"""
    conn = get_db()
    c = conn.cursor()
    
    # Check if category has news
    c.execute('SELECT COUNT(*) as count FROM news WHERE category_id = ?', (category_id,))
    count = c.fetchone()['count']
    
    if count == 0:
        c.execute('DELETE FROM categories WHERE id = ?', (category_id,))
        conn.commit()
    
    conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    if request.method == 'POST':
        # In a real app, you'd send an email or save to database
        # For now, just redirect
        return redirect(url_for('home'))
    
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
