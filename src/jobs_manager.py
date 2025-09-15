import os
import json


class Job:
    def __init__(
        self,
        id,
        company,
        title,
        location,
        employment_type,
        skill_requirement,
        date_posted,
        job_link,
    ):
        self.id = id
        self.company = company
        self.title = title
        self.location = location
        self.employment_type = employment_type
        self.skill_requirement = skill_requirement
        self.date_posted = date_posted
        self.job_link = job_link

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "title": self.title,
            "location": self.location,
            "employment_type": self.employment_type,
            "skill_requirement": self.skill_requirement,
            "date_posted": self.date_posted,
            "job_link": self.job_link,
        }


class Jobs:
    def __init__(self, filename="/data/jobs.json"):
        self.filename = filename
        self.jobs = self.load_jobs()

    def load_jobs(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return []

    def save_job(self):
        with open(self.filename, "w") as f:
            json.dump(self.jobs, f, indent=4)

    def add_job(self):
        pass
