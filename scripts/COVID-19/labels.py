# -*- coding: utf-8 -*-

def scatter_country(lang):
    if lang == "EL":
        return "ADMIN_GR"
    else:
        return "Country,Other"


def scatter_labels(lang):
    if lang == "EL":
        return {
            "Deaths/1M pop": "<b>Θάνατοι</b>/<br>1Μ",
            "Tests/ 1M pop": "Τεστ/ 1M πληθυσμού",
            "Tot Cases/1M pop": "Κρούσματα/ 1M πληθυσμού",
            "size": "",
            "text": "",
        }
    else:
        return {
            "Deaths/1M pop": "<b>Deaths</b>/<br>1Μ",
            "Tests/ 1M pop": "Tests/ 1M population",
            "Tot Cases/1M pop": "Cases/ 1M population",
            "size": "",
            "text": "",
        }


def scatter_title(lang):
    if lang == "EL":
        return "<b>Κρούσματα</b>, <b>Τεστ</b> και <b>Θάνατοι</b> ανά χώρα<br>"
    else:
        return "<b>Cases</b>, <b>Tests</b> and <b>Deaths</b> per country"


def scatter_xaxis_title(lang):
    if lang == "EL":
        return "<b>Τεστ</b>/1 εκατ. πληθυσμού"
    else:
        return "<b>Tests</b>/1M population"


def scatter_yaxis_title(lang):
    if lang == "EL":
        return "<b>Κρούσματα</b>/1 εκατ. πληθυσμού"
    else:
        return "<b>Cases</b>/1M population"


def line_button_all(lang):
    if lang == "EL":
        return "ΟΛΑ"
    else:
        return "ALL"


def line_button_deaths(lang):
    if lang == "EL":
        return "Θάνατοι"
    else:
        return "Deaths"


def line_button_intub(lang):
    if lang == "EL":
        return "Διασ/μένοι"
    else:
        return "Intubated"


def line_button_all_title(lang):
    if lang == "EL":
        return "<b>Θάνατοι</b> και <b>διασωληνωμένοι</b> ασθενείς στην Ελλάδα"
    else:
        return "<b>Deaths</b> and <b>intubated</b> patients in Greece"


def line_button_deaths_title(lang):
    if lang == "EL":
        return "<b>Θάνατοι</b>/ημέρα στην Ελλάδα"
    else:
        return "<b>Deaths</b>/day in Greece"


def line_button_intub_title(lang):
    if lang == "EL":
        return "<b>Διασωληνωμένοι</b> ασθενείς/ημέρα στην Ελλάδα"
    else:
        return "<b>Intubated</b> patients/day in Greece"


def line_trace_deaths(lang):
    if lang == "EL":
        return "θάνατοι"
    else:
        return "deaths"


def line_trace_intub(lang):
    if lang == "EL":
        return "διασωληνωμένοι"
    else:
        return "intubated"


def regions_facets_title(lang):
    if lang == "EL":
        return "Εξέλιξη <b>θανάτων</b> ανά <b>Περιφέρεια</b> στην Ελλάδα"
    else:
        return "Evolution of <b>deaths</b> by <b>district</b> in Greece"


def regions_facets_xaxis_note(lang):
    if lang == "EL":
        return "<i>Δεν περιλαμβάνονται θάνατοι με άγνωστο γεωγραφικό προσδιορισμό.</i>"
    else:
        return "<i>Deaths with unknown location are not included.</i>"


def regions_facets_labels(lang):
    if lang == "EL":
        return {
            "district": "Περιφέρεια",
            "Date": "Ημ/νία",
            "deaths": "Θάνατοι συνολικά",
        }
    else:
        return {
            "district": "District",
            "Date": "Date",
            "deaths": "Total Deaths",
        }


def choropleth_casesrate_title(lang):
    if lang == "EL":
        return "<br><b>Κρούσματα</b> αναλογικά με τα τεστ ανά χώρα<br>"
    else:
        return "<br>Ratio of <b>cases</b> in tests per country"


