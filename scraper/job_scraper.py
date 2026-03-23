# main job scraper - combines all 4 portals
# runs all scrapers and saves results to csv

import os
import csv
from datetime import datetime

from linkedin_scraper import scrape_linkedin
from naukri_scraper import scrape_naukri
from indeed_scraper import scrape_indeed
from internshala_scraper import scrape_internshala


def scrape_all_portals(job_title, location="India"):
    """run all scrapers and combine results"""

    print("\n===== HireFlow Job Scraper =====")
    print("searching for:", job_title)
    print("location:", location)
    print("================================\n")

    all_jobs = []

    # scrape each portal one by one
    linkedin_jobs = scrape_linkedin(job_title, location)
    all_jobs = all_jobs + linkedin_jobs

    naukri_jobs = scrape_naukri(job_title, location)
    all_jobs = all_jobs + naukri_jobs

    indeed_jobs = scrape_indeed(job_title, location)
    all_jobs = all_jobs + indeed_jobs

    internshala_jobs = scrape_internshala(job_title, location)
    all_jobs = all_jobs + internshala_jobs

    print("\n--- total jobs found:", len(all_jobs), "---")
    print("linkedin:", len(linkedin_jobs))
    print("naukri:", len(naukri_jobs))
    print("indeed:", len(indeed_jobs))
    print("internshala:", len(internshala_jobs))

    return all_jobs


def save_to_csv(jobs, filename=None):
    """save job list to a csv file"""

    if len(jobs) == 0:
        print("no jobs to save")
        return

    # create jobs_data folder if it doesnt exist
    data_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "jobs_data")
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # filename with date so we can track history
    if filename is None:
        today = datetime.now().strftime("%Y-%m-%d")
        filename = "jobs_" + today + ".csv"

    filepath = os.path.join(data_folder, filename)

    # write to csv
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "location", "source", "link"])
        writer.writeheader()

        for job in jobs:
            writer.writerow(job)

    print("saved", len(jobs), "jobs to", filepath)
    return filepath


def save_to_json(jobs, filename=None):
    """save jobs as json - useful for the dashboard"""

    import json

    if len(jobs) == 0:
        print("no jobs to save")
        return

    # save to dashboard data folder
    dashboard_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard")
    if not os.path.exists(dashboard_folder):
        os.makedirs(dashboard_folder)

    if filename is None:
        filename = "jobs.json"

    filepath = os.path.join(dashboard_folder, filename)

    # add scraped date to each job
    today = datetime.now().strftime("%Y-%m-%d")
    for job in jobs:
        job["scraped_date"] = today
        job["status"] = "new"  # new, applied, interview, rejected

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)

    print("saved json to", filepath)
    return filepath


# run the scraper
if __name__ == "__main__":
    # change these to whatever you want to search
    search_title = "python developer"
    search_location = "Bangalore"

    jobs = scrape_all_portals(search_title, search_location)

    # save as csv and json
    save_to_csv(jobs)
    save_to_json(jobs)

    print("\ndone! check the jobs_data folder for csv")
    print("and dashboard folder for json")
