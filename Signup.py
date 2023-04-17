import sys
import subprocess
import pkg_resources
from datetime import datetime
import time

required = {'selenium'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print("A module is missing. Installing...")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import Entry_data

# welcome
print('''
Welcome and thanks for trusting me! I tried to find errors so this should work well but I give no guarantees :p
In case you want to change data and/or restart the script you can stop it using Ctrl + C.

Please make sure you have added all the important information into the Entry_data.py file.
As soon as the sign up is unlocked a browser window will open. If the signup is not directly available, it will automatically refresh. There is a small waiting period in the process, where the website checks data. In the end you will be referred to the final page. Please check your input and do the final submit by hand.
Good luck! 
''')

# setup variables
start = False
finish_search = False
finish_entry = False

# search for course
while not finish_search:
    curr_time = datetime.now().strftime("%H:%M:%S")  # getting time

    if not start:
        if curr_time == Entry_data.unlock_time:  # start time
            start = True

        print(f'\rCurrent time: {curr_time}', end='')  # countdown kinda

    else:
        # page setup
        URL = "https://server.sportzentrum.uni-kiel.de/angebote/aktueller_zeitraum/_" + Entry_data.sport + ".html"
        driver = webdriver.Chrome()
        driver.get(URL)

        try:
            # are the submitting buttons available
            driver.find_element(By.TAG_NAME, "input")
        except selenium.common.exceptions.NoSuchElementException:
            # if not: refresh
            print("Not available. Refreshing...")
            driver.refresh()
            pass
        else:
            # if yes: find the correct course and click on the button
            tables = driver.find_elements(By.CLASS_NAME, "bs_angblock")

            for table in tables:
                tbl = table.find_elements(By.CLASS_NAME, "bs_kurse")
                body = tbl[0].find_element(By.TAG_NAME, "tbody")
                for row in body.find_elements(By.TAG_NAME, "tr"):
                    cols = row.find_elements(By.TAG_NAME, "td")

                    if cols[1].accessible_name == Entry_data.detail and cols[2].accessible_name == Entry_data.day and cols[3].accessible_name == Entry_data.time and cols[6].accessible_name == Entry_data.guidance:
                        print(f'Found course: {Entry_data.detail}; {Entry_data.guidance}; {Entry_data.day}, {Entry_data.time}. Opening signup...')
                        button = cols[-1]
                        button.click()
                        driver.switch_to.window(driver.window_handles[1])
                        finish_search = True
                        break
                else:
                    continue
                break

    time.sleep(1)

# fill in data
# sex
boxes_sex = driver.find_elements(By.NAME, "sex")
for box in boxes_sex:
    if box.accessible_name == " " + Entry_data.sex:
        box.click()
        break
# first name
driver.find_element(By.NAME, "vorname").send_keys(Entry_data.first_name)
# last name
driver.find_element(By.NAME, "name").send_keys(Entry_data.last_name)
# street
driver.find_element(By.NAME, "strasse").send_keys(Entry_data.street_and_nr)
# city
driver.find_element(By.NAME, "ort").send_keys(Entry_data.code_and_city)
# status
driver.find_element(By.NAME, "statusorig").click()
driver.find_element(By.XPATH, "//option[@value='" + Entry_data.status + "']").click()
# matriculation
driver.find_element(By.NAME, "matnr").send_keys(Entry_data.matriculation_nr)
# email
driver.find_element(By.NAME, "email").send_keys(Entry_data.email)
# checkboxes
check_boxes1 = driver.find_elements(By.NAME, "freifeld1")
check_boxes1[1].click()
driver.find_element(By.NAME, "freifeld3").click()
# iban
driver.find_element(By.NAME, "iban").send_keys(Entry_data.iban_nr)
# last box
driver.find_element(By.NAME, "tnbed").click()

# submit
wait = WebDriverWait(driver, timeout=10, poll_frequency=1)
wait.until(EC.element_to_be_clickable((By.ID, "bs_submit"))).click()

# final submit
alert = "alert('\nPlease check if everything is filled in and correct and do the final submit at the bottom of the page! Note: The browser will close automatically in 2 min. HAVE FUN! :)');"

try:
    driver.execute_script(alert)
except Exception:
    print('''
    
Something went wrong. No problem at this step.
Please check if everything is filled in and correct and do the final submit at the bottom of the page!Have fun! :)
    
Note: The page will close in 2 min automatically or you can stop the script.
    ''')

time.sleep(120)

# keeps site open
# while True:
#     pass
