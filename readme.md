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
- **Database**: SQLite (default for Django, can be replaced with PostgreSQL or MySQL)
- **Other**: Python

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Jcolereincarnate/ai_detector.git
   cd plagiarism_checker

2. Create and activate a virtual environment:
    python3 -m venv venv
    source venv/bin/activate
3. Install dependencies:
    pip install -r requirements.txt
4. Apply migrations:
    python manage.py migrate
5. Run the development server:
    python manage.py runserver

Environment Variables
Create a .env file in the root directory and configure the following variables:

SECRET_KEY: Django secret key.
DEBUG: Set to True for development, False for production.
DATABASE_URL: Database connection string (optional for SQLite).