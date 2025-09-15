from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from dotenv import load_dotenv


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
        ul = self.wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "ZoMBgxcPjwbXwxVDiHJRnBmTIhQPBYxqqgkZo")
            )
        )
        jobs_list = ul.find_elements(By.TAG_NAME, "li")
        for job in jobs_list:
            job.click()
            job_data = []
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
            job_data.append({"company": company_name, "title": job_title})
        print(job_data)

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
