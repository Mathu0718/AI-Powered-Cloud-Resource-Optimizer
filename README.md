Cloud Cleaner Dashboard
________________________________________________________________________________________________________
A full-stack automated Cloud Cost Optimizer tool built using React, Flask, Ansible, and AWS Services.

This dashboard allows users to:
________________________________________________________________________________________________________
Trigger EC2 cleanup of idle instances via Ansible
Generate and send AWS cost reports as CSV files
Receive email notifications about cleanup actions
View the report and status in a React frontend

Video Demo
________________________________________________________________________________________________________
Watch the full walkthrough on Loom
Click to watch the video demo
(Replace with your actual Loom video link after recording)

Tech Stack
________________________________________________________________________________________________________
Layer	Technologies Used
Frontend	React, Tailwind CSS
Backend	Flask (Python)
Automation	Ansible
Cloud	AWS EC2, S3, SNS, IAM, Cost Explorer API
Email	Gmail SMTP with App Password
Tools	Postman, VS Code, GitHub

Project Flow
________________________________________________________________________________________________________
React Dashboard
View cloud cost report
Trigger cleanup action
Request report via email
Flask Backend API
________________________________________________________________________________________________________
/cleanup: Runs Ansible playbook
/get-csv: Sends report as email and returns JSON
/report: Returns report as JSON
/status: Returns current cleanup status

Ansible Automation
________________________________________________________________________________________________________
Scans EC2 instances for idle time
Stops unused EC2 instances
Generates latest_report.csv
Email Notifications
Sent after cleanup or CSV request
Uses Gmail SMTP and environment variables

AWS Services Used
________________________________________________________________________________________________________
EC2: Instances to be cleaned
IAM: For secure access
Cost Explorer: For cost reporting
S3 (Optional): Store reports
SNS (Optional): Future alert system

File Structure
________________________________________________________________________________________________________
cloud-cleaner-ansible/
├── app.py                      # Flask backend API
├── cleanup.yml                 # Ansible playbook
├── latest_report.csv           # AWS cost report output
├── fetch_cost_report.py        # Billing data script
├── notify_user.py              # Email utility
├── ec2_cleanup/                # Ansible tasks
├── aws/                        # AWS CLI setup files
├── roles/                      # Ansible roles (optional)
├── venv/                       # Python virtual environment
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── Dashboard.jsx
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   └── public/

Running Locally
________________________________________________________________________________________________________
1. Backend (Flask)
bash
Copy
Edit
cd cloud-cleaner-ansible
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
export EMAIL_APP_PASSWORD=your-gmail-app-password
python app.py

2. Frontend (React)
bash
Copy
Edit
cd frontend
npm install
npm run dev

Setup Checklist
________________________________________________________________________________________________________
AWS CLI is installed and configured
IAM user or role has EC2 and billing permissions
AWS Cost Explorer is enabled
Ansible is installed (ansible-playbook --version)
Gmail app password is stored in the environment variable

Features
________________________________________________________________________________________________________
Full-stack integration with AWS automation
Email notifications with dynamic CSV reports
Clean and simple React UI
Secure email sending using environment variables
Easily extendable project structure
Future Improvements
Store reports in AWS S3
Add notification support via AWS SNS
Add user authentication (login system)
PDF report export
Docker support for deployment

Author
Built by Mathu C
Email: mathuchinnamurugan@gmail.com
Linkedin: https://www.linkedin.com/in/mathu-c/

