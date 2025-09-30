from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for form data
class ContactForm(BaseModel):
    name: str
    email: str
    number: str
    message: str

# Email sending function (FIXED)
def send_email_notification(contact_data):
    try:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "partheepan1505@gmail.com"
        
        # Use environment variable for password (SECURITY)
        password = os.getenv("EMAIL_PASSWORD", "dznu zivh zhix keiy")  # Fallback for testing
        
        # You should receive notifications at your own email
        receiver_email = "partheepan1505@gmail.com"  # Change this if you want notifications elsewhere

        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"New Contact from {contact_data['name']}"

        body = f"""
        New Contact Form Submission:
        
        Name: {contact_data['name']}
        Email: {contact_data['email']}
        Phone: {contact_data['number']}
        Message: {contact_data['message']}
        
        This person wants to contact you from your portfolio website.
        
        Best regards,  
        Your Portfolio System
        """

        # Attach body
        message.attach(MIMEText(body, "plain"))

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)

        print(f"✅ Email sent successfully to {receiver_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

# GET endpoint
@app.get("/contact")
async def get_contact():
    return {
        "email": "partheepan1505@gmail.com", 
        "phone": "+91 YOUR_PHONE",  # Add your actual phone number
        "message": "Feel free to contact me"
    }

# POST endpoint (INTEGRATED with email)
@app.post("/contact")
async def submit_contact(contact: ContactForm):
    try:
        # Print received data for debugging
        print(f"📨 Received contact form: {contact.dict()}")
        
        # Send email notification
        email_sent = send_email_notification(contact.dict())
        
        # Here you can add code to save to database, etc.
        
        return {
            "status": "success", 
            "message": "Form submitted successfully" + (" and email sent!" if email_sent else " but email failed."),
            "email_sent": email_sent,
            "data": contact.dict()
        }
        
    except Exception as e:
        print(f"❌ Error in submit_contact: {e}")
        return {"status": "error", "message": str(e)}

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Contact API is running", "status": "success"}

# Test endpoint to check email functionality
@app.get("/test-email")
async def test_email():
    try:
        test_data = {
            "name": "Test User",
            "email": "test@example.com", 
            "number": "+1234567890",
            "message": "This is a test message from the API"
        }
        
        email_sent = send_email_notification(test_data)
        return {
            "status": "success" if email_sent else "error",
            "message": "Test email sent successfully" if email_sent else "Failed to send test email"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}