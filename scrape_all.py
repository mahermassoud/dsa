from selenium import webdriver
import csv
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import collections

# Input file path, input file is plain text file where each line holds a single
# application number
INPUT_PATH = 'C:/Code/dsa-project-scraper/INPUT_PATH.csv'

# Output file is spreadsheet in form of a CSV
OUT_PATH = 'C:/Code/dsa-project-scraper/OUT_PATH.csv'

# JS IDs for:
# Application number input field on first page
APP_NUM_IN_ID = "ctl00_MainContent_txtAppNo"
# Drop down box to select region
REG_DROPDOWN = "ctl00_MainContent_drpdnOffice"
# Selection for sd from dropdown
SD_REG = '04-SAN DIEGO'


# Dictionary with column names as keys and javascript IDs as columns
# different dict for Application summary page
APP_SUMM = collections.OrderedDict()
APP_SUMM["Address"] = "ctl00_MainContent_lblAddress"
APP_SUMM["City"] = "ctl00_MainContent_lblCity"
#APP_SUMM["State"] = "" # NO STATE?
APP_SUMM["Zip"] = "ctl00_MainContent_lblZip"
APP_SUMM["App Num"] = "ctl00_MainContent_lblApplication" # TODO handle
APP_SUMM["Office ID"] = "ctl00_MainContent_lblOffice"
APP_SUMM["Project Name"] = "ctl00_MainContent_lblPname"
APP_SUMM["File Num"] = "ctl00_MainContent_lblFile"
APP_SUMM["PTN Num"] = "ctl00_MainContent_lblPTN"
APP_SUMM["Num incr"] = "ctl00_MainContent_lblInc"
APP_SUMM["Project Type"] = "ctl00_MainContent_lblProjectType"
APP_SUMM["Project Scope"] = "ctl00_MainContent_lblProjectScope" # TODO remove commas

PROJ_SCHED = collections.OrderedDict()
PROJ_SCHED["ACS"] = "ctl00_MainContent_lblACSplanR"

PROJ_CERT = collections.OrderedDict()
PROJ_CERT["Field Engineer"] = "ctl00_MainContent_lblFieldEnf"
PROJ_CERT["Void Date"] = "ctl00_MainContent_lblVoidCanceledDate"
PROJ_CERT["90 Day Letter Date"] = "ctl00_MainContent_lbl90DayLetter"
PROJ_CERT["60 Day Letter Date"] = "ctl00_MainContent_lbl60DayLetter"
PROJ_CERT["Last Cert Date"] = "ctl00_MainContent_lblCloseDate"
PROJ_CERT["Last Cert Letter Type"] = "ctl00_MainContent_lblCloseLetType"
#<input name="ctl00$ContentPlaceHolder1$txt60DayLetter" type="text" readonly="readonly" id="ctl00_ContentPlaceHolder1_txt60DayLetter" style="width:70px;">

PAGE_DICTS = [APP_SUMM, PROJ_SCHED, PROJ_CERT]
############################# End constants ####################################
################################################################################
############## Function defs and instance variables ############################

driver = webdriver.Chrome()

# Given application number and office number, sets driver to its corresponding
# Office ID should be in format 01, 02, 03, 04, or HQ, read as string not number
# app summary page
def enterAppNum(app_num, office_id):
    driver.get("https://www.apps2.dgs.ca.gov/dsa/tracker/Appno.aspx")
    dropdown_field = Select(driver.find_element_by_id(REG_DROPDOWN))
    dropdown_field.select_by_value(office_id)
    app_in_field = driver.find_element_by_id(APP_NUM_IN_ID)

    app_in_field.send_keys(app_num)
    app_in_field.send_keys(Keys.ENTER)

# Takes driver to project schedule page
# PREREQ: driver is on application summary page, has not timed out
def goToProjSchedule():
    link = driver.find_element_by_link_text('Project Schedule')
    link.click()

# Takes driver to project certification page
# PREREQ: driver is on application summary page, has not timed out
def goToProjCert():
    link = driver.find_element_by_link_text('Project Certification')
    link.click()

# Takes driver to change orders page
# PREREQ: driver is on application summary page, has not timed out
def goToChangeOrders():
    link = driver.find_element_by_link_text('Change Orders')
    link.click()

# takes a column header name and returns the corresponding value
# PREREQ: driver is set to page that holds element we are looking for
def getElem(col_name):

    if(col_name == "State"):
        return "CA"

    # Get corresponding javascript ID
    for page_dict in PAGE_DICTS:
        if col_name in page_dict:
            id = page_dict[col_name]

    info = driver.find_element_by_id(id).text
    # Handles case where HTML is different (project schedule page)
    if info == "":
        info = driver.find_element_by_id(id).get_attribute("value")
    return info

################################################################################
##################### Execution code ###########################################

# Get list of app numbers
with open(INPUT_PATH) as infile:
    app_nums = infile.read().splitlines()

table = pd.read_csv(INPUT_PATH, dtype=str)
#file_nums = list(infile[:,0])
#app_nums = list(infile[:,0])

rows = []
# For each app number
#for app in app_nums:
for index, row in table.iterrows():

    office_id = str(row[0])
    app = str(row[1])

    curr_row = []

    # visit its summary page
    enterAppNum(app, office_id)
    # Get all the info we want from app summary page
    for key in PAGE_DICTS[0]:
        curr_row.append(getElem(key))

    # Get info from proj schedule page
    goToProjSchedule()
    for key in PAGE_DICTS[1]:
        curr_row.append(getElem(key))

    # Get info from proj cert page
    driver.back()
    goToProjCert()
    for key in PAGE_DICTS[2]:
        curr_row.append(getElem(key))

    rows.append(curr_row)



# Create output file
with open(OUT_PATH, 'w', newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerow(list(APP_SUMM.keys()) + list(PROJ_SCHED.keys()) + list(PROJ_CERT.keys()))

    for row in rows:
        writer.writerow(row)
driver.close()