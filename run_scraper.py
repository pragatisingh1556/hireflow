# main script - run this to scrape jobs
# searches all 4 portals and saves results
# also sends email alert if configured

import sys
import os

# add scraper folder to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scraper"))

from job_scraper import scrape_all_portals, save_to_csv, save_to_json
from email_alert import send_job_alert


def main():
    print("\n=============================")
    print("   HireFlow Job Scraper")
    print("=============================\n")

    # ask user what to search
    job_title = input("enter job title (eg: python developer): ").strip()
    if job_title == "":
        job_title = "python developer"
        print("using default:", job_title)

    location = input("enter location (eg: Bangalore): ").strip()
    if location == "":
        location = "India"
        print("using default:", location)

    # run all scrapers
    jobs = scrape_all_portals(job_title, location)

    if len(jobs) == 0:
        print("\nno jobs found. try different keywords or check your internet")
        return

    # save results
    save_to_csv(jobs)
    save_to_json(jobs)

    # ask if user wants email alert
    send_email = input("\nsend email alert? (y/n): ").strip().lower()
    if send_email == "y":
        send_job_alert(jobs, job_title)

    print("\n--- done! ---")
    print("csv saved in jobs_data/ folder")
    print("open dashboard/index.html to see results")


if __name__ == "__main__":
    main()
