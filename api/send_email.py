from flask import Flask, request, jsonify
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/api/send_email', methods=['POST', 'OPTIONS'])
def send_email():
    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        # Get form data
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
            
        name = data.get('name')
        sender_email = data.get('email')
        message_content = data.get('message')
        
        # Validate required fields
        if not all([name, sender_email, message_content]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
        # Email configuration - using hardcoded values for testing
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        email_user = 'oniyonkuru233@gmail.com'  # Hardcoded for now
        email_password = 'dqbw wyni rgts pzsg'  # Hardcoded for now
        
        # Try to get from environment variables first
        env_email = os.getenv('EMAIL_USER')
        env_password = os.getenv('EMAIL_PASSWORD')
        
        if env_email and env_password:
            email_user = env_email
            email_password = env_password
        
        print(f"Using email: {email_user}")  # Debug log
        
        # Create SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_password)
        
        # Send notification email to portfolio owner (you)
        owner_msg = MIMEMultipart()
        owner_msg['From'] = email_user
        owner_msg['To'] = email_user
        owner_msg['Subject'] = f"New Message from {name} - Portfolio Contact Form"
        
        owner_body = f"""You have received a new message from your portfolio contact form:

Name: {name}
Email: {sender_email}

Message:
{message_content}

---
This message was sent from your portfolio contact form.
Reply directly to this email to respond to {name}."""
        
        owner_msg.attach(MIMEText(owner_body, 'plain'))
        server.sendmail(email_user, email_user, owner_msg.as_string())
        print("Owner email sent successfully")  # Debug log
        
        # Send auto-reply confirmation email to the user
        user_msg = MIMEMultipart()
        user_msg['From'] = email_user
        user_msg['To'] = sender_email
        user_msg['Subject'] = "Thank you for contacting Olivier Niyonkuru"
        
        user_body = f"""Dear {name},

Thank you for reaching out to me through my portfolio contact form!

I have received your message and will get back to you as soon as possible. I appreciate you taking the time to contact me.

Your message:
"{message_content}"

Best regards,
Olivier Niyonkuru
ProfessionalSoftware Engineer


---
This is an automated confirmation email. Please do not reply to this message.
If you need to send additional information, please use the contact form on my portfolio."""
        
        user_msg.attach(MIMEText(user_body, 'plain'))
        server.sendmail(email_user, sender_email, user_msg.as_string())
        print("User email sent successfully")  # Debug log
        
        server.quit()
        
        response = jsonify({'success': True, 'message': 'Message sent successfully! You will receive a confirmation email shortly.'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        print(f"Error: {e}")  # Debug log
        response = jsonify({'success': False, 'message': f'Error sending message: {str(e)}'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/api/test_email', methods=['GET'])
def test_email():
    """Simple test endpoint to check if email configuration works"""
    try:
        email_user = os.getenv('EMAIL_USER', 'oniyonkuru233@gmail.com')
        email_password = os.getenv('EMAIL_PASSWORD', 'dqbw wyni rgts pzsg')
        
        return jsonify({
            'success': True, 
            'message': 'Email configuration loaded',
            'email_user': email_user,
            'has_password': bool(email_password)
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
