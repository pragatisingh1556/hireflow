# linkedin job scraper
# scrapes job listings from linkedin without login
# uses their public job search page

import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_linkedin(job_title, location="India"):
    """scrape jobs from linkedin public listings"""

    print("searching linkedin for:", job_title)

    jobs = []

    # linkedin public job search url
    # found this from inspecting the network tab
    query = job_title.replace(" ", "%20")
    loc = location.replace(" ", "%20")
    url = "https://www.linkedin.com/jobs/search?keywords=" + query + "&location=" + loc

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("linkedin returned status:", response.status_code)
            return jobs

        soup = BeautifulSoup(response.text, "html.parser")

        # linkedin uses these classes for job cards
        # might break if they change their html
        job_cards = soup.find_all("div", class_="base-card")

        for card in job_cards[:15]:  # only take first 15
            try:
                title_tag = card.find("h3", class_="base-search-card__title")
                company_tag = card.find("h4", class_="base-search-card__subtitle")
                location_tag = card.find("span", class_="job-search-card__location")
                link_tag = card.find("a", class_="base-card__full-link")

                title = "N/A"
                if title_tag:
                    title = title_tag.text.strip()

                company = "N/A"
                if company_tag:
                    company = company_tag.text.strip()

                job_location = "N/A"
                if location_tag:
                    job_location = location_tag.text.strip()

                link = ""
                if link_tag:
                    link = link_tag["href"]

                job = {
                    "title": title,
                    "company": company,
                    "location": job_location,
                    "link": link,
                    "source": "LinkedIn"
                }
                jobs.append(job)

            except Exception as e:
                # skip this card if something went wrong
                continue

        print("found", len(jobs), "jobs on linkedin")

    except requests.exceptions.Timeout:
        print("linkedin request timed out")
    except Exception as e:
        print("error scraping linkedin:", str(e))

    # small delay so we dont get blocked
    time.sleep(random.uniform(1, 3))

    return jobs


# test it
if __name__ == "__main__":
    results = scrape_linkedin("python developer", "Bangalore")
    for job in results:
        print(job["title"], "-", job["company"])
