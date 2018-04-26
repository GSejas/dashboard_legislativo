import requests
from bs4 import BeautifulSoup
import re
import docx


from docx import Document
from docx.shared import Inches

def retrieve_prod_url(url):
    print(url)

    r = requests.get(url)

    soup = BeautifulSoup(r.text, "html.parser")

    list_links = []

    for links in soup.find_all("a")[20:-6]:
        # print(links.get_text())
        if links["href"][0] == '.':
            list_links.append(links["href"][1:])
        else:
            list_links.append(links["href"])

    return (list_links)


def product_text(urlnew):
    print(urlnew)
    r = requests.get(urlnew)
    soupling = BeautifulSoup(r.text, "html.parser")
    contien = re.compile(".*contiene(.*?)de(.*)")
    print(soupling.find_all('p')[0].get_text())
    # for i in soupling.find_all('p')[:-2]:
    # print(i.get_text())
    d = contien.match(soupling.find_all('p')[0].get_text())
    if d is not None:
        print(d.group(2))

    i = 0
    for y in soupling.select("a > img"):
        if i == 1:
            try:
                img_str = "http://www.lisancr.com/" + y["src"].split("/../../")[1]
                print(img_str)
            except IndexError:
                print("There was an error with the split here")
                print(y["src"])
                # add_down_image(document, img_str)
        i = i + 1


def add_down_image(doc, img_url):
    with open("my_image.jpg", "wb") as img_handle:
        img_data = requests.get(img_url)
        img_handle.write(img_data.content)
    doc.add_picture("my_image.jpg", width=Inches(5.64))


# We've now imported the two packages that will do the heavy lifting
# for us, reqeusts and BeautifulSoup

# Let's put the URL of the page we want to scrape in a variable
# so that our code down below can be a little cleaner
url_to_scrape = 'http://www.lisancr.com/ES/productos/'

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

# for table_row in soup.select("#block-system-main > div > div > div.view-content > div.views-row"):
# Each tr (table row) has three td HTML elements (most people
# call these table cels) in it (first name, last name, and age)
#	print(table_row)
#	print("\n\n")

# for links in soup.find_all('a'):
#        print(links.get('href'))

# print("Separating")


# document = Document()

i = 0
list_links = []

for links in soup.find_all("a")[20:-6]:
    a = links.get_text()
    print(links.get_text())
    if links["href"][0] == '.':
        list_links.append(links["href"][1:])
    else:
        list_links.append(links["href"])

print(list_links)

urlnew = "http://www.lisancr.com/ES/productos/division-humana/aciclovir-tabletas.html"

r = requests.get(urlnew)

soupling = BeautifulSoup(r.text, "html.parser")

for i in soupling.find_all('p')[:-2]:
    print(i.get_text())

i = 0
for y in soupling.select("a > img"):

    if i == 1:
        print(y["src"].split("/../../")[1])
    i = i + 1

for url in retrieve_prod_url(url_to_scrape):
    product_text("http://www.lisancr.com/ES/productos" + url)

    # document.save('demo5.docx')