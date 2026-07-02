import requests
from bs4 import BeautifulSoup
import csv

# 1. Fetch the webpage
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)

# 2. Parse the HTML
soup = BeautifulSoup(page.content, "html.parser")

# The jobs are inside a container with id="ResultsContainer"
results = soup.find(id="ResultsContainer")

# Find all job cards
job_cards = results.find_all("div", class_="card-content")

# 3. Prepare to store data
jobs = []

for job in job_cards:
    # Extract required fields with safe handling for missing data
    title_element = job.find("h2", class_="title")
    title = title_element.text.strip() if title_element else "N/A"
    
    company_element = job.find("h3", class_="company")
    company = company_element.text.strip() if company_element else "N/A"
    
    location_element = job.find("p", class_="location")
    location = location_element.text.strip() if location_element else "N/A"
    
    # Get the detail page URL (the "Apply" link)
    link_element = job.find_all("a")[-1]  # Usually the last link is "Apply"
    link = link_element["href"] if link_element and "href" in link_element.attrs else "N/A"
    
    # Make full URL if it's relative
    if link.startswith("/"):
        link = "https://realpython.github.io/fake-jobs" + link
    
    jobs.append({
        "title": title,
        "company": company,
        "location": location,
        "url": link
    })

# 4. Save to CSV
with open("fake_jobs.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["title", "company", "location", "url"])
    writer.writeheader()
    writer.writerows(jobs)

print(f"✅ Scraped {len(jobs)} job listings and saved to fake_jobs.csv")