# Tong's Daily Dose

A personal blog and learning journal built with Flask, featuring Markdown content, a modern UI, and an integrated OpenAI-powered chat assistant.

## Features
- 📚 Blog content in Markdown (daily, weekly, and resource sections)
- 🖼️ Clean, responsive design with custom CSS
- 💬 AI chat assistant using OpenAI GPT (on the home page)
- 🐳 Dockerized for easy deployment
- ☁️ Cloud Run ready (Google Cloud Platform)

## Project Structure
```
Tong-s-daily-dose/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker build file
├── docker-compose.yml    # Local development with Docker
├── cloudbuild.yaml       # Cloud Build config for GCP
├── static/               # Static files (content, images, CSS)
├── templates/            # Jinja2 HTML templates
└── ...
```

## Local Development
1. **Clone the repo:**
   ```bash
   git clone https://github.com/TongHere/Tong-s-daily-dose.git
   cd Tong-s-daily-dose
   ```
2. **Get an OpenAI API key:**
   - Sign up at https://platform.openai.com/api-keys
   - Copy your API key (starts with `sk-...`)
3. **Run with Docker Compose:**
   ```bash
   export OPENAI_API_KEY=sk-...   # <-- your key here
   docker-compose up --build
   ```
   The app will be available at http://localhost:8000

## Production Deployment (Cloud Run)
1. **Set up Google Cloud SDK and project**
2. **Build and deploy:**
   ```bash
   gcloud builds submit --config cloudbuild.yaml .
   ```
3. **Set the OpenAI API key in Cloud Run:**
   ```bash
   gcloud run services update tong-daily-dose \
     --region us-central1 \
     --update-env-vars OPENAI_API_KEY=sk-...   # <-- your key here
   ```
4. **Visit your app:**
   - The deployed URL will be shown in the output (e.g., https://tong-daily-dose-xxxx.a.run.app)

## Customization
- **Content:** Add or edit Markdown files in `static/content/`
- **Images:** Place images in `static/img/`
- **Styling:** Edit `static/styles.css` or inline styles in `templates/index.html`
- **Chat prompt:** Adjust the system prompt in `app.py` for the OpenAI assistant

## Security Notes
- **Never commit your OpenAI API key to GitHub!**
- Use environment variables for all secrets
- Monitor your OpenAI usage to avoid unexpected charges

## License
MIT 