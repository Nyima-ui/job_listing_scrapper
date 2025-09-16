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
    def __init__(
        self,
        jobs_data,
        filename=None,
    ):
        if filename is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(base_dir, "..", "data", "jobs.json")

        self.filename = filename
        self.jobs_data = jobs_data

    def save_job_to_file(self):
        with open(self.filename, "w", encoding='utf-8') as f:
            json.dump(self.jobs_data, f, indent=4)




