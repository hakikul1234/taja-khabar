# TAJA KHABAR NEWS 24 - Modern News Website

A modern, responsive news website built with **Python Flask**, **HTML5**, **CSS3**, and **JavaScript**. Featuring a professional news portal with a simple admin panel for content management.

**Motto:** "Sach Sab Se Aage" (Truth Comes First)

## 🎯 Features

### Public Website
- **Home Page** - Latest, breaking, featured, and trending news
- **Multiple Categories** - Breaking News, National, International, Politics, Crime, Business, Technology, Sports, Entertainment, Education, Health
- **News Detail Pages** - Full article view with related news
- **Category Pages** - View all news in specific category
- **About Us** - Website information and mission
- **Contact Us** - Contact form with information
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile devices
- **Breaking News Ticker** - Scrolling ticker for breaking stories
- **Trending News Widget** - Sidebar with trending news
- **Advertisement Placeholders** - Ready for ad integration

### Admin Panel
- **Add News** - Create new articles with image upload
- **Edit News** - Modify existing articles
- **Delete News** - Remove articles
- **Mark Breaking News** - Highlight important stories
- **Mark Featured News** - Feature stories on homepage
- **Category Management** - Add/delete news categories
- **Dashboard** - Statistics and recent news overview
- **Image Upload** - Upload and manage article images

## 📊 Project Structure

```
project/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── run.sh                    # Server startup script
├── news.db                   # SQLite database (created on first run)
├── templates/
│   ├── base.html            # Base template with header/footer
│   ├── index.html           # Homepage
│   ├── category.html        # Category listing page
│   ├── news_detail.html     # Single news article page
│   ├── about.html           # About Us page
│   ├── contact.html         # Contact Us page
│   └── admin/
│       ├── dashboard.html   # Admin dashboard
│       ├── add_news.html    # Add news form
│       ├── edit_news.html   # Edit news form
│       └── add_category.html # Add category form
├── static/
│   ├── css/
│   │   ├── style.css        # Main website styles
│   │   └── admin.css        # Admin panel styles
│   └── uploads/             # Uploaded news images (created on first run)
└── README.md               # This file
```

## 🗄️ Database Schema

### Categories Table
- `id` - Primary key
- `name` - Category name (unique)
- `created_at` - Creation timestamp

### News Table
- `id` - Primary key
- `title` - Article title
- `description` - Article content
- `image` - Image filename
- `category_id` - Foreign key to categories
- `author` - Author name
- `created_at` - Creation timestamp
- `is_breaking` - Boolean flag for breaking news
- `is_featured` - Boolean flag for featured news

## 🚀 Installation & Setup

### Requirements
- Python 3.7+
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

Alternatively, use the provided script:
```bash
chmod +x run.sh
./run.sh
```

### Step 3: Access the Application
- **Website:** http://localhost:5000/
- **Admin Panel:** http://localhost:5000/admin
- **Add News:** http://localhost:5000/admin/news/add
- **Add Category:** http://localhost:5000/admin/category/add

## 📝 Using the Admin Panel

### Adding a News Article
1. Go to Admin Panel → "Add News"
2. Fill in the article details:
   - **Title** - Article headline
   - **Description** - Full article content
   - **Category** - Select from dropdown
   - **Author** - Author name
   - **Image** - Upload news image (PNG, JPG, GIF)
   - **Breaking News** - Check if it's breaking news
   - **Featured News** - Check to feature on homepage
3. Click "Add News"

### Editing Articles
1. Go to Admin Dashboard
2. Find the article in the "Recent News" table
3. Click "Edit"
4. Modify details and click "Update News"

### Deleting Articles
1. Go to Admin Dashboard
2. Find the article in the "Recent News" table
3. Click "Delete"

### Managing Categories
1. Go to Admin Panel → "Add Category"
2. Enter category name and click "Add Category"
3. To delete: Go to Dashboard and click "Delete" next to category
   - Note: Can only delete empty categories

## 🎨 Design & Color Scheme

The website uses a professional news portal color scheme:
- **Primary Color:** Red (#C40000) - For headlines, accents, and call-to-action
- **Secondary Color:** Blue (#003366) - For navigation and sections
- **Background:** White (#FFFFFF) - Clean, readable background
- **Text:** Black (#000000) - High contrast for readability

## 📱 Responsive Design

The website is fully responsive and includes breakpoints for:
- **Desktop:** 1200px+ (full layout)
- **Tablet:** 768px - 1199px (adjusted grid and spacing)
- **Mobile:** Below 768px (single column layout)
- **Small Mobile:** Below 480px (optimized for small screens)

## 🔐 Security Notes

- The admin panel is accessible directly without authentication
- For production deployment, implement authentication/authorization
- Validate and sanitize all user inputs
- Use HTTPS in production
- Store sensitive configuration in environment variables
- Implement rate limiting for file uploads

## 📦 Default Categories

The following categories are created automatically:
1. Breaking News
2. National News
3. International News
4. Politics
5. Crime
6. Business
7. Technology
8. Sports
9. Entertainment
10. Education
11. Health

## 🖼️ Supported Image Formats

- PNG
- JPG/JPEG
- GIF
- Maximum file size: 16MB

Images are stored with timestamps to prevent filename conflicts.

## 🔧 Customization

### Changing Colors
Edit the CSS variables in `static/css/style.css` and `static/css/admin.css`:
```css
:root {
    --primary-color: #C40000;      /* Change red */
    --secondary-color: #003366;    /* Change blue */
    --white: #FFFFFF;
    --black: #000000;
    --gray-light: #F5F5F5;
}
```

### Adding New Categories
Categories can be added through the admin panel or directly to the database.

### Modifying Navigation
Edit the navigation links in `templates/base.html` navbar section.

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change port number
```

### Database Issues
Delete `news.db` to reset the database:
```bash
rm news.db
python app.py
```

### Upload Directory Issues
Ensure the `static/uploads` directory has write permissions:
```bash
chmod 755 static/uploads
```

## 📄 License

This project is provided as-is for educational and demonstration purposes.

## 👨‍💼 Author

Created as a complete, production-ready news website template.

## 📞 Support

For issues or questions about setup and customization, refer to the code comments and documentation in each file.

---

**TAJA KHABAR NEWS 24** - Bringing you the truth, always! 🌐📰
