import os
import json


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
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.jobs_data, f, indent=4)
    

def json_to_text(jsonfile, output_file="text.md"):
    if not jsonfile or not os.path.exists(jsonfile):
        print("❌ Provide a valid file")
        return

    try:
        with open(jsonfile, "r", encoding="utf-8") as f:
            data = json.load(f)

        with open(output_file, "w", encoding="utf-8") as f:
            for job in data:
                f.write(f"# {job.get('company', '')}\n")
                f.write(f"## {job.get('title', '')}\n\n")

                # Preferences
                if "prefrences" in job:
                    f.write("### Preferences\n")
                    for pref in job["prefrences"]:
                        f.write(f"- {pref}\n")
                    f.write("\n")

                # Responsibilities
                if "responsibility" in job:
                    f.write("### Responsibilities\n")
                    f.write(job["responsibility"] + "\n\n")

                # Requirements
                if "requirement" in job:
                    f.write("### Requirements\n")
                    f.write(job["requirement"] + "\n\n")

        print(f"✅ Extracted text written to {output_file}")

    except Exception as e:
        print(f"⚠️ Error: {e}")
            
        
        
base_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(base_dir, "..", "data", "jobs.json")

# json_to_text(filename, r"C:\Users\Tenzin Nyima\job_listing_scraper\data\text.md")