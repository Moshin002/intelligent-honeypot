import logging
import os
from flask import Flask, request, jsonify

app = Flask(__name__)


def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.getenv('LOG_FILE', 'threats.log')),
            logging.StreamHandler()
        ]
    )


@app.route('/wp-admin')
def fake_admin():
    logging.warning(f"ADMIN SCAN ATTEMPTED by {request.remote_addr}")
    return "Fake admin page", 200


@app.route('/')
def health_check():
    return jsonify({
        "status": "running", "message": "Simplified server works!"})


if __name__ == '__main__':
    configure_logging()
    logging.info("✅ Server starting on 0.0.0.0:5000 (IPv4 only)")
    app.run(host='0.0.0.0', port=5000)
