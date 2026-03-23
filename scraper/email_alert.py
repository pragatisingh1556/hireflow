# email alert - sends job results to your email
# uses gmail smtp - you need to enable "app passwords" in google account
# learned this from a geeksforgeeks article

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# load .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


def send_job_alert(jobs, job_title):
    """send email with job listings"""

    sender_email = os.getenv("EMAIL_ADDRESS")
    sender_password = os.getenv("EMAIL_PASSWORD")
    receiver_email = os.getenv("ALERT_EMAIL")

    if not sender_email or not sender_password:
        print("email credentials not set in .env file")
        print("skipping email alert")
        return False

    # build the email body
    subject = "HireFlow Alert: " + str(len(jobs)) + " new " + job_title + " jobs found"

    # create html table for jobs
    html_body = "<h2>HireFlow Job Alert</h2>"
    html_body = html_body + "<p>Found <b>" + str(len(jobs)) + "</b> jobs for: " + job_title + "</p>"
    html_body = html_body + "<table border='1' cellpadding='8' cellspacing='0' style='border-collapse: collapse;'>"
    html_body = html_body + "<tr style='background-color: #7C4DFF; color: white;'>"
    html_body = html_body + "<th>Title</th><th>Company</th><th>Location</th><th>Source</th><th>Link</th>"
    html_body = html_body + "</tr>"

    for i in range(len(jobs)):
        job = jobs[i]
        # alternate row colors
        if i % 2 == 0:
            bg = "#f9f9f9"
        else:
            bg = "#ffffff"

        html_body = html_body + "<tr style='background-color: " + bg + ";'>"
        html_body = html_body + "<td>" + job.get("title", "N/A") + "</td>"
        html_body = html_body + "<td>" + job.get("company", "N/A") + "</td>"
        html_body = html_body + "<td>" + job.get("location", "N/A") + "</td>"
        html_body = html_body + "<td>" + job.get("source", "N/A") + "</td>"

        link = job.get("link", "")
        if link:
            html_body = html_body + "<td><a href='" + link + "'>Apply</a></td>"
        else:
            html_body = html_body + "<td>-</td>"

        html_body = html_body + "</tr>"

    html_body = html_body + "</table>"
    html_body = html_body + "<br><p style='color: #888;'>Sent by HireFlow - Off Campus Auto Job Finder</p>"

    # create the email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.attach(MIMEText(html_body, "html"))

    try:
        # connect to gmail smtp
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("email alert sent to", receiver_email)
        return True

    except Exception as e:
        print("failed to send email:", str(e))
        return False


if __name__ == "__main__":
    # test with dummy data
    test_jobs = [
        {
            "title": "Python Developer",
            "company": "TCS",
            "location": "Bangalore",
            "source": "LinkedIn",
            "link": "https://example.com"
        },
        {
            "title": "Backend Engineer",
            "company": "Infosys",
            "location": "Hyderabad",
            "source": "Naukri",
            "link": "https://example.com"
        }
    ]

    send_job_alert(test_jobs, "python developer")
