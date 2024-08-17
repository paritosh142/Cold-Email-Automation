# app.py
from flask import Flask, render_template, request
from gemini import generate_email
import webbrowser
import urllib.parse
from dotenv import load_dotenv
import os
from flask_cors import CORS


# Load environment variables from .env file
load_dotenv()


app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-email', methods=['POST'])
def generate_email_route():
    # Get the form data
    email = request.form['email']
    job_description = request.form['job_description']
    recruiter_name = request.form['recruiter_name']
    company_name = request.form['company_name']
    location = request.form['location']
    job_title = request.form['job_title']

    # Generate the email using the Gemini API
    generated_email = generate_email(job_description, recruiter_name, company_name, location, job_title)

    # Print the raw output to inspect its structure
    print(f"Generated Email:\n{generated_email}")

    try:
        # Split the generated email based on the first occurrence of 'Subject:'
        subject_body_parts = generated_email.split('Subject:', 1)
        
        # If 'Subject:' exists, proceed with extracting the subject and body
        if len(subject_body_parts) > 1:
            subject_body_split = subject_body_parts[1].split('\n', 1)
            subject = subject_body_split[0].strip()  # Get the subject line
            body = subject_body_split[1].strip() if len(subject_body_split) > 1 else ""
        else:
            raise ValueError("Subject line not found in the generated email.")

    except Exception as e:
        return f"Error: Could not parse the generated email. Ensure the email is formatted correctly. Details: {str(e)}"

    # URL encode the subject and body
    encoded_subject = urllib.parse.quote(subject)
    encoded_body = urllib.parse.quote(body)

    # Redirect to Gmail with the generated email
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={email}&su={encoded_subject}&body={encoded_body}"
    webbrowser.open(gmail_url)

    return f"Subject: {subject}\nBody: {body}"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT environment variable if provided, otherwise default to 5000
    app.run(host="0.0.0.0", port=port)
