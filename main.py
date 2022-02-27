from flask import Flask, render_template, request, redirect, send_file

from scraper import stackoverflow, weworkremotely, remoteok
from exporter import save_to_file


db = {"stackoverflow": {}, "remoteok": {}, "weworkremotely": {}}

app = Flask("SuperScrapper")


def existingJobs(website, word):
    existingJobs = db[website].get(word)
    if existingJobs:
        existing_jobs = existingJobs
    else:
        existing_jobs = globals()[website].get_jobs(word)
        db[website][word] = existing_jobs
    return existing_jobs


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/searchresult")
def search():
    jobs = []
    length = 0
    word = request.args.get("keyword")
    so = request.args.get("website1")
    remoteok = request.args.get("website2")
    wwr = request.args.get("website3")
    if word:
        word = word.lower()
        if so:
            jobs.append(existingJobs("stackoverflow", word))
        if remoteok:
            jobs.append(existingJobs("remoteok", word))
        if wwr:
            jobs.append(existingJobs("weworkremotely", word))
        elif not so and not remoteok and not wwr:
            jobs.append(existingJobs("stackoverflow", word))
            jobs.append(existingJobs("remoteok", word))
            jobs.append(existingJobs("weworkremotely", word))
        for i in range(len(jobs)):
            length += len(jobs[i])
        if length == 0:
            return render_template("opps.html")
    else:
        return redirect("/")
    return render_template("searchresult.html", searchingBy=word, resultsNumber=length, jobs=jobs, so=so, remoteok=remoteok, wwr=wwr)


@app.route("/export")
def export():
    list = []
    jobs = []

    try:
        word = request.args.get("keyword")
        if not word:
            raise Exception()
        word = word.lower()
        website1 = request.args.get("website1")
        list.append(website1)
        website2 = request.args.get("website2")
        list.append(website2)
        website3 = request.args.get("website3")
        list.append(website3)
        for i in list:
            if i != 'None':
                for job in db[i][word]:
                    jobs.append(job)
        if list[0] == "None" and list[1] == "None" and list[2] == "None":
            for job in db["stackoverflow"][word]:
                jobs.append(job)
            for job in db["remoteok"][word]:
                jobs.append(job)
            for job in db["weworkremotely"][word]:
                jobs.append(job)
        save_to_file(jobs)
        return send_file("jobs.csv")
    except:
        return redirect("/")


app.run(host="127.0.0.1")
