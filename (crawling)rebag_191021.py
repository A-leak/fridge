import requests
from bs4 import BeautifulSoup
import csv


def get_links(): # function loading url of each items.
    req = requests.get('https://shop.rebag.com/collections/all-bags?_=pf&pf_st_availability_hidden=true')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('.product-caption > .product-vendor')
    itemurl = []

    for title in links:
        itemurl.append(title.get('href')) # make list "itemurl" for first page
    
    i=2

    # append list "itemurl" from second page
    while i : 
        req = requests.get('https://shop.rebag.com/collections/all-bags?page=' + str(i) + '&_=pf&pf_st_availability_hidden=true')
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select('.product-caption > .product-vendor')
        for item in links:
            itemurl.append(item.get('href'))
        i += 1

        if i == 110:  #escape
            break

    return itemurl


# get info. from each item url : vendor, name, price, description
itemurl = get_links()
rebag_list = []

for item in itemurl:
    req = requests.get('https://shop.rebag.com' + item)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    vendor = soup.select_one('h1 > a').text
    name = soup.select_one('h2').text
    price = soup.select_one('span').text
    description = soup.select_one('div.content > p').text

    temp=[] # make list of each item
    temp.append(vendor)
    temp.append(name)
    temp.append(price)
    temp.append(description)
    rebag_list.append(temp) # append info. of item to "rebag_list"

# extract final result into csv
with open('result.csv' , 'w', encoding = 'utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['vendor', 'name', 'price', 'description'])
    writer.writerows(rebag_list)