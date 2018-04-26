import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib2
import time
import os
# We've now imported the two packages that will do the heavy lifting
# for us, reqeusts and BeautifulSoup

# Let's put the URL of the page we want to scrape in a variable
# so that our code down below can be a little cleaner
url_to_scrape = 'http://www.asamblea.go.cr/glcp/SitePages/ConsultaActasPlenario.aspx'
# url_to_scrape = 'http://www.asamblea.go.cr/glcp/SitePages/ConsultaActasPlenario.aspx'

# Tell requests to retreive the contents our page (it'll be grabbing
# what you see when you use the View Source feature in your browser)
r = requests.get(url_to_scrape)

# We now have the source of the page, let's ask BeaultifulSoup
# to parse it for us.
soup = BeautifulSoup(r.text, "html.parser")

# Down below we'll add our inmates to this list
inmates_list = []

# BeautifulSoup provides nice ways to access the data in the parsed
# page. Here, we'll use the select method and pass it a CSS style
# selector to grab all the rows in the table (the rows contain the
# inmate names and ages).

for table_row in soup.select("tbody > tr > td"):
    # Each tr (table row) has three td HTML elements (most people
    # call these table cels) in it (first name, last name, and age)
    cells = table_row.get_text()
    print(cells)



iframexx = soup.find_all('iframe')
# for iframe in iframexx:
print(iframexx[1].attrs['src'])
r1 = requests.get(iframexx[1].attrs['src'])
# response = urllib2.urlopen(iframe.attrs['src'])
iframe_soup = BeautifulSoup(r1.text, "html.parser")
#print(iframe_soup)



profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', os.getcwd())
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
driver = webdriver.Firefox(profile)

def download_file_table(driver):
    credit_table = driver.find_element_by_css_selector('#ContentPlaceHolder1_grvActasPlenario > tbody')
    for row in credit_table.find_elements_by_css_selector('tr'):
        for cell in row.find_elements_by_tag_name('td.btn'):
            cell.click()
    time.sleep(1)
#driver = webdriver.PhantomJS()
driver.get("http://www.asamblea.go.cr/glcp/SitePages/ConsultaActasPlenario.aspx")
iframe = driver.find_elements_by_tag_name('iframe')[1]

## Give time for iframe to load ##
driver.switch_to.frame(iframe)

# interact with your element inside the iframe
download_file_table(driver)

next = driver.find_element_by_css_selector('tr:nth-child(17) > td > table > tbody > tr > td > input[type="image"]')
next.click()
try:
    while(1):
        # download all files from the iframe
        download_file_table(driver)

        #next table
        next = driver.find_element_by_css_selector(
            'tr:nth-child(17) > td > table > tbody > tr > td:nth-child(2) > input[type="image"]')

        #click button
        next.click()
except SyntaxError:
    print("syn")
finally:
    driver.quit()
        # ContentPlaceHolder1_grvActasPlenario > tbody > tr:nth-child(17) > td > table > tbody > tr > td > input[type="image"]
        # ContentPlaceHolder1_grvActasPlenario > tbody > tr:nth-child(17) > td > table > tbody > tr > td:nth-child(2) > input[type="image"]
        # ContentPlaceHolder1_grvActasPlenario > tbody > tr:nth-child(17) > td > table > tbody > tr > td:nth-child(2) > input[type="image"]
           # print(cell.text)