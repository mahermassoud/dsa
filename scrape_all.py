from selenium import webdriver
import csv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import collections

# Input file path, input file is plain text file where each line holds a single
# application number
INPUT_PATH = '/Users/massoudmaher/Desktop/app_nums_small.csv'

# Output file is spreadsheet in form of a CSV
OUT_PATH = '/Users/massoudmaher/Desktop/projs.csv'

# JS IDs for:
# Application number input field on first page
APP_NUM_IN_ID = "ctl00_ContentPlaceHolder1_txtAppNo"
# Drop down box to select region
REG_DROPDOWN = "ctl00_ContentPlaceHolder1_drpdnOffice"
# Selection for sd from dropdown
SD_REG = '04-SAN DIEGO'


# Dictionary with column names as keys and javascript IDs as columns
# different dict for each page
COL_HEADERS = collections.OrderedDict()
COL_HEADERS["Address"] = "ctl00_ContentPlaceHolder1_lblAddress"
COL_HEADERS["City"] = "ctl00_ContentPlaceHolder1_lblCity"
COL_HEADERS["State"] = "" # TODO auto fill CA
COL_HEADERS["Zip"] = "ctl00_ContentPlaceHolder1_lblZip"
COL_HEADERS["App num"] = "ctl00_ContentPlaceHolder1_lblApplication" # TODO handle
COL_HEADERS["Project Name"] = "ctl00_ContentPlaceHolder1_lblPname"
COL_HEADERS["Office ID"] = "ctl00_ContentPlaceHolder1_lblOffice"
COL_HEADERS["File Num"] = "ctl00_ContentPlaceHolder1_lblFile"

COL_HEADERS["Project Scope"] = "ctl00_ContentPlaceHolder1_lblProjectScope" # TODO remove commas
############################# End constants ####################################
################################################################################
############## Function defs and instance variables ############################

driver = webdriver.Chrome()

# Gets application number anad sets driver to its corresponding
# app summary page
def enterAppNum(app_num):
    driver.get("https://www.apps2.dgs.ca.gov/dsa/tracker/Appno.aspx")
    dropdown_field = Select(driver.find_element_by_id(REG_DROPDOWN))
    dropdown_field.select_by_visible_text(SD_REG)
    app_in_field = driver.find_element_by_id(APP_NUM_IN_ID)

    app_in_field.send_keys(app_num)
    app_in_field.send_keys(Keys.ENTER)

# takes a column header name and returns the corresponding value
# PREREQ: driver is set to page that holds element we are looking for
def getElem(col_name):

    if(col_name == "State"):
        return "CA"

    id = COL_HEADERS[col_name]
    return driver.find_element_by_id(id).text

################################################################################
##################### Execution code ###########################################

# Get list of app numbers
with open(INPUT_PATH) as infile:
    app_nums = infile.read().splitlines()

rows = []
# For each app number
for app in app_nums:

    # visit its page
    enterAppNum(app)

    # Get all the info we want
    curr_row = []
    for key in COL_HEADERS.keys():
        curr_row.append(getElem(key))

    rows.append(curr_row)



# Create output file
with open(OUT_PATH, 'w', newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerow(list(COL_HEADERS.keys()))

    for row in rows:
        writer.writerow(row)
driver.close()