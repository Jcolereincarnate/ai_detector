# AI Text Detector

## Description
AI Text Detector is a web-based application designed to analyze and detect the authenticity of text. It provides insights into the percentage of AI-generated and human-written content, along with AI confidence levels. This tool is ideal for ensuring content originality and maintaining transparency in text generation.

## Features
- Analyze text for AI-generated content.
- Display the percentage of AI-generated and human-written text.
- Show AI confidence levels for the analysis.
- User-friendly interface for text analysis.
- Additional features like readability adjustments and content authenticity checks.

## Tech Stack
- **Backend**: Django
- **Frontend**: HTML, CSS
- **Template Engine**: Django Template Language
- **Database**: Supabase Postgres via DATABASE_URL (SQLite remains as a local fallback)
- **Other**: Python

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Jcolereincarnate/ai_detector.git
   cd ai_detector
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy the sample environment file and update the values for your own environment:
   ```bash
   cp .env.example .env
   ```
5. Apply migrations:
   ```bash
   python manage.py migrate
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Environment Variables
Create a `.env` file in the project root and configure the following variables:

- `SECRET_KEY`: Django secret key.
- `DEBUG`: Set to `True` for development, `False` for production.
- `ALLOWED_HOSTS`: Comma-separated local and deployment hosts.
- `DATABASE_URL`: Supabase/Postgres connection string for Render and production.
- `RENDER_EXTERNAL_HOSTNAME`: Set automatically by Render; used for host and CSRF trust configuration.

Example:
```env
SECRET_KEY=replace-with-a-long-random-secret
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-app.onrender.com
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.xxxxxx.supabase.co:5432/postgres?sslmode=require
```

## Deploying to Render
1. Push this repository to GitHub.
2. In Render, create a new Web Service and connect the GitHub repo.
3. Set the build command to `pip install -r requirements.txt`.
4. Set the start command to `gunicorn plagiarism_checker.wsgi:application`.
5. Add the environment variables from your `.env` file in the Render dashboard.
6. Create a Supabase Postgres database if you have not already, then copy the connection string into `DATABASE_URL`.
7. Run `python manage.py migrate` on the deployed app or use Render's deploy command after setting the variable.
