from flask import Flask, jsonify
from route.user import user_bp  # Import the user blueprint
from route.buzzer import user_bp

app = Flask(__name__)

# Register the user blueprint with the app
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)