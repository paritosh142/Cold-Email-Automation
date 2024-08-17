import re
import google.generativeai as genai
from resume import resume_content
from template import template_content
from opening_line import open
from closing_line import close
import os

# Load the Gemini API key from environment variables
gemini_api_key_private = os.getenv('gemini_api_key_private')

# Configure the Gemini API key
genai.configure(api_key=gemini_api_key_private)

def generate_email(job_description, recruiter_name, company_name, location, job_title):
    # Resume and Template Content
    resume = resume_content
    template = template_content

    # Lines
    opening_lines = open
    closing_lines = close

    # Build the prompt dynamically
    prompt = f"""
    Craft a complete and personalized cold email for a job application based on the provided details. The email should follow the given template and be infused with a slightly unconventional yet professional tone.

    From the Resume:
    {resume}

    Email Template:
    {template}

    Additional Information:
    - Recruiter Name: {recruiter_name}
    - Company Name: {company_name}
    - Location: {location}
    - Job Title: {job_title}
    - Job Description: {job_description}

    Use the details to fill in the corresponding sections of the email template.

    Opening Line Options:
    Choose one of the following engaging openings or craft a similar unique introduction that fits the tone:
    {opening_lines}

    Closing Line Options:
    Choose one of the following distinctive closings or create a similar memorable ending:
    {closing_lines}

    Ensure the email:
    - Has a professional yet slightly unconventional tone.
    - Is concise and highlights the applicant's unique value proposition.
    - Includes a captivating subject line.
    - Presents a well-structured body with all placeholders replaced with extracted information.
    - Excludes markdown-like syntax such as `**`.

    Alert the user if any crucial information is missing from the resume and insert placeholders where manual input is needed.
    """

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)

    return response.text