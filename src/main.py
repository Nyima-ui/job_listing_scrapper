from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time

def connect_linked(): 
    with webdriver.Chrome() as driver: 
        driver.get("https://www.youtube.com/watch?v=Y21OR1OPC9A")
        time.sleep(10)


if __name__ == "__main__": 
    connect_linked()