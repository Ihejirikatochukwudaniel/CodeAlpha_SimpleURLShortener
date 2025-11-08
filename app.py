from flask import Flask, request, jsonify, redirect, render_template_string
import sqlite3
import string
import random
import os

app = Flask(__name__)

# Database file path
DB_PATH = 'urls.db'

def init_db():
    """Initialize the database and create tables"""
    try:
        # Delete old database if it exists and is corrupted
        if os.path.exists(DB_PATH):
            print(f"Found existing database at {DB_PATH}")
        
        conn = sqlite3.connect(DB_PATH)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                clicks INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        
        # Verify table was created
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='urls'")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            print("✓ Table 'urls' created/verified successfully")
            return True
        else:
            print("✗ Failed to create table 'urls'")
            return False
    except Exception as e:
        print(f"✗ Database initialization error: {e}")
        return False

# Initialize database immediately when module loads
print("\n" + "="*50)
print("🚀 URL Shortener - Initializing...")
print("="*50)
init_db()
print(f"📂 Database location: {os.path.abspath(DB_PATH)}")
print("="*50 + "\n")

def generate_short_code(length=6):
    """Generate a random short code"""
    characters = string.ascii_letters + string.digits
    for _ in range(10):  # Try 10 times max
        code = ''.join(random.choice(characters) for _ in range(length))
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM urls WHERE short_code = ?', (code,))
            exists = cursor.fetchone()
            conn.close()
            if not exists:
                return code
        except sqlite3.OperationalError as e:
            print(f"Database error: {e}")
            # Try to reinitialize database
            init_db()
            conn.close()
    return code  # Return anyway if all attempts fail

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
        }
        .input-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }
        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            display: none;
        }
        .result.show {
            display: block;
        }
        .short-url {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 10px;
        }
        .short-url input {
            flex: 1;
            padding: 12px;
            border: 2px solid #667eea;
            border-radius: 8px;
            font-size: 16px;
        }
        .copy-btn {
            padding: 12px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            width: auto;
        }
        .error {
            color: #e74c3c;
            margin-top: 10px;
            padding: 10px;
            background: #fdeaea;
            border-radius: 5px;
            display: none;
        }
        .error.show {
            display: block;
        }
        .stats {
            margin-top: 10px;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 URL Shortener</h1>
        <p class="subtitle">Transform long URLs into short, shareable links</p>
        
        <div class="input-group">
            <label for="longUrl">Enter your long URL:</label>
            <input type="text" id="longUrl" placeholder="https://example.com/very/long/url/here">
        </div>
        
        <button id="shortenBtn" onclick="shortenUrl()">Shorten URL</button>
        
        <div class="error" id="error"></div>
        
        <div class="result" id="result">
            <h3>Your shortened URL:</h3>
            <div class="short-url">
                <input type="text" id="shortUrl" readonly>
                <button class="copy-btn" onclick="copyToClipboard()">Copy</button>
            </div>
            <div class="stats" id="stats"></div>
        </div>
    </div>

    <script>
        async function shortenUrl() {
            const longUrl = document.getElementById('longUrl').value.trim();
            const errorDiv = document.getElementById('error');
            const resultDiv = document.getElementById('result');
            const btn = document.getElementById('shortenBtn');
            
            errorDiv.classList.remove('show');
            resultDiv.classList.remove('show');
            
            if (!longUrl) {
                errorDiv.textContent = 'Please enter a URL';
                errorDiv.classList.add('show');
                return;
            }
            
            try {
                new URL(longUrl);
            } catch (e) {
                errorDiv.textContent = 'Please enter a valid URL (include http:// or https://)';
                errorDiv.classList.add('show');
                return;
            }
            
            btn.disabled = true;
            btn.textContent = 'Shortening...';
            
            try {
                const response = await fetch('/api/shorten', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ url: longUrl })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    const shortUrl = window.location.origin + '/' + data.short_code;
                    document.getElementById('shortUrl').value = shortUrl;
                    document.getElementById('stats').textContent = 'Created: ' + new Date(data.created_at).toLocaleString();
                    resultDiv.classList.add('show');
                } else {
                    errorDiv.textContent = data.error || 'An error occurred';
                    errorDiv.classList.add('show');
                }
            } catch (error) {
                errorDiv.textContent = 'Failed to connect: ' + error.message;
                errorDiv.classList.add('show');
            } finally {
                btn.disabled = false;
                btn.textContent = 'Shorten URL';
            }
        }
        
        function copyToClipboard() {
            const input = document.getElementById('shortUrl');
            input.select();
            document.execCommand('copy');
            event.target.textContent = 'Copied!';
            setTimeout(() => event.target.textContent = 'Copy', 2000);
        }
        
        document.getElementById('longUrl').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') shortenUrl();
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        original_url = data['url']
        
        if not original_url.startswith(('http://', 'https://')):
            return jsonify({'error': 'URL must start with http:// or https://'}), 400
        
        short_code = generate_short_code()
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Try to insert
        try:
            cursor.execute(
                'INSERT INTO urls (short_code, original_url) VALUES (?, ?)',
                (short_code, original_url)
            )
            conn.commit()
        except sqlite3.OperationalError as e:
            # If table doesn't exist, create it and try again
            print(f"Table error, reinitializing: {e}")
            conn.close()
            init_db()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO urls (short_code, original_url) VALUES (?, ?)',
                (short_code, original_url)
            )
            conn.commit()
        
        cursor.execute('SELECT created_at FROM urls WHERE short_code = ?', (short_code,))
        created_at = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            'short_code': short_code,
            'original_url': original_url,
            'created_at': created_at
        }), 201
        
    except Exception as e:
        app.logger.error(f'Error in shorten_url: {e}')
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/<short_code>')
def redirect_to_url(short_code):
    if short_code == 'favicon.ico':
        return '', 404
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
        result = cursor.fetchone()
        
        if result:
            original_url = result[0]
            cursor.execute('UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?', (short_code,))
            conn.commit()
            conn.close()
            return redirect(original_url)
        else:
            conn.close()
            return 'Short URL not found', 404
            
    except Exception as e:
        app.logger.error(f'Error in redirect: {e}')
        return 'Server error', 500

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM urls WHERE short_code = ?', (short_code,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return jsonify({
                'short_code': row[1],
                'original_url': row[2],
                'created_at': row[3],
                'clicks': row[4]
            })
        else:
            return jsonify({'error': 'Not found'}), 404
            
    except Exception as e:
        app.logger.error(f'Error in get_stats: {e}')
        return jsonify({'error': 'Server error'}), 500

@app.route('/health')
def health():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM urls')
        count = cursor.fetchone()[0]
        conn.close()
        return jsonify({'status': 'ok', 'total_urls': count})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print('Starting Flask server...')
    print('Visit: http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)