from flask import Flask, jsonify, request
from flask_cors import CORS  # Import CORS
import subprocess

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/report')
def get_report():
    with open('latest_report.csv', 'r') as f:
        lines = f.readlines()
    headers = lines[0].strip().split(',')
    data = []
    for line in lines[1:]:
        values = line.strip().split(',')
        data.append(dict(zip(headers, values)))
    return jsonify(data)

@app.route('/cleanup', methods=['POST'])
def cleanup():
    try:
        result = subprocess.run(['ansible-playbook', 'cleanup.yml'], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": "Cleanup triggered successfully"})
        else:
            print("Ansible error:", result.stderr)  # Print ansible error for debugging
            return jsonify({"message": "Cleanup failed", "error": result.stderr}), 500
    except Exception as e:
        print("Exception in cleanup:", str(e))  # Print exception for debugging
        return jsonify({"message": "Exception occurred", "error": str(e)}), 500


@app.route('/status')
def status():
    return jsonify({"message": "Last cleanup successful. No EC2 instances stopped."})

if __name__ == "__main__":
    app.run(debug=True)