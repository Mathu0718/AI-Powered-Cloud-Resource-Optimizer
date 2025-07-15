import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

SENDER = "mathuchinnamurugan@gmail.com"
PASSWORD = "kpsg olmj mtga bqmb"   # App Password (NOT normal Gmail password)
RECEIVER = "mathuchinnamurugan@gmail.com"

subject = "✅ Cloud Cleanup Completed"
body = "✅ Cleanup Completed. No EC2 instances were stopped.\n\nPlease find the report attached."

# Create email
msg = MIMEMultipart()
msg["Subject"] = subject
msg["From"] = SENDER
msg["To"] = RECEIVER
msg.attach(MIMEText(body))

# Attach the CSV file
filename = "latest_report.csv"
try:
    with open(filename, "rb") as file:
        part = MIMEApplication(file.read(), Name=filename)
        part['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(part)
except Exception as e:
    print("❌ Failed to attach file:", e)

# Send the email
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, PASSWORD)
        server.send_message(msg)
    print("✅ Email with attachment sent successfully.")
except Exception as e:
    print("❌ Failed to send email:", e)