def choropleth_casesrate_annot(lang):
    if lang == "EL":
        return "Οι διαφορετικές πολιτικές των χωρών ως προς τα τεστ <br>μπορεί να οδηγούν σε υποεκτιμήσεις ή υπερεκτιμήσεις."
    else:
        return "Different policies of various countries on testing <br>might drive to underestimations or overestimations."


def choropleth_recoveredrate_title(lang):
    if lang == "EL":
        return "<br>Όσοι <b>ανάρρωσαν</b> ανά χώρα<br>"
    else:
        return "<br><b>Recovery</b> ratio per country"


def choropleth_recoveredrate_annot(lang):
    if lang == "EL":
        return "ανάρρωσαν/κρούσματα (%)<br>Οι διαφορετικές πολιτικές των χωρών ως προς την<br>καταγραφή των στοιχείων μπορεί να επηρεάζουν τα αποτελέσματα."
    else:
        return "recovered/cases (%)<br>Different policies of various countries on<br>record keeping might influence results."

    
def non_residents_line_title(lang):
    if lang == "EL":
        return "<b>Eισαγόμενα</b> κρούσματα στην Ελλάδα"
    else:
        return "<b>Ιmported cases</b> in Greece"

def non_residents_line_xaxis_note(lang):
    if lang == "EL":
        return "<i>Περιλαμβάνονται εισαγόμενα κρούσματα από 15 Ιουνίου και εφεξής</i>"
    else:
        return '<i>Imported cases from June 15 onwards are included.</i>'
    
def non_residents_line_yaxis_title(lang):
    if lang == 'EL':
        return 'Κυλιόμενος μέσος όρος 7 ημερών'
    else:
        return '7-day moving average'
    

def linesubplots_tests_cases_title(lang):
    if lang == "EL":
        return "Εξέλιξη <b>τεστ</b> και <b>κρουσμάτων</b> στην Ελλάδα"
    else:
        return "Evolution of <b>tests</b> and <b>cases</b> in Greece"
    
def linesubplots_tests_cases_subtitles(lang):
    if lang == 'EL':
        return '<b>Συνολικά τεστ</b>', '<b>Συνολικά κρούσματα</b>'
    else: 
        return '<b>Total tests</b>', '<b>Total cases</b>'
    
def linesubplots_tests_hovertemplate(lang):
    if lang == 'EL': 
        return 'Έως %{x}:<br>%{text}M τεστ'
    else:
        return 'Until %{x}:<br>%{text}M tests'
    
def linesubplots_cases_hovertemplate(lang):
    if lang == 'EL': 
        return 'Έως %{x}:<br>%{text}K κρούσματα'
    else:
        return 'Until %{x}:<br>%{text}K cases'
    
    
def schools_map_greece_title(lang):
    if lang == 'EL':
        return '<b>Σχολεία</b> σε <b>αναστολή</b> λειτουργίας στην Ελλάδα'
    else:
        return '<b>Schools suspended</b> in Greece'

def get_schools_oliki_name(lang):
    if lang == 'EL':
        return 'Ολική<br>αναστολή'
    else:
        return 'Schools<br>closed'
    
def get_schools_meriki_name(lang):
    if lang=='EL':
        return 'Μερική<br>αναστολή'
    else:
        return 'Partial<br>suspension'
    
def get_schools_reoper_name(lang):
    if lang == 'EL':
        return 'Επαναλειτουργία<br>σχολείου'
    else:
        return 'Schools<br>re-operation'
    
def get_schools_reoper_name2(lang):
    if lang == 'EL':
        return 'Επαναλειτουργία<br>τμημάτων/τάξεων'
    else:
        return 'Re-operation after<br>partial suspension'
    
def schools_map_athens_title(lang):
    if lang == 'EL':
        return '<b>Σχολεία</b> σε <b>αναστολή</b> λειτουργίας στην Αθήνα'
    else:
        return '<b>Schools suspended</b> in Athens'
        