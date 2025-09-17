from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium import webdriver
from dotenv import load_dotenv

from jobs_manager import Jobs
from helper import filter_text
from gemini import model

import time
import os

options = Options()
options.add_argument("--headless=new")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")

load_dotenv()
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
LINKED_PW = os.getenv("LINKED_PW")


class LinkedInBot:
    def __init__(self, email, password, timeout=20):
        self.email = email
        self.password = password
        self.driver = uc.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, timeout)

    def login(self):
        self.driver.get("https://www.linkedin.com/feed/")

        email_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_field.send_keys(self.email)

        password_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.send_keys(self.password)

        sign_in_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        sign_in_btn.click()

    def go_to_jobs(self):
        # Navigate directly to the Jobs page for reliability instead of clicking the nav item
        self.driver.get("https://www.linkedin.com/jobs/")
        # Wait until the URL reflects the jobs section
        self.wait.until(EC.url_contains("/jobs"))

    def show_all_jobs(self):
        try:
            show_all_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[normalize-space()='Show all']")
                )
            )
            show_all_btn.click()
        except Exception:
            print("⚠️ 'Show all' button not found or not clickable.")

    def extract_data(self):
        job_data = []
        job_elements = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//li[contains(@class, 'ember-view')]")
            )
        )
        num_jobs = len(job_elements)
        for i in range(num_jobs):
            try:

                jobs_list = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//li[contains(@class, 'ember-view')]")
                    )
                )
                job = jobs_list[i]
                job.click()

                company_name = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            ".job-details-jobs-unified-top-card__company-name a",
                        )
                    )
                ).text

                job_title = self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//h1[@class='t-24 t-bold inline']/a")
                    )
                ).text

                prefrences_div = self.wait.until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "job-details-fit-level-preferences")
                    )
                )
                buttons = prefrences_div.find_elements(By.TAG_NAME, "button")
                prefrences = [btn.text.strip() for btn in buttons]

                # description_div = self.wait.until(
                #     EC.presence_of_element_located((By.ID, "job-details"))
                # )
                # full_description = description_div.text

                # responsibility = model.generate_content(
                #     "Extract the core responsibilities and roles of the developer from the following job description text. List each responsibility as a separate, concise point."
                #     + full_description
                # )
                # filtered_responsibility = filter_text(responsibility.text)

                # requirement = model.generate_content(
                #     "Extract the specific skills, qualifications, and experience required for the applicant from the job description below. Please list these as bullet points, focusing only on what the candidate needs to possess or demonstrate."
                #     + full_description
                # )
                # filtered_requirement = filter_text(requirement.text)

                # date_posted = self.wait.until(
                #     EC.visibility_of_element_located(
                #         (
                #             By.XPATH,
                #             "//span[contains(@class, 'tvm__text.tvm__text--low-emphasis:nth-of-type(3)') or contains(@class, 'tvm__text.tvm__text--positive:nth-of-type(3)')]",
                #         )
                #     )
                # ).text
                # all_spans = self.wait.until(
                #     EC.visibility_of_all_elements_located((By.CLASS_NAME, "tvm__text"))
                # )
                # for span in all_spans: 
                #     if 'ago' in span.text: 
                #         print(f"🪙{span.text}")
                current_page_url = self.driver.current_url
                job_data.append(
                    {
                        "company": company_name,
                        "title": job_title,
                        "prefrences": prefrences,
                        # "responsibility": filtered_responsibility,
                        # "requirement": filtered_requirement,
                        # "date-posted": date_posted,
                        "job-link": current_page_url,
                    }
                )
            except Exception as e:
                print(f" ⚠️ Error while extracting job data: {e}")

        jobs = Jobs(job_data)
        jobs.save_job_to_file()

    def run(self):
        try:
            self.login()
            self.go_to_jobs()
            self.show_all_jobs()
            self.extract_data()
            time.sleep(360)
        finally:
            self.driver.quit()


if __name__ == "__main__":
    bot = LinkedInBot(EMAIL_ACCOUNT, LINKED_PW)
    bot.run()
