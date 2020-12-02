# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os
import shutil
import time

# Prompt user input
month = input("Enter month: ")
year = input("Enter year: ")

# Set options for headless Chrome
download_path = '<default_download_path>'
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("--disable-notifications")
options.add_argument('--no-sandbox')
options.add_argument('--verbose')
options.add_experimental_option("prefs", {
        "download.default_directory": download_path,
        "download.prompt_for_download": False, # To auto download the file
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
        "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
})
options.add_argument('--disable-gpu')
options.add_argument('--disable-software-rasterizer')

# Set Chrome driver path (pls change to correct driver path)
DRIVER_PATH = '<driver_path>'
# driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

# Read credentials and URL
credentials = pd.read_csv('Credentials.csv')
credentials.fillna(-999999, inplace=True)

# Send GET request to access site
driver.get(credentials['URL'][0])

# Send username and password to input, then click login button
driver.find_element_by_id('username').send_keys(credentials['Username'][0])
driver.find_element_by_id('password').send_keys(credentials['Password'][0])
driver.find_element_by_xpath('/html/body/form/table/tbody/tr[1]/td[2]/table/tbody/tr[3]/td[3]/div/input').click()

# time.sleep() is to prevent the next command to run before the page is loaded
time.sleep(5)

# Validate login is successful by finding logout button
try:
    title = driver.find_element_by_xpath("//*[ text() = 'Logout' ]")
    print('Successfully logged in')
except NoSuchElementException:
    print('Incorrect login/password')

# Access document element
driver.find_element_by_xpath('/html/body/map/area[3]').click()
time.sleep(5)

driver.find_element_by_xpath('/html/body/table[1]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[2]/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table[1]/tbody/tr[2]/td/table/tbody/tr/td/a/img').click()
time.sleep(5)

# Select month and year using dropdown box
driver.find_element_by_xpath("//select[@name='year']/option[@value='" + year + "']").click()
driver.find_element_by_xpath("//select[@name='month']/option[@value='" + month + "']").click()
time.sleep(5)

driver.find_element_by_xpath('/html/body/div/table[3]/tbody/tr[2]/td/form/table/tbody/tr/td[3]/div/img').click()
time.sleep(5)

# Logout (confirming the alert popup)
driver.find_element_by_xpath('/html/body/div/table[4]/tbody/tr/td/table/tbody/tr/td[2]/div/a[2]').click()
time.sleep(1)
alert = driver.switch_to.alert
alert.accept()
time.sleep(1)
alert.accept()

driver.quit()

# Get latest downloaded file
filename = max([download_path + "\\" + f for f in os.listdir(download_path)],key=os.path.getctime)
# Change filename to specified
shutil.move(filename, os.path.join(download_path, year + r"-" + month + r".pdf"))
time.sleep(1)
print("Finished successfully")
