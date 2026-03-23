# HireFlow - Off-Campus Auto Job Application Tool

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=black)
![Chrome Extension](https://img.shields.io/badge/Chrome-Extension-4285F4?logo=googlechrome&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

A job hunting automation tool for freshers and off-campus candidates. Scrapes job listings from LinkedIn, Naukri, Indeed and Internshala, auto-fills application forms using a Chrome extension, and tracks all applications in a dashboard.

## Features

- Scrapes jobs from 4 portals (LinkedIn, Naukri, Indeed, Internshala)
- Filter by job title, location, experience level
- Chrome extension to auto-fill job application forms
- Save your profile once, fill forms with one click
- Job tracker dashboard with status tracking (New, Applied, Interview, Rejected)
- Export jobs to CSV
- Email alerts for new job listings
- Works without storing any login credentials (safe scraping)

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Scraping | Python, BeautifulSoup, Requests |
| Browser Extension | JavaScript, Chrome Manifest V3 |
| Dashboard | HTML, CSS, JavaScript |
| Email Alerts | Python smtplib |
| Data Storage | CSV, JSON, LocalStorage |

## Project Structure

```
hireflow/
├── scraper/
│   ├── linkedin_scraper.py     # linkedin job scraper
│   ├── naukri_scraper.py       # naukri.com scraper
│   ├── indeed_scraper.py       # indeed.co.in scraper
│   ├── internshala_scraper.py  # internshala scraper
│   ├── job_scraper.py          # combines all scrapers
│   └── email_alert.py          # sends job alerts via email
├── extension/
│   ├── manifest.json           # chrome extension config
│   ├── popup.html              # extension popup UI
│   ├── popup.css               # popup styles
│   ├── popup.js                # popup logic
│   ├── content.js              # auto-fill script
│   └── content.css             # injected styles
├── dashboard/
│   ├── index.html              # job tracker page
│   ├── style.css               # dashboard styles
│   └── script.js               # dashboard logic
├── run_scraper.py              # main entry point
├── requirements.txt            # python dependencies
└── .env.example                # email config template
```

## Setup

### 1. Python Scraper

```bash
git clone https://github.com/pragatisingh1556/hireflow.git
cd hireflow
pip install -r requirements.txt
python run_scraper.py
```

### 2. Chrome Extension

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (top right toggle)
3. Click "Load unpacked"
4. Select the `extension/` folder
5. Pin the HireFlow extension
6. Fill your profile and click "Save Profile"
7. Go to any job portal and click "Auto Fill This Page"

### 3. Dashboard

Open `dashboard/index.html` in your browser. It shows scraped jobs with filters and status tracking.

### 4. Email Alerts (optional)

1. Copy `.env.example` to `.env`
2. Add your Gmail address and [App Password](https://myaccount.google.com/apppasswords)
3. Run the scraper with email alert enabled

## Screenshots

Coming soon

## What I Learned

- Web scraping with BeautifulSoup and handling different HTML structures
- Building Chrome extensions with Manifest V3
- Content scripts for DOM manipulation on external websites
- Sending HTML emails using Python smtplib
- Building a responsive dashboard with vanilla HTML/CSS/JS
- Working with localStorage for data persistence

## Future Improvements

- Add more job portals (Glassdoor, AngelList)
- Resume parser to auto-extract profile data
- Schedule scraper to run daily using cron job
- Add Google Sheets integration for tracking
- Browser notification for new matching jobs
