from flask import Flask, render_template, send_from_directory, abort, request, url_for, jsonify
import markdown
import os
import logging
import re
from google.cloud import monitoring_v3
from google.cloud import logging as cloud_logging
from datetime import datetime
import openai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Cloud Logging
cloud_logging_client = cloud_logging.Client()
cloud_logging_client.setup_logging()

# Initialize Cloud Monitoring
monitoring_client = monitoring_v3.MetricServiceClient()
project_name = f"projects/tongsdailydose-462517"

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    logger.warning("OPENAI_API_KEY environment variable not set")

app = Flask(__name__)

# Version information
VERSION = "1.0.6"
BUILD_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
TEST_MESSAGE = "Added chat functionality"

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
    content = load_markdown('deepseek.md')
    logger.info(f"Content loaded, rendering template with version: {VERSION}")
    return render_template('index.html', 
                         section='home',
                         content=content, 
                         version=VERSION, 
                         build_time=BUILD_TIME, 
                         test_message=TEST_MESSAGE)

@app.route('/daily/<content>')
def daily(content):
    logger.info(f"Accessing daily content: {content}")
    content_html = load_markdown(f'{content}.md')
    return render_template('index.html', 
                         section='daily',
                         subpage=content,
                         content=content_html, 
                         version=VERSION, 
                         build_time=BUILD_TIME, 
                         test_message=TEST_MESSAGE)

@app.route('/weekly/<content>')
def weekly(content):
    logger.info(f"Accessing weekly content: {content}")
    content_html = load_markdown(f'{content}.md')
    return render_template('index.html', 
                         section='weekly',
                         subpage=content,
                         content=content_html, 
                         version=VERSION, 
                         build_time=BUILD_TIME, 
                         test_message=TEST_MESSAGE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        logger.info(f"Received chat POST: {data}")
        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No data provided'}), 400
        user_message = data.get('message', '')
        conversation = data.get('conversation', [])
        if not user_message:
            logger.error("Empty message received")
            return jsonify({'error': 'No message provided'}), 400
        if not openai.api_key:
            logger.error("OpenAI API key not configured")
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        logger.info(f"Processing chat message: {user_message[:50]}...")
        # Build messages for OpenAI
        messages = [{"role": m["role"], "content": m["content"]} for m in conversation]
        messages.append({"role": "user", "content": user_message})
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for Tong's Daily Dose blog. Keep responses concise and friendly."},
                    *messages
                ],
                max_tokens=150,
                temperature=0.7,
                timeout=10
            )
            assistant_message = response.choices[0].message.content if response.choices else None
            logger.info(f"OpenAI response: {assistant_message}")
            if assistant_message:
                return jsonify({'response': assistant_message})
            else:
                logger.error("No response from OpenAI API")
                return jsonify({'error': 'No response from OpenAI API'}), 502
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return jsonify({'error': f'OpenAI API error: {str(e)}'}), 502
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

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