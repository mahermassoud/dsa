from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


driver = webdriver.Chrome()
driver.get("https://www.apps2.dgs.ca.gov/dsa/tracker/Appno.aspx")

# Select drop down
dropdown = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_drpdnOffice'))
dropdown.select_by_visible_text('04-SAN DIEGO')

# Input app num
app_in_field = Select(driver.find_element_by_id('ctl00_ContentPlaceHolder1_drpdnOffice'))
