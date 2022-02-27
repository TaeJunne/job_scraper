from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}

#s = HTMLSession()
c = {"NID": "511=d-uOQTUmVzRCT6DGL3RsF8URKXN_yYFbJ6wPE0A_iYWG24j7kaIjHXYcOCIMWVbdFYljeT1PcTG8PtF0H6R19ZNDcPrgFOh4-C4cT4nn5gldiTtrIehMgs_5V-XslMfRrUMDnBq4RwyG02-o3KTlqhlTvN6A7p68oPl6EGZyqX4", "DV": "A8Y5R7_LVXAnsNFUD5FEuifxmVGc8xfXaKa0v0CjmwIAAAA",
     "1P_JAR": "2022-02-27-06", "visits": "6", "adShuffer": "0", "new_user": "false", "cf_use_ob": "0", "ref": "https%3A%2F%2Fwww.google.com%2F", "cf_clearance": "Rag62Wk6F3ZJtItbfq3tPT.CTwAzYh2xPO4eLEOQ9nk-1645941696-0-150"}

# s.cookies.update(c)


def extract_jobs(result):
    try:
        title = result.find("h2", {"itemprop": "title"}).string.strip()
        company = result.find("h3", {"itemprop": "name"}).string.strip()
        if "💰" in result.find("div", class_="location").string:
            location = "No office location"
        else:
            location = result.find(
                "div", class_="location").string.strip(" 🌏🇺🇸")
        link = "https://remoteok.com" + \
            result.find("a", {"itemprop": "url"}).attrs["href"]
        return {"from": "RemoteOK", "title": title, "company": company, "location": location, "link": link}
    except:
        pass


def push_requests(url):
    elements = []
    r = requests.get(url, headers=headers, cookies=c)
    curSession = requests.Session()
    soup = BeautifulSoup(r.text, "html.parser")
    results = soup.find_all("td", class_="company_and_position")
    for result in results:
        job = extract_jobs(result)
        if job != None:
            elements.append(job)
    return elements


def get_jobs(word):
    url = f"https://remoteok.com/remote-dev+python-jobs"
    jobs = push_requests(url)
    return jobs
