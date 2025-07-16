from flask import Flask, render_template, send_from_directory, abort, request, url_for, jsonify
import markdown
import os
import logging
import re
from google.cloud import monitoring_v3
from google.cloud import logging as cloud_logging
from datetime import datetime
import requests
from dotenv import load_dotenv
from tong_chatbot import get_chat_response, is_chatbot_configured

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Cloud Logging
try:
    cloud_logging_client = cloud_logging.Client()
    cloud_logging_client.setup_logging()
    logger.info("Google Cloud Logging initialized successfully")
except Exception as e:
    logger.warning(f"Google Cloud Logging not available (likely running locally): {e}")
    cloud_logging_client = None

# Initialize Cloud Monitoring
try:
    monitoring_client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/tongsdailydose-462517"
    logger.info("Google Cloud Monitoring initialized successfully")
except Exception as e:
    logger.warning(f"Google Cloud Monitoring not available (likely running locally): {e}")
    monitoring_client = None
    project_name = None

# Check OpenAI configuration
if not is_chatbot_configured():
    logger.warning("OPENAI_API_KEY environment variable not set")

app = Flask(__name__)

# Version information
VERSION = "1.0.6"
BUILD_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
TEST_MESSAGE = "Added chat functionality"

def fetch_news_data():
    """Fetch news data from NewsAPI and return categorized articles."""
    try:
        NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
        if not NEWSAPI_KEY:
            logger.error("NEWSAPI_KEY environment variable not set")
            return {"error": "NewsAPI key not configured"}

        # Domain categories
        tech_domains = {
            "theverge.com", "technologyreview.com", "wired.com", "techcrunch.com",
            "techradar.com", "thenextweb.com",
        }
        business_domains = {
            "wsj.com", "businessinsider.com", "ft.com", "cnbc.com",
            "bloomberg.com", "time.com",
        }
        general_domains = {
            "reuters.com", "theguardian.com", "nytimes.com", "bbc.com",
            "cnn.com", "nbcnews.com", "washingtonpost.com",
        }

        # Explicit mapping from NewsAPI source names → domains
        name_to_domain = {
            "The Verge": "theverge.com", "Wired": "wired.com",
            "MIT Technology Review": "technologyreview.com", "TechCrunch": "techcrunch.com",
            "TechRadar": "techradar.com", "The Next Web": "thenextweb.com",
            "The Wall Street Journal": "wsj.com", "Business Insider": "businessinsider.com",
            "Financial Times": "ft.com", "CNBC": "cnbc.com", "Bloomberg": "bloomberg.com",
            "TIME": "time.com", "Reuters": "reuters.com", "The Guardian": "theguardian.com",
            "The New York Times": "nytimes.com", "BBC News": "bbc.com", "CNN": "cnn.com",
            "NBC News": "nbcnews.com", "The Washington Post": "washingtonpost.com",
        }

        # Combined domain list for the NewsAPI request
        ai_domains = list(tech_domains | business_domains | general_domains)
        domain_str = ",".join(ai_domains)

        # Build and send the NewsAPI request
        url = (
            "https://newsapi.org/v2/everything?"
            "q=artificial+intelligence+OR+AI&"
            "from=2025-07-12&"
            "to=2025-07-14&"
            "sortBy=popularity&"
            f"domains={domain_str}&"
            f"apiKey={NEWSAPI_KEY}"
        )

        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            logger.error(f"NewsAPI error: {data}")
            return {"error": f"NewsAPI error: {data.get('message', 'Unknown error')}"}

        # Categorize the articles
        business_articles, tech_articles, general_articles = [], [], []

        for art in data.get("articles", []):
            source_name = art["source"]["name"]
            domain = name_to_domain.get(source_name, "").lower()

            article = {
                "source": source_name,
                "title": art["title"],
                "description": art.get("description", "No description available."),
                "url": art["url"],
                "published_at": art["publishedAt"][:10],  # YYYY-MM-DD
            }

            if domain in tech_domains:
                tech_articles.append(article)
            elif domain in business_domains:
                business_articles.append(article)
            elif domain in general_domains:
                general_articles.append(article)

        return {
            "business": business_articles,
            "tech": tech_articles,
            "general": general_articles,
            "total": len(business_articles) + len(tech_articles) + len(general_articles)
        }

    except Exception as e:
        logger.error(f"Error fetching news: {str(e)}")
        return {"error": f"Error fetching news: {str(e)}"}

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
    logger.info(f"Accessing reading content: {content}")
    content_html = load_markdown(f'{content}.md')
    return render_template('index.html', 
                         section='daily',
                         subpage=content,
                         content=content_html, 
                         version=VERSION, 
                         build_time=BUILD_TIME, 
                         test_message=TEST_MESSAGE)

@app.route('/news')
def news():
    """News aggregator page."""
    logger.info("Accessing news aggregator page")
    news_data = fetch_news_data()
    return jsonify(news_data)

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint that uses the chatbot library."""
    try:
        data = request.get_json()
        logger.info(f"Received chat POST: {data}")
        
        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No data provided'}), 400
            
        user_message = data.get('message', '')
        conversation = data.get('conversation', [])
        
        # Get response from chatbot library
        assistant_message, error = get_chat_response(user_message, conversation)
        
        if error:
            logger.error(f"Chatbot error: {error}")
            return jsonify({'error': error}), 502
            
        return jsonify({'response': assistant_message})
        
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