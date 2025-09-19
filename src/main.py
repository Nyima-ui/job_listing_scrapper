import time
import os
import random

from helper import write_in_json
from gemini import model

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from dotenv import load_dotenv

# =================
# CONFIG & SETUP
# =================

load_dotenv()

EMAIL = os.getenv("EMAIL_ACCOUNT")
PASSWORD = os.getenv("LINKED_PW")
PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")

# Directories
script_dir = os.path.dirname(os.path.abspath(__file__))
extension_path = os.path.join(script_dir, os.pardir, "proxy_auth_extension")

# Proxy - Oxylabs
proxy = f"http://{PROXY_USER}:{PROXY_PASS}@unblock.oxylabs.io:60000"


def create_driver():
    options = uc.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument(f"--load-extension={extension_path}")

    driver = uc.Chrome(options=options)
    driver.wait = WebDriverWait(driver, 20)
    return driver


# =================
# AUTH & NAVIGATION
# =================


def login_linkedIn(driver):
    driver.get("https://www.linkedin.com/feed/")

    email_field = driver.wait.until(EC.presence_of_element_located((By.ID, "username")))
    email_field.send_keys(EMAIL)
    password_field = driver.wait.until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_field.send_keys(PASSWORD)
    signin_btn = driver.wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]'))
    )
    signin_btn.click()
    # ---- 30 seconds to solve the captcha manually ----
    time.sleep(30)


def go_to_jobs(driver):
    jobs_btn = driver.wait.until(
        EC.element_to_be_clickable((By.XPATH, '//span[text()="Jobs"]'))
    )
    jobs_btn.click()


def show_all_jobs(driver):
    show_all_btn = driver.wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//a[contains(@href, "/jobs/collections/recommended/")]',
            )
        )
    )
    show_all_btn.click()


# =================
# DATE EXTRACTION
# =================


def get_job_title(driver):
    job_title = driver.wait.until(
        EC.presence_of_element_located(
            (By.XPATH, '//h1[@class="t-24 t-bold inline"]/a')
        )
    ).text
    return job_title


def get_company_name(driver):
    company_name = driver.wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__company-name a")
        )
    ).text
    return company_name


def get_preferences(driver):
    try:
        preferences_div = driver.wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "job-details-fit-level-preferences")
            )
        )
        buttons = preferences_div.find_elements(By.TAG_NAME, "button")
        prefrences = [btn.text.strip() for btn in buttons]
        return prefrences
    except Exception:
        return []


def get_date_posted(driver):
    spans = driver.wait.until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "tvm__text"))
    )
    for span in spans:
        if "ago" in span.text:
            return span.text
    return None


def get_job_desciption(driver):
    description_div = driver.wait.until(
        EC.presence_of_element_located((By.ID, "job-details"))
    )
    description_text = description_div.text.strip()
    responsibility_prompt = (
        "Here is a job description. Extract only the job responsibilities as a clean, concise list. "
        "Don’t add any extra text or introduction—just output the list directly.\n\n"
        f"{description_text}"
    )
    requirement_prompt = (
        "Here is a job description. Extract only the job requirements as a clean, concise list. "
        "Don’t add any extra text or introduction—just output the list directly.\n\n"
        f"{description_text}"
    )
    responsibility = model.generate_content(responsibility_prompt).text
    requirement = model.generate_content(requirement_prompt).text
    return {"responsibility": responsibility, "requirement": requirement}


# =================
# SCRAPPER LOOP
# =================
def click_each_job(driver):
    jobs_data = []
    try:
        jobs_card = driver.wait.until(
            EC.visibility_of_any_elements_located(
                (By.XPATH, "//li[contains(@class, 'ember-view')]")
            )
        )
        for job_card in jobs_card:
            job_card.click()
            sleep_time1 = random.uniform(3, 8)
            sleep_time2 = random.uniform(1, 3)
            time.sleep(sleep_time1)

            job_description = get_job_desciption(driver)
            time.sleep(sleep_time2)
            job = {
                "job-title": get_job_title(driver),
                "company-name": get_company_name(driver),
                "preferences": get_preferences(driver),
                "date-posted": get_date_posted(driver),
                "responsibility": job_description["responsibility"],
                "requirement": job_description["requirement"],
                "job-link": driver.current_url,
            }
            jobs_data.append(job)
            print(f"✅ Extracted a job")

    except Exception as e:
        print(f"❌ Error extracting job data  {e}")
    return jobs_data


# =================
# MAIN
# =================
def main():
    driver = create_driver()
    login_linkedIn(driver)
    go_to_jobs(driver)
    show_all_jobs(driver)
    click_each_job(driver)

    jobs_list = click_each_job(driver)
    write_in_json(jobs_list)
    print(f"✅ Scraped {len(jobs_list)} jobs and saved to file.")
    time.sleep(60)
    driver.quit()


if __name__ == "__main__":
    main()
