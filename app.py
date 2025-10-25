from flask import Flask, render_template
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_here')

@app.route('/')
def index():
    return render_template('index.html')

# Email functionality moved to API route for better Vercel compatibility

if __name__ == '__main__':
    app.run(debug=True)
