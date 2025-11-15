"""
Simple Flask server to serve frontend static files.
This can be deployed separately on Railway for the frontend.
"""
from flask import Flask, send_from_directory, send_file
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Health check endpoint
@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Frontend server is running'}, 200

# Serve index.html at root
@app.route('/')
def index():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(current_dir, 'index.html')
        app.logger.info(f"Serving index.html from: {index_path}")
        if os.path.exists(index_path):
            return send_file(index_path)
        else:
            app.logger.error(f"index.html not found at: {index_path}")
            return "index.html not found", 404
    except Exception as e:
        app.logger.error(f"Error serving index.html: {e}")
        return f"Error: {str(e)}", 500

# Serve other HTML files and static assets
@app.route('/<path:filename>')
def serve_file(filename):
    try:
        # Security: prevent directory traversal
        if '..' in filename or filename.startswith('/'):
            return "Forbidden", 403
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, filename)
        
        # Normalize path to prevent directory traversal
        file_path = os.path.normpath(file_path)
        if not file_path.startswith(current_dir):
            return "Forbidden", 403
        
        # Check if file exists
        if not os.path.exists(file_path):
            # Try with .html extension for HTML files
            if not filename.endswith('.html'):
                html_path = f"{file_path}.html"
                if os.path.exists(html_path):
                    file_path = html_path
                else:
                    app.logger.warning(f"File not found: {file_path}")
                    return "File not found", 404
            else:
                app.logger.warning(f"File not found: {file_path}")
                return "File not found", 404
        
        app.logger.info(f"Serving file: {file_path}")
        return send_file(file_path)
    except Exception as e:
        app.logger.error(f"Error serving {filename}: {e}")
        import traceback
        app.logger.error(traceback.format_exc())
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)
else:
    # For gunicorn
    pass

