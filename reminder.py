import schedule
import time
from datetime import datetime, timedelta
from database import get_upcoming_meetings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from plyer import notification  # Import the plyer library for pop-up notifications

def send_reminder(meeting):
    """Send a pop-up reminder for the upcoming meeting."""
    print(f"Reminder: You have a meeting at {meeting[1]} with {meeting[2]}. Location: {meeting[3]}")

    # Pop-up notification
    notification.notify(
        title=f"Meeting Reminder: {meeting[1]}",
        message=f"You have a meeting with {meeting[2]}. Location: {meeting[3]}",
        timeout=10  # Duration the notification stays on screen (in seconds)
    )

def send_notification_to_participants(meeting):
    """Send an email notification to all participants."""
    participants = meeting[2].split(', ')  # Assuming participants are stored as comma-separated emails
    
    # SMTP settings for sending emails (you may want to use a different email provider)
    sender_email = "your_email@gmail.com"
    password = "your_password"

    subject = f"Meeting Reminder: {meeting[1]}"
    body = f"Dear Participant,\n\nThis is a reminder for your meeting at {meeting[1]}.\nLocation: {meeting[3]}\n\nBest regards,\nYour Assistant"

    # Connect to the SMTP server and send the emails
    try:
        for participant in participants:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = participant
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, participant, msg.as_string())
                print(f"Notification sent to {participant}")
    except Exception as e:
        print(f"Error sending email: {e}")

def schedule_reminders():
    """Fetch meetings from the database and schedule reminders."""
    meetings = get_upcoming_meetings()

    for meeting in meetings:
        # Convert meeting datetime string to datetime object
        meeting_time = datetime.strptime(meeting[1], "%Y-%m-%d %H:%M:%S")

        # Schedule reminder 10 minutes before the meeting
        reminder_time = meeting_time - timedelta(minutes=10)
        
        # Schedule the task
        schedule.every().day.at(reminder_time.strftime("%H:%M")).do(send_reminder, meeting=meeting)
        schedule.every().day.at(reminder_time.strftime("%H:%M")).do(send_notification_to_participants, meeting=meeting)

def run_reminders():
    """Run the reminder scheduler indefinitely."""
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    run_reminders()
