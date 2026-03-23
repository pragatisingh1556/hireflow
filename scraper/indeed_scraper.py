# indeed job scraper
# scrapes job listings from indeed india
# public page - no login required

import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_indeed(job_title, location="India"):
    """scrape jobs from indeed.co.in"""

    print("searching indeed for:", job_title)

    jobs = []

    query = job_title.replace(" ", "+")
    loc = location.replace(" ", "+")
    url = "https://www.indeed.co.in/jobs?q=" + query + "&l=" + loc

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("indeed returned status:", response.status_code)
            return jobs

        soup = BeautifulSoup(response.text, "html.parser")

        # indeed uses these divs for job results
        job_cards = soup.find_all("div", class_="job_seen_beacon")

        # fallback selector
        if len(job_cards) == 0:
            job_cards = soup.find_all("td", class_="resultContent")

        for card in job_cards[:15]:
            try:
                title_tag = card.find("h2", class_="jobTitle")
                if not title_tag:
                    title_tag = card.find("a", {"data-jk": True})

                company_tag = card.find("span", {"data-testid": "company-name"})
                if not company_tag:
                    company_tag = card.find("span", class_="companyName")

                location_tag = card.find("div", {"data-testid": "text-location"})
                if not location_tag:
                    location_tag = card.find("div", class_="companyLocation")

                # get the link
                link_tag = card.find("a", href=True)
                link = ""
                if link_tag:
                    href = link_tag.get("href", "")
                    if href.startswith("/"):
                        link = "https://www.indeed.co.in" + href
                    else:
                        link = href

                title = "N/A"
                if title_tag:
                    # sometimes title is inside a span
                    span = title_tag.find("span")
                    if span:
                        title = span.text.strip()
                    else:
                        title = title_tag.text.strip()

                company = "N/A"
                if company_tag:
                    company = company_tag.text.strip()

                job_location = location
                if location_tag:
                    job_location = location_tag.text.strip()

                job = {
                    "title": title,
                    "company": company,
                    "location": job_location,
                    "link": link,
                    "source": "Indeed"
                }
                jobs.append(job)

            except Exception as e:
                continue

        print("found", len(jobs), "jobs on indeed")

    except requests.exceptions.Timeout:
        print("indeed request timed out")
    except Exception as e:
        print("error scraping indeed:", str(e))

    time.sleep(random.uniform(1, 3))

    return jobs


if __name__ == "__main__":
    results = scrape_indeed("software developer", "bangalore")
    for job in results:
        print(job["title"], "-", job["company"])
