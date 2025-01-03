# CalenderAI
Meeting Reminder Application
This Python-based application automatically fetches meeting details from your emails and sends timely reminders. The tool is designed to improve productivity by automatically notifying you and all meeting participants before meetings, so you never miss an appointment.

Features:
Fetch Meeting Data: Automatically retrieves meeting details (time, participants, location) from your emails.
Pop-Up Notifications: Sends desktop pop-up reminders 10 minutes before each meeting.
Email Notifications: Sends email reminders to all meeting participants.
Background Execution: Runs automatically at system startup using cron jobs (Mac/Linux) or Task Scheduler (Windows).
Database: Stores meeting details in a local SQLite database for easy retrieval and scheduling.
Easy Deployment: Can be packaged as an executable for easy distribution using PyInstaller.

Technologies Used:
Python
SQLite (for local storage)
Plyer (for pop-up notifications)
smtplib (for email notifications)
Schedule (for scheduling reminders)

How to Use:
Clone or download the repository.
Install the required libraries with pip install -r requirements.txt.
Set up your email credentials and configure your email provider.
Set up background execution (via cron jobs or Task Scheduler).
The system will automatically fetch meeting details and send reminders.
