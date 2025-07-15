from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

app = Flask(__name__)
CORS(app)  # Allow all origins (restrict in production!)

REPORT_FILE = "latest_report.csv"

# Reusable email sender with environment variable for password
def send_email(subject, body, to_email, attachment_path=None, attachment_name=None):
    sender = "mathuchinnamurugan@gmail.com"
    password = os.getenv("**** **** **** ****")  # Use env var for app password
    if not password:
        raise Exception("Email app password not set in environment variable EMAIL_APP_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    if attachment_path:
        with open(attachment_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=attachment_name)
        part['Content-Disposition'] = f'attachment; filename="{attachment_name}"'
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

@app.route("/report", methods=["GET"])
def get_report():
    if not os.path.exists(REPORT_FILE):
        return jsonify({"error": "Report not found"}), 404

    with open(REPORT_FILE, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
    return jsonify(data), 200

@app.route('/cleanup', methods=['POST'])
def cleanup():
    try:
        result = subprocess.run(['ansible-playbook', 'cleanup.yml'], capture_output=True, text=True)
        print("Ansible stdout:", result.stdout)
        print("Ansible stderr:", result.stderr)

        if result.returncode == 0:
            message_body = "✅ Cleanup Completed. No EC2 instances were stopped."
            if 'stopped' in result.stdout.lower():
                message_body = "✅ Cleanup Completed. Instances were stopped."

            send_email(
                subject="✅ Cloud Cleanup Completed",
                body=message_body,
                to_email="mathuchinnamurugan@gmail.com"
            )
            return jsonify({"status": message_body})
        else:
            return jsonify({"status": "❌ Cleanup failed", "error": result.stderr}), 500
    except Exception as e:
        return jsonify({"status": "❌ Exception occurred", "error": str(e)}), 500

@app.route("/status", methods=["GET"])
def get_status():
    # You can extend this to save real status after each cleanup
    return jsonify({"status": "Idle, last cleanup successful"}), 200

@app.route('/get-csv', methods=['GET'])
def get_csv():
    try:
        if not os.path.exists(REPORT_FILE):
            return jsonify({"status": "CSV file not found"}), 404

        send_email(
            subject="📄 Latest Cloud Cost Report",
            body="Please find the latest cost report attached.",
            to_email="mathuchinnamurugan@gmail.com",
            attachment_path=REPORT_FILE,
            attachment_name="cloud_cost_report.csv"
        )

        with open(REPORT_FILE, 'r') as f:
            lines = f.readlines()
        headers = lines[0].strip().split(',')
        data = [dict(zip(headers, row.strip().split(','))) for row in lines[1:]]
        return jsonify({"status": "CSV sent to email", "report": data})

    except Exception as e:
        return jsonify({"status": "Error sending CSV", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
