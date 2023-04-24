from datetime import datetime
import time
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from gui_version import dictionaries

def signup(user_input):

    # setup variables
    start = False
    finish_search = False
    finish_entry = False

    # manipulation
    user_input['unlock_time'] = f"{user_input['timestart_h']}:{user_input['timestart_m']}:00"
    user_input['sport_form'] = user_input['sport'].replace(" ", "_")
    user_input['status_short'] = dictionaries.poss_status[user_input['status']]

    # search for course
    while not finish_search:
        curr_time = datetime.now().strftime("%H:%M:%S")  # getting time

        if not start:
            if curr_time == user_input['unlock_time']:  # start time
                start = True

            print(f'\rCurrent time: {curr_time}', end='')  # countdown kinda

        else:
            # page setup
            url = "https://server.sportzentrum.uni-kiel.de/angebote/aktueller_zeitraum/_" + user_input['sport_form'] + ".html"
            driver = webdriver.Chrome()
            driver.get(url)

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

                        if cols[1].accessible_name == user_input['detail'] and cols[2].accessible_name == user_input['day'] and cols[3].accessible_name == user_input['time'] and cols[6].accessible_name == user_input['guidance']:
                            print(f"Found course: {user_input['detail']}; {user_input['guidance']}; {user_input['day']}, {user_input['time']}. Opening signup...")
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
        if box.accessible_name == " " + user_input['sex']:
            box.click()
            break
    # first name
    driver.find_element(By.NAME, "vorname").send_keys(user_input['firstname'])
    # last name
    driver.find_element(By.NAME, "name").send_keys(user_input['lastname'])
    # street
    driver.find_element(By.NAME, "strasse").send_keys(user_input['street'])
    # city
    driver.find_element(By.NAME, "ort").send_keys(user_input['codecity'])
    # status
    driver.find_element(By.NAME, "statusorig").click()
    driver.find_element(By.XPATH, "//option[@value='" + user_input['status_short'] + "']").click()
    # matriculation
    try:
        driver.find_element(By.NAME, "matnr").send_keys(user_input['matnr'])
    except EC.NoSuchElementException:
        pass
    # email
    driver.find_element(By.NAME, "email").send_keys(user_input['email'])
    # checkboxes
    check_boxes1 = driver.find_elements(By.NAME, "freifeld1")
    check_boxes1[1].click()
    driver.find_element(By.NAME, "freifeld3").click()
    # iban
    driver.find_element(By.NAME, "iban").send_keys(user_input['iban'])
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
