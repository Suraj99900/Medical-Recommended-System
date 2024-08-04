from flask import Flask, jsonify
from flask_cors import CORS
from route.user import user_bp  # Import the user blueprint

app = Flask(__name__)
CORS(app)
# Register the user blueprint with the app
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)