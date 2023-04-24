import tkinter as tk

from gui_version import dictionaries


class Windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.frames = None
        self.configure_gui()

        self.show_frame(StartPage)

    def configure_gui(self):
        container = tk.Frame(self, height=400, width=600)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, EntryPage):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.title("HSP SignUp")

    def show_frame(self, page):
        frame = self.frames[page]
        # raises the current frame to the top
        frame.tkraise()

    def close(self):
        self.destroy()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        enter_data_button = tk.Button(
            self,
            text="Enter your data",
            command=lambda: controller.show_frame(EntryPage)
        )

        enter_data_button.place(relx=0.5, rely=1, anchor='s')


class EntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # labels
        self.empty1_lbl = tk.Label(self, text=' ', height=1)
        self.empty2_lbl = tk.Label(self, text=' ', height=1)
        self.timestart_lbl = tk.Label(self, text='Start time [hh:mm]')
        self.timestart_sep = tk.Label(self, text=":")
        self.sport_lbl = tk.Label(self, text='Sport type')
        self.detail_lbl = tk.Label(self, text='Detail')
        self.day_lbl = tk.Label(self, text='Day')
        self.time_lbl = tk.Label(self, text='Time')
        self.guidance_lbl = tk.Label(self, text='Guidance')
        self.sex_lbl = tk.Label(self, text='Sex')
        self.firstname_lbl = tk.Label(self, text='First name')
        self.lastname_lbl = tk.Label(self, text='Last name')
        self.street_lbl = tk.Label(self, text='Street and number')
        self.codecity_lbl = tk.Label(self, text='Code and city name')
        self.status_lbl = tk.Label(self, text='Status')
        self.matnr_lbl = tk.Label(self, text='Matriculation number')
        self.telephone_lbl = tk.Label(self, text='Work telephone number')
        self.email_lbl = tk.Label(self, text='Email')
        self.iban_lbl = tk.Label(self, text='IBAN')
        self.empty3_lbl = tk.Label(self, text=' ', height=2)

        # entry boxes
        self.timestart_h_box = tk.Entry(self)
        self.timestart_m_box = tk.Entry(self)
        
        self.sport_box = tk.Entry(self)
        self.detail_box = tk.Entry(self)
        self.day_box = tk.Entry(self)
        self.time_box = tk.Entry(self)
        self.guidance_box = tk.Entry(self)
        
        sex_list = [i for i in dictionaries.poss_sex.keys()]
        sex_var = tk.StringVar()
        sex_var.set(sex_list[0])
        self.sex_box = tk.OptionMenu(self, sex_var, *sex_list)

        self.firstname_box = tk.Entry(self)
        self.lastname_box = tk.Entry(self)
        self.street_box = tk.Entry(self)
        self.codecity_box = tk.Entry(self)
        
        status_list = [i for i in dictionaries.poss_status.keys()]
        status_var = tk.StringVar()
        status_var.set(status_list[0])
        self.status_box = tk.OptionMenu(self, status_var, *status_list)
        
        self.matnr_box = tk.Entry(self)
        self.telephone_box = tk.Entry(self)
        self.email_box = tk.Entry(self)
        self.iban_box = tk.Entry(self)

        self.entry_list = [self.timestart_h_box, self.timestart_m_box, self.sport_box, self.detail_box, self.day_box,
                           self.time_box, self.guidance_box, sex_var, self.firstname_box, self.lastname_box,
                           self.street_box, self.codecity_box, status_var, self.matnr_box, self.telephone_box,
                           self.email_box, self.iban_box]

        submit = tk.Button(
            self,
            text='Submit',
            command=self.collect_entries
        )
        
        # arrange
        full_width = 3
        full_orientation = 'NSEW'
        col_lbl = 0
        col_box = 1
        row_start = 0

        self.timestart_lbl.grid(row=row_start+1, column=col_lbl, sticky='W')
        self.sport_lbl.grid(row=row_start+2, column=col_lbl, sticky='W')
        self.empty1_lbl.grid(row=row_start + 3, column=col_lbl)
        self.detail_lbl.grid(row=row_start+4, column=col_lbl, sticky='W')
        self.day_lbl.grid(row=row_start+5, column=col_lbl, sticky='W')
        self.time_lbl.grid(row=row_start+6, column=col_lbl, sticky='W')
        self.guidance_lbl.grid(row=row_start+7, column=col_lbl, sticky='W')
        self.empty2_lbl.grid(row=row_start+8, column=col_lbl)
        self.sex_lbl.grid(row=row_start+9, column=col_lbl, sticky='W')
        self.firstname_lbl.grid(row=row_start+10, column=col_lbl, sticky='W')
        self.lastname_lbl.grid(row=row_start+11, column=col_lbl, sticky='W')
        self.street_lbl.grid(row=row_start+12, column=col_lbl, sticky='W')
        self.codecity_lbl.grid(row=row_start+13, column=col_lbl, sticky='W')
        self.status_lbl.grid(row=row_start+14, column=col_lbl, sticky='W')
        self.email_lbl.grid(row=row_start+16, column=col_lbl, sticky='W')
        self.iban_lbl.grid(row=row_start+17, column=col_lbl, sticky='W')
        self.empty3_lbl.grid(row=row_start+18, column=col_lbl, sticky='W')

        self.timestart_h_box.grid(row=row_start+1, column=col_box)
        self.timestart_sep.grid(row=row_start+1, column=col_box+1)
        self.timestart_m_box.grid(row=row_start+1, column=col_box+2)
        self.sport_box.grid(row=row_start+2, column=col_box, columnspan=full_width, sticky=full_orientation)
        self.detail_box.grid(row=row_start+4, column=col_box, columnspan=full_width, sticky=full_orientation)
        self.day_box.grid(row=row_start + 5, column=col_box, columnspan=full_width, sticky=full_orientation)
        self.time_box.grid(row=row_start + 6, column=col_box, columnspan=full_width, sticky=full_orientation)
        self.guidance_box.grid(row=row_start + 7, column=col_box, columnspan=full_width, sticky=full_orientation)
        self.sex_box.grid(row=row_start+9, column=col_box, columnspan=full_width, sticky=full_orientation)
        self.firstname_box.grid(row=row_start+10, column=col_box, columnspan=full_width, sticky=full_orientation)
        self.lastname_box.grid(row=row_start+11, column=col_box, columnspan=full_width, sticky=full_orientation)
        self.street_box.grid(row=row_start+12, column=col_box, columnspan=full_width, sticky=full_orientation)
        self.codecity_box.grid(row=row_start+13, column=col_box, columnspan=full_width, sticky=full_orientation)
        self.status_box.grid(row=row_start+14, column=col_box, columnspan=full_width, sticky=full_orientation)
        self.email_box.grid(row=row_start+16, column=col_box, columnspan=full_width, sticky=full_orientation)
        self.iban_box.grid(row=row_start+17, column=col_box, columnspan=full_width, sticky=full_orientation)

        def matr_or_phone(*args):
            show_matr = ["StudentIn der UNI Kiel", "StudentIn der FH", "StudentIn der Muthesius-HS",
                         "StudentIn einer anderen HS aus Schleswig-Holstein", "Beschäftigte/r des UKSH"]
            show_tel = ["Beschäftigte/r der UNI Kiel", "Beschäftigte/r der FH", "Beschäftigte/r IPN",
                        "Beschäftigte/r Geomar", "Beschäftigte/r der Muthesius-HS"]
            mattel_wid = [self.matnr_lbl, self.matnr_box, self.telephone_lbl, self.telephone_box]
            for w in mattel_wid:
                w.grid_remove()
            if status_var.get() in show_matr:
                self.matnr_lbl.grid(row=row_start+15, column=col_lbl, sticky='W')
                self.matnr_box.grid(row=row_start+15, column=1, columnspan=full_width, sticky=full_orientation)
            elif status_var.get() in show_tel:
                self.telephone_lbl.grid(row=row_start+15, column=col_lbl, sticky='W')
                self.telephone_box.grid(row=row_start+15, column=col_box, columnspan=full_width,
                                        sticky=full_orientation)

        status_var.trace("w", matr_or_phone)

        submit.place(relx=0.5, rely=1, anchor='s')

    def collect_entries(self):
        global user_input_dic
        user_input_dic = {}
        for index, entry in enumerate(self.entry_list):
            user_input_dic[dictionaries.entry_data[index]] = entry.get()
        self.destroy()

