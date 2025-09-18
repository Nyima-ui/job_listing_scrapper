import time
import os

from helper import write_in_json

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
                '//a[@href="https://www.linkedin.com/jobs/collections/recommended/?discover=recommended&discoveryOrigin=JOBS_HOME_JYMBII"]',
            )
        )
    )
    show_all_btn.click()


jobs_list = []


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
    preferences_div = driver.wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "job-details-fit-level-preferences")
        )
    )
    buttons = preferences_div.find_elements(By.TAG_NAME, "button")
    prefrences = [btn.text.strip() for btn in buttons]
    return prefrences


def get_date_posted(driver):
    spans = driver.wait.until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "tvm__text"))
    )
    span_with_ago = None
    for span in spans:
        if "ago" in span.text:
            span_with_ago = span
            break
    if span_with_ago:
        return span_with_ago.text
    else:
        print("❌ Couldn't get the span text or span")
        return None
    




def click_each_job(driver):
    jobs_card = driver.wait.until(
        EC.visibility_of_any_elements_located(
            (By.XPATH, "//li[contains(@class, 'ember-view')]")
        )
    )
    for job_card in jobs_card:
        job_card.click()
        time.sleep(1.5)

        job = {}
        job["job-title"] = get_job_title(driver)
        job["company-name"] = get_company_name(driver)
        job["preferences"] = get_preferences(driver)
        job["date-posted"] = get_date_posted(driver)
        job["job-link"] = driver.current_url
        jobs_list.append(job)

    time.sleep(10)


def main():
    driver = create_driver()
    login_linkedIn(driver)
    go_to_jobs(driver)
    show_all_jobs(driver)
    click_each_job(driver)

    write_in_json(jobs_list)


if __name__ == "__main__":
    main()
