
        
      
      
      
      
      
      
# def click_each_job(driver):
#     jobs_data = []

#     job_index = 0
#     while True:
#         try:
#             jobs_card = driver.wait.until(
#                 EC.visibility_of_any_elements_located(
#                     (By.XPATH, "//li[contains(@class, 'ember-view')]")
#                 )
#             )
#             if job_index >= len(jobs_card):
#                 break

#             job_card = jobs_card[job_index]
#             driver.execute_script("arguments[0].scrollIntoView();", job_card)
#             job_card.click()
#             time.sleep(1.5)

#             job = {
#                 "job-title": get_job_title(driver),
#                 "company-name": get_company_name(driver),
#                 "preferences": get_preferences(driver),
#                 "date-posted": get_date_posted(driver),
#                 "job-link": driver.current_url,
#             }

#             jobs_data.append(job)
#             print(f"✅ Extracted job {job_index + 1}")
#             job_index += 1
#         except Exception as e:
#             print(f"❌ Error extracting job data {job_index + 1} {e}")
#             job_index += 1

#     return jobs_data