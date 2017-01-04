from selenium import webdriver
import csv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# Input file path, input file is plain text file where each line holds a single
# application number
INPUT_PATH = '/Users/massoudmaher/Desktop/app_nums.csv'

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
# TODO use orderedDict
APP_SUM_FIELDS = {
    "Office ID":"ctl00_ContentPlaceHolder1_lblOffice",
    "File Num":"ctl00_ContentPlaceHolder1_lblFile"
}
########################### End constants ##################################

driver = webdriver.Chrome()
driver.get("https://www.apps2.dgs.ca.gov/dsa/tracker/Appno.aspx")

print(APP_SUM_FIELDS.keys())
# Select required fields on page
dropdown_field = Select(driver.find_element_by_id(REG_DROPDOWN))
dropdown_field.select_by_visible_text(SD_REG)
app_in_field = driver.find_element_by_id(APP_NUM_IN_ID)

# Get list of app numbers
with open(INPUT_PATH) as infile:
    app_nums = infile.read().splitlines()

def enterAppNum(app_num):
    driver.get("https://www.apps2.dgs.ca.gov/dsa/tracker/Appno.aspx")
    dropdown_field = Select(driver.find_element_by_id(REG_DROPDOWN))
    dropdown_field.select_by_visible_text(SD_REG)
    app_in_field = driver.find_element_by_id(APP_NUM_IN_ID)

    app_in_field.send_keys(app_num)
    app_in_field.send_keys(Keys.ENTER)

enterAppNum(115070)

office_elem = driver.find_element_by_id("ctl00_ContentPlaceHolder1_lblOffice")
print(office_elem.text)

# Create output file
with open(OUT_PATH, 'w', newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerow(list(APP_SUM_FIELDS.keys()) )

#driver.close()
