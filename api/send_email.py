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
        
        # Email configuration
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        email_user = os.getenv('EMAIL_USER')
        email_password = os.getenv('EMAIL_PASSWORD')
        
        if not email_user or not email_password:
            return jsonify({'success': False, 'message': 'Email configuration not found'}), 500
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_user
        msg['Subject'] = f"New Message from {name}"
        
        body = f"""
You have received a new message from your portfolio contact form:

Name: {name}
Email: {sender_email}

Message:
{message_content}
"""
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_password)
        text = msg.as_string()
        server.sendmail(email_user, email_user, text)
        server.quit()
        
        response = jsonify({'success': True, 'message': 'Message sent successfully!'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        print(f"Error: {e}")
        response = jsonify({'success': False, 'message': 'Error sending message. Please try again later.'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

if __name__ == '__main__':
    app.run(debug=True)
