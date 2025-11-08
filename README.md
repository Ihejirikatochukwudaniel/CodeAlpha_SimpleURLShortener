# 🔗 URL Shortener

A lightweight and elegant URL shortener application built with Flask and SQLite. Transform long URLs into short, shareable links with built-in click tracking.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🚀 **Simple & Fast** - Shorten URLs in seconds
- 🎨 **Beautiful UI** - Modern, gradient-based design
- 📊 **Click Tracking** - Monitor how many times your links are visited
- 💾 **SQLite Database** - Persistent storage without external dependencies
- 📋 **Copy to Clipboard** - One-click copy functionality
- 🔍 **URL Validation** - Ensures only valid URLs are shortened
- 📱 **Responsive Design** - Works on desktop and mobile devices

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with gradient backgrounds

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
```bash
   git clone https://github.com/yourusername/url-shortener.git
   cd url-shortener
```

2. **Create a virtual environment**
```bash
   python -m venv venv
```

3. **Activate the virtual environment**
   - Windows:
```bash
     venv\Scripts\activate
```
   - Mac/Linux:
```bash
     source venv/bin/activate
```

4. **Install dependencies**
```bash
   pip install -r requirements.txt
```

5. **Run the application**
```bash
   python app.py
```

6. **Access the app**
   Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure
```
url-shortener/
│
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── urls.db            # SQLite database (auto-generated)
├── .gitignore         # Git ignore file
└── README.md          # Project documentation
```

## 🚀 Usage

### Shorten a URL
1. Enter a long URL in the input field (must include `http://` or `https://`)
2. Click "Shorten URL"
3. Copy your shortened URL and share it!

### API Endpoints

#### Shorten URL
```http
POST /api/shorten
Content-Type: application/json

{
  "url": "https://example.com/very/long/url"
}

Response:
{
  "short_code": "aBc123",
  "original_url": "https://example.com/very/long/url",
  "created_at": "2025-11-08 23:00:00"
}
```

#### Redirect to Original URL
```http
GET /{short_code}
```

#### Get URL Statistics
```http
GET /api/stats/{short_code}

Response:
{
  "short_code": "aBc123",
  "original_url": "https://example.com/very/long/url",
  "created_at": "2025-11-08 23:00:00",
  "clicks": 42
}
```

#### Health Check
```http
GET /health

Response:
{
  "status": "ok",
  "total_urls": 10
}
```

## 🎯 Features in Detail

### Short Code Generation
- 6-character alphanumeric codes
- Case-sensitive (52 letters + 10 digits = 62 possibilities per character)
- ~56 billion possible combinations

### Database Schema
```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    clicks INTEGER DEFAULT 0
);
```

## 🔧 Configuration

You can modify these settings in `app.py`:

- `DB_PATH`: Database file location (default: `urls.db`)
- `short_code length`: Length of generated codes (default: 6)
- `host`: Server host (default: `0.0.0.0`)
- `port`: Server port (default: `5000`)

## 🐛 Troubleshooting

### Database Issues
If you encounter database errors:
```bash
# Delete the database and restart
del urls.db  # Windows
rm urls.db   # Mac/Linux

python app.py
```

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Change 5000 to 8000
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👤 Author

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/url-shortener](https://github.com/yourusername/url-shortener)

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Icons from emoji
- Gradient inspiration from [UI Gradients](https://uigradients.com/)

---

Made with ❤️ and Python
```

## Additional Files to Create:

### .gitignore
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/

# Database
*.db
*.sqlite
*.sqlite3

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env

# OS
.DS_Store
Thumbs.db
```

### LICENSE (MIT)
```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
