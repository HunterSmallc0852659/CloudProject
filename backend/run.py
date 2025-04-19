from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Serve index.html when visiting the root path
@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

# Your existing upload route here
@app.route('/upload', methods=['POST'])
def upload_file():
    # Handle file upload logic
    pass

if __name__ == "__main__":
    app.run(debug=True)