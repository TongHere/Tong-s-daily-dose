from flask import Flask, render_template, send_from_directory, abort
import markdown
import os
import logging
import re
from google.cloud import monitoring_v3
from google.cloud import logging as cloud_logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Cloud Logging
cloud_logging_client = cloud_logging.Client()
cloud_logging_client.setup_logging()

# Initialize Cloud Monitoring
monitoring_client = monitoring_v3.MetricServiceClient()
project_name = f"projects/tongsdailydose-462517"

app = Flask(__name__)

# Version information
VERSION = "1.0.3"
BUILD_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def fix_image_paths(content):
    """Fix image paths in markdown content to work with Flask's static files."""
    # Replace relative image paths with Flask's url_for
    def replace_img_path(match):
        img_path = match.group(1)
        if not img_path.startswith(('http://', 'https://')):
            # Convert relative path to Flask static URL
            return f'<img src="{url_for("static", filename=img_path)}"'
        return match.group(0)

    # Find all img tags and fix their src attributes
    content = re.sub(r'<img src="([^"]+)"', replace_img_path, content)
    return content

def load_markdown(filename):
    """Load and convert markdown file to HTML."""
    try:
        file_path = os.path.join('static/content', filename)
        logger.info(f"Loading markdown file: {file_path}")
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return f"Error: File {filename} not found"
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
            logger.info(f"Successfully loaded {filename}")
            # Convert markdown to HTML
            html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
            # Fix image paths
            html_content = fix_image_paths(html_content)
            return html_content
    except Exception as e:
        logger.error(f"Error loading {filename}: {str(e)}")
        return f"Error loading content: {str(e)}"

@app.route('/')
def home():
    logger.info(f"Accessing home page with version: {VERSION}")
    content = load_markdown('static/content/deepseek.md')
    logger.info(f"Content loaded, rendering template with version: {VERSION}")
    return render_template('index.html', content=content, version=VERSION, build_time=BUILD_TIME)

@app.route('/daily')
def daily():
    logger.info("Accessing daily content")
    return render_template('index.html', content=load_markdown('deepseek.md'), version=VERSION, build_time=BUILD_TIME)

@app.route('/weekly')
def weekly():
    logger.info("Accessing weekly content")
    return render_template('index.html', content=load_markdown('deepseek.md'), version=VERSION, build_time=BUILD_TIME)

@app.errorhandler(404)
def page_not_found(e):
    logger.error(f"Page not found: {request.path}")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"Internal server error: {str(e)}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Use environment variable for port, default to 8000
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 