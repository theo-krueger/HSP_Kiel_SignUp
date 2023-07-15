from PyQt5 import QtCore, QtWidgets
import sys
import dictionaries
from datetime import datetime
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from apscheduler.schedulers.qt import QtScheduler
from apscheduler.events import *
from random import randint


# creating a class that inherits the QDialog class
class Window(QtWidgets.QDialog):
    def __init__(self):
        super(Window, self).__init__()

        self.scheduler = Scheduler()
        self.signup = signup()

        self.setWindowTitle("Entry")
        self.setGeometry(100, 100, 300, 400)

        self.Entry_data = {}

        # creating a group box
        self.formGroupBox = QtWidgets.QGroupBox()
        # input boxes
        self.starttime_Label = QtWidgets.QLabel("Start time")
        self.starttime_TimeEdit = QtWidgets.QTimeEdit()
        self.sport_Label = QtWidgets.QLabel("Sport")
        self.sport_LineEdit = QtWidgets.QLineEdit()
        self.detail_Label = QtWidgets.QLabel("Detail")
        self.detail_LineEdit = QtWidgets.QLineEdit()
        self.day_Label = QtWidgets.QLabel("Day")
        self.day_LineEdit = QtWidgets.QLineEdit()
        self.time_Label = QtWidgets.QLabel("Time")
        self.time_TimeEdit = QtWidgets.QTimeEdit()
        self.guidance_Label = QtWidgets.QLabel("Guidance")
        self.guidance_LineEdit = QtWidgets.QLineEdit()
        self.gender_Label = QtWidgets.QLabel("Gender")
        self.gender_ComboBox = QtWidgets.QComboBox()
        self.gender_ComboBox.addItems([i for i in dictionaries.poss_gender.keys()])
        self.firstname_Label = QtWidgets.QLabel("First name")
        self.firstname_LineEdit = QtWidgets.QLineEdit()
        self.lastname_Label = QtWidgets.QLabel("Last name")
        self.lastname_LineEdit = QtWidgets.QLineEdit()
        self.street_Label = QtWidgets.QLabel("Street/Nr")
        self.street_LineEdit = QtWidgets.QLineEdit()
        self.codecity_Label = QtWidgets.QLabel("Postcode/city")
        self.codecity_LineEdit = QtWidgets.QLineEdit()
        self.status_Label = QtWidgets.QLabel("Status")
        self.status_ComboBox = QtWidgets.QComboBox()
        self.status_ComboBox.addItems([i for i in dictionaries.poss_status.keys()])
        self.status_ComboBox.currentTextChanged.connect(self.matr_or_phone)
        self.matnr_Label = QtWidgets.QLabel("Matriculation number")
        self.matnr_LineEdit = QtWidgets.QLineEdit()
        self.telephone_Label = QtWidgets.QLabel("Work telephone")
        self.telephone_LineEdit = QtWidgets.QLineEdit()
        self.email_Label = QtWidgets.QLabel("Email")
        self.email_LineEdit = QtWidgets.QLineEdit()
        self.iban_Label = QtWidgets.QLabel("IBAN")
        self.iban_LineEdit = QtWidgets.QLineEdit()

        self.boxes = [self.starttime_TimeEdit, self.sport_LineEdit, self.detail_LineEdit, self.day_LineEdit,
                      self.time_TimeEdit, self.guidance_LineEdit, self.gender_ComboBox, self.firstname_LineEdit,
                      self.lastname_LineEdit, self.street_LineEdit, self.codecity_LineEdit, self.status_ComboBox,
                      self.matnr_LineEdit, self.telephone_LineEdit, self.email_LineEdit, self.iban_LineEdit]
        for box in self.boxes:
            box.setMinimumWidth(300)
        self.labels = [self.starttime_Label, self.sport_Label, self.detail_Label, self.day_Label, self.time_Label,
                       self.guidance_Label, self.gender_Label, self.firstname_Label, self.lastname_Label,
                       self.street_Label, self.codecity_Label, self.status_Label, self.matnr_Label,
                       self.telephone_Label, self.email_Label, self.iban_Label]
        for label in self.labels:
            label.setMinimumWidth(150)

        self.joblist_button = QtWidgets.QPushButton("Print job list", self)
        self.joblist_button.clicked.connect(self.job_list)

        # calling the method that create the form
        self.create_form()

        # creating a dialog button for ok and cancel
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.accepted.connect(self.getInfo)
        self.buttonBox.rejected.connect(self.reject)

        # creating a vertical layout
        mainLayout = QtWidgets.QVBoxLayout()

        # adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.joblist_button)
        mainLayout.addWidget(self.buttonBox)

        # setting lay out
        self.setLayout(mainLayout)

    # get info method called when form is accepted
    def getInfo(self):
        self.Entry_data["start_time"] = self.starttime_TimeEdit.text() + ":00"
        self.Entry_data["sport"] = self.sport_LineEdit.text()
        self.Entry_data["detail"] = self.detail_LineEdit.text()
        self.Entry_data["day"] = self.day_LineEdit.text()
        if self.time_TimeEdit.text() == "00:00":
            self.Entry_data["time"] = ""
        else:
            self.Entry_data["time"] = self.time_TimeEdit.text()
        self.Entry_data["guidance"] = self.guidance_LineEdit.text()
        self.Entry_data["gender"] = dictionaries.poss_gender[self.gender_ComboBox.currentText()]
        self.Entry_data["firstname"] = self.firstname_LineEdit.text()
        self.Entry_data["lastname"] = self.lastname_LineEdit.text()
        self.Entry_data["streetnumber"] = self.street_LineEdit.text()
        self.Entry_data["codecity"] = self.codecity_LineEdit.text()
        self.Entry_data["status"] = dictionaries.poss_status[self.status_ComboBox.currentText()]
        self.Entry_data["matnr"] = self.matnr_LineEdit.text()
        self.Entry_data["telephone"] = self.telephone_LineEdit.text()
        self.Entry_data["email"] = self.email_LineEdit.text()
        self.Entry_data["iban"] = self.iban_LineEdit.text()

        self.job_add(data=self.Entry_data)

    def matr_or_phone(self):
        current_status = self.status_ComboBox.currentText()
        if current_status in dictionaries.show_matr:
            self.telephone_LineEdit.hide()
            self.telephone_Label.hide()
            self.matnr_LineEdit.show()
            self.matnr_Label.show()
        elif current_status in dictionaries.show_tel:
            self.matnr_LineEdit.hide()
            self.matnr_Label.hide()
            self.telephone_LineEdit.show()
            self.telephone_Label.show()
        else:
            self.matnr_LineEdit.hide()
            self.matnr_Label.hide()
            self.telephone_LineEdit.hide()
            self.telephone_Label.hide()

    # create form method
    def create_form(self):
        # creating a form layout
        layout = QtWidgets.QFormLayout()

        # adding rows
        layout.addRow(self.starttime_Label, self.starttime_TimeEdit)
        layout.addRow(QtWidgets.QLabel(" "))
        layout.addRow(self.sport_Label, self.sport_LineEdit)
        layout.addRow(self.detail_Label, self.detail_LineEdit)
        layout.addRow(self.day_Label, self.day_LineEdit)
        layout.addRow(self.time_Label, self.time_TimeEdit)
        layout.addRow(self.guidance_Label, self.guidance_LineEdit)
        layout.addRow(QtWidgets.QLabel(" "))
        layout.addRow(self.gender_Label, self.gender_ComboBox)
        layout.addRow(self.firstname_Label, self.firstname_LineEdit)
        layout.addRow(self.lastname_Label, self.lastname_LineEdit)
        layout.addRow(self.street_Label, self.street_LineEdit)
        layout.addRow(self.codecity_Label, self.codecity_LineEdit)
        layout.addRow(self.status_Label, self.status_ComboBox)
        layout.addRow(self.matnr_Label, self.matnr_LineEdit)
        layout.addRow(self.telephone_Label, self.telephone_LineEdit)
        layout.addRow(self.email_Label, self.email_LineEdit)
        layout.addRow(self.iban_Label, self.iban_LineEdit)

        # setting layout
        self.formGroupBox.setLayout(layout)

    def job_add(self, data):
        start_date = datetime.today()
        start_time_parts = data["start_time"].split(":")
        start_time = start_date.replace(hour=int(start_time_parts[0]),
                                        minute=int(start_time_parts[1]),
                                        second=int(start_time_parts[2]))

        id_ = data["sport"] + "_" + data["day"] + "_" + data["time"]
        existing_ids = [i.id for i in self.scheduler.scheduler.get_jobs()]
        if id_ in existing_ids:
            id_ = id_ + str(randint(0, 1000))

        self.scheduler.add_job(self.signup.main, start_time, id_, kwargs={"Entry_data": data})

    def job_list(self):
        message = "Jobs:"

        jobs = self.scheduler.scheduler.get_jobs()
        if not jobs:
            message = message + "\n\t" + "no jobs currently scheduled"
        for job in jobs:
            message = message + "\n\t" + f"ID: {job.id}; Next run: {job.next_run_time.strftime('%Y/%m/%d %H:%M')}"

        print(message)


