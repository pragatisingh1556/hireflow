# naukri.com job scraper
# scrapes fresher jobs from naukri
# no login needed - uses public search page

import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_naukri(job_title, location="India"):
    """scrape jobs from naukri.com"""

    print("searching naukri for:", job_title)

    jobs = []

    # naukri search url format
    query = job_title.replace(" ", "-")
    loc = location.lower().replace(" ", "-")
    url = "https://www.naukri.com/" + query + "-jobs-in-" + loc

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("naukri returned status:", response.status_code)
            return jobs

        soup = BeautifulSoup(response.text, "html.parser")

        # naukri job card structure
        job_cards = soup.find_all("article", class_="jobTuple")

        # if that doesnt work try the new layout
        if len(job_cards) == 0:
            job_cards = soup.find_all("div", class_="srp-jobtuple-wrapper")

        for card in job_cards[:15]:
            try:
                title_tag = card.find("a", class_="title")
                company_tag = card.find("a", class_="subTitle")
                location_tag = card.find("li", class_="fleft")
                link_tag = card.find("a", class_="title")

                # try alternate selectors if first ones dont work
                if not title_tag:
                    title_tag = card.find("a")
                if not company_tag:
                    company_tag = card.find("span")

                title = "N/A"
                if title_tag:
                    title = title_tag.text.strip()

                company = "N/A"
                if company_tag:
                    company = company_tag.text.strip()

                job_location = location
                if location_tag:
                    job_location = location_tag.text.strip()

                link = ""
                if link_tag and link_tag.get("href"):
                    link = link_tag["href"]

                job = {
                    "title": title,
                    "company": company,
                    "location": job_location,
                    "link": link,
                    "source": "Naukri"
                }
                jobs.append(job)

            except Exception as e:
                continue

        print("found", len(jobs), "jobs on naukri")

    except requests.exceptions.Timeout:
        print("naukri request timed out")
    except Exception as e:
        print("error scraping naukri:", str(e))

    time.sleep(random.uniform(1, 3))

    return jobs


if __name__ == "__main__":
    results = scrape_naukri("python developer", "bangalore")
    for job in results:
        print(job["title"], "-", job["company"])
