from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from dotenv import load_dotenv

from jobs_manager import Jobs

import time
import os

load_dotenv()
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
LINKED_PW = os.getenv("LINKED_PW")


class LinkedInBot:
    def __init__(self, email, password, timeout=10):
        self.email = email
        self.password = password
        self.driver = uc.Chrome()
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
        jobs_link = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Jobs']"))
        )
        jobs_link.click()

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

                time.sleep(2)

                company = self.wait.until(
                    EC.presence_of_element_located(
                        (
                            By.CSS_SELECTOR,
                            ".job-details-jobs-unified-top-card__company-name a",
                        )
                    )
                )
                company_name = company.text

                title = self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//h1[@class='t-24 t-bold inline']/a")
                    )
                )
                job_title = title.text

                prefrences_div = self.wait.until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "job-details-fit-level-preferences")
                    )
                )
                buttons = prefrences_div.find_elements(By.TAG_NAME, "button")
                prefrences = [btn.text.strip() for btn in buttons]

                description_div = self.wait.until(
                    EC.presence_of_element_located((By.ID, "job-details"))
                )
                # desc_spans = description_div.find_elements(By.TAG_NAME, "span")
                # full_description = "\n".join(
                #     [span.text.strip() for span in desc_spans if span.text.strip()]
                # )
                full_description = description_div.text
                job_data.append(
                    {
                        "company": company_name,
                        "title": job_title,
                        "prefrences": prefrences,
                        "description": full_description,
                    }
                )
            except Exception as e:
                print(f"stale element reference action{e}")

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
