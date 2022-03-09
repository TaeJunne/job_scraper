import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}


def job_count(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser").select_one(
        "#job-search-form > div.d-flex.fd-row.jc-space-between.ai-center > div.flex--item.js-search-title.-header.seo-header > span").string
    jobCount = int(soup.split()[0])
    return jobCount


def extract_jobs(result):
    try:
        title = result.select_one(
            "div.flex--item.fl1 > h2 > a.s-link").attrs["title"]
        company = result.select_one(
            "div.flex--item.fl1 > h3 > span:first-child").string.strip()
        location = result.select_one(
            "div.flex--item.fl1 > h3 >span:nth-child(2)").string.strip()
        link = "https://stackoverflow.com" + \
            result.select_one("div.flex--item.fl1 > h2 > a").attrs["href"]
        return{"from": "StackOverflow", "title": title, "company": company, "location": location, "link": link}
    except:
        pass


def push_requests(url, jobCount):
    elements = []
    if jobCount != 0:
        for i in range(jobCount // 25 + 1):
            r = requests.get(
                f"{url}&pg={i + 1}", headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            ad = soup.select_one("#content > div.js-search-container.search-container.mbn24 > div > div.flex--item.fl1.br.bc-black-2 > div > div.listResults > div.bb.bc-black-2.fc-black-500")
            if ad:
                results = ad.previous_siblings
            else:
                results = soup.select(
                    "#content > div.js-search-container.search-container.mbn24 > div > div.flex--item.fl1.br.bc-black-2 > div > div.listResults div.d-flex")
            for result in results:
                job = extract_jobs(result)
                if job != None:
                    elements.append(job)
    return elements


def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?r=true&q={word}"
    jobCount = job_count(url)
    jobs = push_requests(url, jobCount)
    return jobs
