import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}


def extract_jobs(result):
    try:
        title = result.select_one("a span.title").string
        company = result.find("span", class_="company").string
        location = result.find("span", class_="region company").string
        link = "https://weworkremotely.com" + \
            result.select_one("li > a").attrs["href"]
        return {"from": "WeWorkRemotely", "title": title, "company": company, "location": location, "link": link}
    except:
        pass


def push_requests(url):
    elements = []
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    categories = soup.select("#job_list section.jobs")
    for category in categories:
        if "Full-Stack" in category.find("a").string:
            category_num = "#category-2"
        elif "Front-End" in category.find("a").string:
            category_num = "#category-17"
        elif "Back-End" in category.find("a").string:
            category_num = "#category-18"
        elif "Other" in category.find("a").string:
            category_num = "#category-4"
        else:
            category_num = "None"
        results = soup.select(f"{category_num} > article > ul > li")
        for result in results:
            job = extract_jobs(result)
            if job != None:
                elements.append(job)
    return elements


def get_jobs(word):
    url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    jobs = push_requests(url)
    return jobs
