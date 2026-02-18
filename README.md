# Resume Chatbot - Portfolio Project

This project is a Flask-based portfolio website featuring an AI-powered chatbot that answers questions based on Debasriya Panigrahy's resume.

## Features
- **Portfolio Website**: Displays About, Education, Projects, Skills, and Contact info.
- **AI Chatbot**: powered by Groq (Llama 3.3 70B), answers questions using the resume as context.
- **Minimizable UI**: A sleek, modern chat widget.

## Prerequisites
- Python 3.8+
- A Groq API Key

## Local Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd portfolio
    ```

2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**:
    Create a `.env` file in the root directory and add your Groq API key:
    ```
    GROQ_API_KEY=your_groq_api_key_here
    ```

5.  **Run the application**:
    ```bash
    python app.py
    ```
    The app will run at `http://127.0.0.1:5000`.

## Deployment on Render

1.  **Create a new Web Service** on [Render](https://render.com/).
2.  **Connect your GitHub repository**.
3.  **Settings**:
    - **Runtime**: Python 3
    - **Build Command**: `pip install -r requirements.txt`
    - **Start Command**: `gunicorn app:app`
4.  **Environment Variables**:
    - Add `GROQ_API_KEY` with your actual API key value.
    - Add `PYTHON_VERSION` (e.g., `3.10.0`) if needed.

## Project Structure
- `app.py`: Main Flask application.
- `cleaned_resume.txt`: The text source for the chatbot.
- `templates/`: HTML templates.
- `static/`: CSS and other static assets.
