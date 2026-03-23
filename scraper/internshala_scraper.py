# internshala job/internship scraper
# good for freshers - lots of entry level jobs
# public page scraping

import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_internshala(job_title, location=""):
    """scrape internships and jobs from internshala"""

    print("searching internshala for:", job_title)

    jobs = []

    # internshala url format is different
    query = job_title.lower().replace(" ", "-")
    url = "https://internshala.com/internships/" + query + "-internship"

    if location:
        url = url + "/in-" + location.lower().replace(" ", "-")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("internshala returned status:", response.status_code)
            return jobs

        soup = BeautifulSoup(response.text, "html.parser")

        # internshala uses these for listing cards
        job_cards = soup.find_all("div", class_="individual_internship")

        # try alternate class name
        if len(job_cards) == 0:
            job_cards = soup.find_all("div", class_="internship_meta")

        for card in job_cards[:15]:
            try:
                title_tag = card.find("h3", class_="heading_4_5")
                if not title_tag:
                    title_tag = card.find("a", class_="view_detail_button")

                company_tag = card.find("h4", class_="heading_6")
                if not company_tag:
                    company_tag = card.find("p", class_="company_name")

                location_tag = card.find("a", class_="location_link")
                if not location_tag:
                    location_tag = card.find("p", id="location_names")

                link_tag = card.find("a", class_="view_detail_button")

                title = "N/A"
                if title_tag:
                    title = title_tag.text.strip()

                company = "N/A"
                if company_tag:
                    company = company_tag.text.strip()

                job_location = "Remote"
                if location_tag:
                    job_location = location_tag.text.strip()

                link = ""
                if link_tag and link_tag.get("href"):
                    href = link_tag["href"]
                    if href.startswith("/"):
                        link = "https://internshala.com" + href
                    else:
                        link = href

                job = {
                    "title": title,
                    "company": company,
                    "location": job_location,
                    "link": link,
                    "source": "Internshala"
                }
                jobs.append(job)

            except Exception as e:
                continue

        print("found", len(jobs), "jobs on internshala")

    except requests.exceptions.Timeout:
        print("internshala request timed out")
    except Exception as e:
        print("error scraping internshala:", str(e))

    time.sleep(random.uniform(1, 3))

    return jobs


if __name__ == "__main__":
    results = scrape_internshala("python", "bangalore")
    for job in results:
        print(job["title"], "-", job["company"])