class Scheduler(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self.scheduler = QtScheduler(timezone="Europe/Berlin")
        self.scheduler.add_listener(self.listener, EVENT_JOB_MISSED)
        self.scheduler.start()

    def add_job(self, func, start_time, id_, kwargs=None):
        self.scheduler.add_job(func, next_run_time=start_time, id=id_, kwargs=kwargs)
        print("Job submitted.")

    def shutdown(self):
        self.scheduler.shutdown()

    def listener(self, event):
        if event.code == EVENT_JOB_MISSED:
            print("Given event time was missed. Job canceled. Please check that the start time is in the future...")


class signup:
    def main(self, **kwargs):
        Entry_data = kwargs.get("Entry_data")

        def open_page():
            url = f"https://server.sportzentrum.uni-kiel.de/angebote/aktueller_zeitraum/_{Entry_data['sport']}.html"
            global driver
            driver = webdriver.Chrome()
            driver.get(url)

        def refresh_page():
            print("Not available. Refreshing...")
            driver.refresh()

        def find_course():
            try:
                driver.find_element(By.TAG_NAME, "input")
            except selenium.common.exceptions.NoSuchElementException:
                refresh_page()
                pass
            else:
                tables = driver.find_elements(By.CLASS_NAME, "bs_angblock")

                for table in tables:
                    tbl = table.find_elements(By.CLASS_NAME, "bs_kurse")
                    body = tbl[0].find_element(By.TAG_NAME, "tbody")
                    for row in body.find_elements(By.TAG_NAME, "tr"):
                        cols = row.find_elements(By.TAG_NAME, "td")

                        if cols[1].accessible_name == Entry_data["detail"] and \
                           cols[2].accessible_name == Entry_data["day"] and \
                           cols[3].accessible_name == Entry_data["time"] and \
                           cols[6].accessible_name == Entry_data["guidance"]:
                            print(
                                "Found course:",
                                Entry_data['sport'],
                                Entry_data['detail'],
                                Entry_data['guidance'],
                                Entry_data['day'],
                                Entry_data['time'],
                                "Opening signup...",
                                sep="\n\t"
                            )
                            button = cols[-1]
                            button.click()
                            driver.switch_to.window(driver.window_handles[1])
                            break
                    else:
                        continue
                    break

        def fill_in_data():
            boxes_gender = driver.find_elements(By.NAME, "sex")
            for box in boxes_gender:
                if box.accessible_name == " " + Entry_data["gender"]:
                    box.click()
                    break

            driver.find_element(By.NAME, "vorname").send_keys(Entry_data["firstname"])
            driver.find_element(By.NAME, "name").send_keys(Entry_data["lastname"])
            driver.find_element(By.NAME, "strasse").send_keys(Entry_data["streetnumber"])
            driver.find_element(By.NAME, "ort").send_keys(Entry_data["codecity"])

            driver.find_element(By.NAME, "statusorig").click()
            driver.find_element(By.XPATH, "//option[@value='" + Entry_data["status"] + "']").click()

            driver.find_element(By.NAME, "matnr").send_keys(Entry_data["matnr"])
            driver.find_element(By.NAME, "email").send_keys(Entry_data["email"])

            check_boxes1 = driver.find_elements(By.NAME, "freifeld1")
            check_boxes1[1].click()
            driver.find_element(By.NAME, "freifeld3").click()

            driver.find_element(By.NAME, "iban").send_keys(Entry_data["iban"])
            driver.find_element(By.NAME, "tnbed").click()

        def submit_form():
            wait = WebDriverWait(driver, timeout=10, poll_frequency=1)
            wait.until(EC.element_to_be_clickable((By.ID, "bs_submit"))).click()

        # Usage:
        open_page()
        find_course()
        fill_in_data()
        submit_form()


# main method
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    # start the app
    sys.exit(app.exec())
