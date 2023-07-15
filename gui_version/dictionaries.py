entry_data = [
    "start_time",
    "sport",
    "detail",
    "day",
    "time",
    "guidance",
    "gender",
    "firstname",
    "lastname",
    "street",
    "codecity",
    "status",
    "matnr",
    "telephone",
    "email",
    "iban"
]

poss_gender = {
    "prefer not to say": "keine Angabe",
    "female": "weiblich",
    "male": "männlich",
    "diverse": "divers",
}

poss_status = {
    "Student at UNI Kiel": "S-UKL",
    "Student at FH": "S-FHK",
    "Student at VFH": "S-VFH",
    "Student at WAK": "S-WAK",
    "Student at Muthesius-HS": "S-MHS",
    "Student at another HS in Schleswig-Holstein": "S-aHSH",
    "Working at UNI Kiel": "B-UKL",
    "Working at IPN": "B-IPN",
    "Working at UKSH": "B-UKSH",
    "Working at Muthesius-HS": "B-MHS",
    "Working at Geomar": "B-Geo",
    "Extern discounted": "Ext e",
    "Extern": "Extern",
    "Member of 'Alumni und Freunde der CAU e.V.'": "Alumni"
}

show_matr = [
    "Student at UNI Kiel",
    "Student at FH",
    "Student at Muthesius-HS",
    "Student at another HS in Schleswig-Holstein",
    "Working at UKSH"
]

show_tel = [
    "Working at UNI Kiel",
    "Working at IPN",
    "Working at Muthesius-HS",
    "Working at Geomar",
]