def setup():
    required = {'selenium', 'schwifty'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed

    if missing:
        print(f"Required modules missing: {missing}")
        print("Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)


try:
    import sys
    import subprocess
    import pkg_resources
    import tkinter as tk
    from tkinter import ttk
    import time
    from selenium import webdriver
    import selenium.common.exceptions
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from schwifty import IBAN
    import re

    from gui_version import dictionaries
except ImportError:
    setup()
    import sys
    import subprocess
    import pkg_resources
    import tkinter as tk
    from tkinter import ttk
    import time
    from selenium import webdriver
    import selenium.common.exceptions
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from schwifty import IBAN, exceptions
    import re

    from gui_version import dictionaries


class Windows(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        container = ttk.Frame(self, height=400, width=600)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.app_data = {
            "timestart_h": tk.StringVar(),
            "timestart_m": tk.StringVar(),
            "sport": tk.StringVar(),
            "detail": tk.StringVar(),
            "day": tk.StringVar(),
            "time": tk.StringVar(),
            "guidance": tk.StringVar(),
            "gender": tk.StringVar(),
            "firstname": tk.StringVar(),
            "lastname": tk.StringVar(),
            "street": tk.StringVar(),
            "codecity": tk.StringVar(),
            "status": tk.StringVar(),
            "matnr": tk.StringVar(),
            "telephone": tk.StringVar(),
            "email": tk.StringVar(),
            "iban": tk.StringVar()
        }

        self.frames = {}
        for F in (StartPage, EntryPage, RunningPage):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.title("HSP SignUp")

        self.show_frame(StartPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_settings()

        info_text_text = """
        Welcome and thanks for trusting me! I tried to find errors so this should work well but I give no
        guarantees :p \n
        In case you want to change data and/or restart the script you can stop it by closing this window. \n 
        Please enter your data on the next page and click on submit after checking it. This window will stay open
        until the script has finished running, please don't close it. When the website unlocks, a browser window
        will open and insert all your data. If you have filled in all of the fields, it should lead to to the last
        page where you can check the data again and will have to click on the final submit. \n
        Good luck!
        """

        self.info_text = ttk.Label(
            self,
            text=info_text_text,
            justify="left"
        )

        self.enter_data_button = tk.Button(
            self,
            text="Enter your data",
            command=lambda: controller.show_frame(EntryPage)
        )

        self.info_text.grid(row=1, column=0, columnspan=4, sticky='nsew', padx=(50, 50))
        self.info_text.bind('<Configure>', lambda e: self.info_text.config(wraplength=self.info_text.winfo_width()))

        self.enter_data_button.grid(row=4, column=0, pady=50)

    def grid_settings(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)


class EntryPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_settings()

        self.controller.app_data_dic = {}

        # labels
        self.timestart_lbl = ttk.Label(self, text='Start time [hh:mm]')
        self.timestart_sep = ttk.Label(self, text=":")
        self.sport_lbl = ttk.Label(self, text='Sport type')
        self.detail_lbl = ttk.Label(self, text='Detail')
        self.day_lbl = ttk.Label(self, text='Day')
        self.time_lbl = ttk.Label(self, text='Time')
        self.guidance_lbl = ttk.Label(self, text='Guidance')
        self.gender_lbl = ttk.Label(self, text='Gender')
        self.firstname_lbl = ttk.Label(self, text='First name')
        self.lastname_lbl = ttk.Label(self, text='Last name')
        self.street_lbl = ttk.Label(self, text='Street and number')
        self.codecity_lbl = ttk.Label(self, text='Code and city name')
        self.status_lbl = ttk.Label(self, text='Status')
        self.matnr_lbl = ttk.Label(self, text='Matriculation number')
        self.telephone_lbl = ttk.Label(self, text='Work telephone number')
        self.email_lbl = ttk.Label(self, text='Email')
        self.iban_lbl = ttk.Label(self, text='IBAN')

        # entry boxes
        self.timestart_h_box = ttk.Entry(self, textvariable=self.controller.app_data["timestart_h"])
        self.timestart_m_box = ttk.Entry(self, textvariable=self.controller.app_data["timestart_m"])

        self.sport_box = ttk.Entry(self, textvariable=self.controller.app_data["sport"])
        self.detail_box = ttk.Entry(self, textvariable=self.controller.app_data["detail"])
        self.day_box = ttk.Entry(self, textvariable=self.controller.app_data["day"])
        self.time_box = ttk.Entry(self, textvariable=self.controller.app_data["time"])
        self.guidance_box = ttk.Entry(self, textvariable=self.controller.app_data["guidance"])

        gender_list = [i for i in dictionaries.poss_gender.keys()]
        self.controller.app_data["gender"].set("Gender")
        self.gender_box = tk.OptionMenu(self, self.controller.app_data["gender"], *gender_list)

        self.firstname_box = ttk.Entry(self, textvariable=self.controller.app_data["firstname"])
        self.lastname_box = ttk.Entry(self, textvariable=self.controller.app_data["lastname"])
        self.street_box = ttk.Entry(self, textvariable=self.controller.app_data["street"])
        self.codecity_box = ttk.Entry(self, textvariable=self.controller.app_data["codecity"])

        status_list = [i for i in dictionaries.poss_status.keys()]
        self.controller.app_data["status"].set("Status")
        self.status_box = tk.OptionMenu(self, self.controller.app_data["status"], *status_list)

        self.matnr_box = ttk.Entry(self, textvariable=self.controller.app_data["matnr"])
        self.telephone_box = ttk.Entry(self, textvariable=self.controller.app_data["telephone"])
        self.email_box = ttk.Entry(self, textvariable=self.controller.app_data["email"])
        self.iban_box = ttk.Entry(self, textvariable=self.controller.app_data["iban"])

        self.continue_button = ttk.Button(
            self,
            text='Continue',
            command=lambda: [self.controller.update(), self.check_entries(controller=controller)]
        )

        # arrange
        self.full_width = 3
        self.full_orientation = 'NSEW'
        self.col_lbl = 1
        self.col_box = 2
        self.row_start = 2

        self.timestart_lbl.grid(row=self.row_start+1, column=self.col_lbl, sticky='W', pady=(20, 0))
        self.sport_lbl.grid(row=self.row_start+2, column=self.col_lbl, sticky='W')
        self.detail_lbl.grid(row=self.row_start+4, column=self.col_lbl, sticky='W', pady=(15, 0))
        self.day_lbl.grid(row=self.row_start+5, column=self.col_lbl, sticky='W')
        self.time_lbl.grid(row=self.row_start+6, column=self.col_lbl, sticky='W')
        self.guidance_lbl.grid(row=self.row_start+7, column=self.col_lbl, sticky='W')
        self.gender_lbl.grid(row=self.row_start+9, column=self.col_lbl, sticky='W', pady=(15, 0))
        self.firstname_lbl.grid(row=self.row_start+10, column=self.col_lbl, sticky='W')
        self.lastname_lbl.grid(row=self.row_start+11, column=self.col_lbl, sticky='W')
        self.street_lbl.grid(row=self.row_start+12, column=self.col_lbl, sticky='W')
        self.codecity_lbl.grid(row=self.row_start+13, column=self.col_lbl, sticky='W')
        self.status_lbl.grid(row=self.row_start+14, column=self.col_lbl, sticky='W')
        self.email_lbl.grid(row=self.row_start+16, column=self.col_lbl, sticky='W')
        self.iban_lbl.grid(row=self.row_start+17, column=self.col_lbl, sticky='W')

        self.timestart_h_box.grid(row=self.row_start+1, column=self.col_box, sticky=self.full_orientation, pady=(20, 0))
        self.timestart_sep.grid(row=self.row_start+1, column=self.col_box+1, pady=(20, 0))
        self.timestart_m_box.grid(row=self.row_start+1, column=self.col_box+2, sticky=self.full_orientation, pady=(20, 0))
        self.sport_box.grid(row=self.row_start+2, column=self.col_box, columnspan=self.full_width, sticky=self.full_orientation)
        self.detail_box.grid(row=self.row_start+4, column=self.col_box, columnspan=self.full_width, sticky=self.full_orientation, pady=(15,0))
        self.day_box.grid(row=self.row_start + 5, column=self.col_box, columnspan=self.full_width, sticky=self.full_orientation)
        self.time_box.grid(row=self.row_start + 6, column=self.col_box, columnspan=self.full_width, sticky=self.full_orientation)
        self.guidance_box.grid(row=self.row_start + 7, column=self.col_box, columnspan=self.full_width, sticky=self.full_orientation)
        self.gender_box.grid(row=self.row_start+9, column=self.col_box, columnspan=self.full_width, sticky=self.full_orientation, pady=(15, 0))
        self.firstname_box.grid(row=self.row_start+10, column=self.col_box, columnspan=self.full_width, sticky=self.full_orientation)
        self.lastname_box.grid(row=self.row_start+11, column=self.col_box, columnspan=self.full_width, sticky=self.full_orientation)
        self.street_box.grid(row=self.row_start+12, column=self.col_box, columnspan=self.full_width, sticky=self.full_orientation)
        self.codecity_box.grid(row=self.row_start+13, column=self.col_box, columnspan=self.full_width, sticky=self.full_orientation)
        self.status_box.grid(row=self.row_start+14, column=self.col_box, columnspan=self.full_width, sticky=self.full_orientation)
        self.email_box.grid(row=self.row_start+16, column=self.col_box, columnspan=self.full_width, sticky=self.full_orientation)
        self.iban_box.grid(row=self.row_start+17, column=self.col_box, columnspan=self.full_width, sticky=self.full_orientation)

        def matr_or_phone(*args):
            mattel_wid = [self.matnr_lbl, self.matnr_box, self.telephone_lbl, self.telephone_box]
            for w in mattel_wid:
                w.grid_remove()
            if self.controller.app_data["status"].get() in dictionaries.show_matr:
                self.matnr_lbl.grid(row=self.row_start+15, column=self.col_lbl, sticky='W')
                self.matnr_box.grid(row=self.row_start+15, column=self.col_box, columnspan=self.full_width,
                                    sticky=self.full_orientation)
            elif self.controller.app_data["status"].get() in dictionaries.show_tel:
                self.telephone_lbl.grid(row=self.row_start+15, column=self.col_lbl, sticky='W')
                self.telephone_box.grid(row=self.row_start+15, column=self.col_box, columnspan=self.full_width,
                                        sticky=self.full_orientation)

        self.controller.app_data["status"].trace("w", matr_or_phone)

        self.continue_button.grid(row=self.row_start+21, column=3, pady=20)

    def grid_settings(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(6, weight=1)
        self.grid_columnconfigure(8, weight=1)
        self.grid_columnconfigure(9, weight=1)
        self.grid_columnconfigure(10, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_rowconfigure(9, weight=1)
        self.grid_rowconfigure(10, weight=1)
        self.grid_rowconfigure(11, weight=1)
        self.grid_rowconfigure(12, weight=1)
        self.grid_rowconfigure(13, weight=1)
        self.grid_rowconfigure(14, weight=1)
        self.grid_rowconfigure(15, weight=1)
        self.grid_rowconfigure(16, weight=1)
        self.grid_rowconfigure(17, weight=1)
        self.grid_rowconfigure(18, weight=1)
        self.grid_rowconfigure(19, weight=1)
        self.grid_rowconfigure(20, weight=1)

    def check_entries(self, controller):
        # check entries
        check = True
        # time
        if not len(self.controller.app_data["timestart_h"].get()) == 2 or not len(self.controller.app_data["timestart_m"].get()) == 2:
            print("Time format invalid, please notice that both the hours and minutes need two digits each...")
            check = False
        # code city
        code, city = self.controller.app_data["codecity"].get().split(" ")
        if not len(code) == 5:
            print("Post code invalid, please check...")
            check = False
        # IBAN
        try:
            IBAN(self.controller.app_data["iban"].get(), validate_bban=True)
        except exceptions:
            print("IBAN invalid, please check...")
            check = False
        # email
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", self.controller.app_data["email"].get()):
            print("Email invalid, please check...")
            check = False

        if check:
            controller.show_frame(RunningPage)

        # print entries
        for entry in self.controller.app_data:
            try:
                print(f"{entry}: {self.controller.app_data[entry].get()}")
            except AttributeError:
                print(f"{entry}: {self.controller.app_data[entry]}")


class RunningPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.grid_settings()

        self.time_lbl = ttk.Label(self,
                                  font=("calibri", 30, "bold")
                                  )
        self.start_button = ttk.Button(
            self,
            text="Start signin",
            command=self.signup
        )
        self.back_button = ttk.Button(
            self,
            text="Back to Entry",
            command=lambda: controller.show_frame(EntryPage)
        )
        self.stop_button = ttk.Button(
            self,
            text="Close",
            command=self.controller.destroy
        )

        self.time_lbl.grid(row=2, column=2, padx=(50, 50))
        self.start_button.grid(row=3, column=2,)
        self.back_button.grid(row=4, column=1)
        self.stop_button.grid(row=4, column=3)

    def grid_settings(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

    def get_time(self):
        time_str = time.strftime('%H:%M:%S')
        self.time_lbl.config(text=time_str)
        self.time_lbl.after(1000, self.get_time)
        self.controller.update()

        return time_str

    def add_entries(self):
        self.controller.app_data['unlock_time'] = f"{self.controller.app_data['timestart_h'].get()}:{self.controller.app_data['timestart_m'].get()}:00"
        self.controller.app_data['sport_form'] = self.controller.app_data['sport'].get().replace(" ", "_")
        self.controller.app_data['status_code'] = dictionaries.poss_status[self.controller.app_data['status'].get()]
        self.controller.app_data['gender_code'] = dictionaries.poss_gender[self.controller.app_data['gender'].get()]

    def signup(self):
        self.add_entries()

        # setup variables
        start = False
        finish_search = False

        # search for course
        while not finish_search:
            curr_time = self.get_time()

            if not start:
                if curr_time == self.controller.app_data['unlock_time']:  # start time
                    start = True

                print(f'\rCurrent time: {curr_time}', end='')  # countdown kinda

            else:
                print(f"\nStarting...")
                # page setup
                url = "https://server.sportzentrum.uni-kiel.de/angebote/aktueller_zeitraum/_" + self.controller.app_data['sport_form'] + ".html"
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

                            if cols[1].accessible_name == self.controller.app_data['detail'].get() \
                                    and cols[2].accessible_name == self.controller.app_data['day'].get() \
                                    and cols[3].accessible_name == self.controller.app_data['time'].get() \
                                    and cols[6].accessible_name == self.controller.app_data['guidance'].get():
                                print(f"Found course: {self.controller.app_data['detail'].get()}; {self.controller.app_data['guidance'].get()}; {self.controller.app_data['day'].get()}, {self.controller.app_data['time'].get()}. Opening signup...")
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
        # gender
        boxes_gender = driver.find_elements(By.NAME, "sex")
        for box in boxes_gender:
            if box.accessible_name == " " + self.controller.app_data['gender_code']:
                box.click()
                break
        # first name
        driver.find_element(By.NAME, "vorname").send_keys(self.controller.app_data['firstname'].get())
        # last name
        driver.find_element(By.NAME, "name").send_keys(self.controller.app_data['lastname'].get())
        # street
        driver.find_element(By.NAME, "strasse").send_keys(self.controller.app_data['street'].get())
        # city
        driver.find_element(By.NAME, "ort").send_keys(self.controller.app_data['codecity'].get())
        # status
        driver.find_element(By.NAME, "statusorig").click()
        driver.find_element(By.XPATH, "//option[@value='" + self.controller.app_data['status_code'] + "']").click()
        # matriculation
        try:
            driver.find_element(By.NAME, "matnr").send_keys(self.controller.app_data['matnr'].get())
        except EC.NoSuchElementException:
            pass
        try:
            driver.find_element(By.NAME, "mitnr").send_keys(self.controller.app_data['telephone'].get())
        except EC.NoSuchElementException:
            pass
        # email
        driver.find_element(By.NAME, "email").send_keys(self.controller.app_data['email'].get())
        # checkboxes
        check_boxes1 = driver.find_elements(By.NAME, "freifeld1")
        check_boxes1[1].click()
        driver.find_element(By.NAME, "freifeld3").click()
        # iban
        driver.find_element(By.NAME, "iban").send_keys(self.controller.app_data['iban'].get())
        # last box
        driver.find_element(By.NAME, "tnbed").click()

        # submit
        wait = WebDriverWait(driver, timeout=10, poll_frequency=1)
        wait.until(EC.element_to_be_clickable((By.ID, "bs_submit"))).click()

        # final submit
        print('''

        Something went wrong. No problem at this step.
        Please check if everything is filled in and correct and do the final submit at the bottom of the page!Have fun! :)

        Note: The page will close in 2 min automatically or you can stop the script.
        ''')

        time.sleep(120)


if __name__ == "__main__":

    app = Windows()
    app.mainloop()
