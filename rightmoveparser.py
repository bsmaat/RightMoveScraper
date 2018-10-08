from bs4 import BeautifulSoup#
from rightmoveitem import RightMoveItem
import requests
import re

class _Const(object):


    def NA(self):
        def fset(self, value):
            raise TypeError
        def fget(self):
            return "N/A"


class RightMoveParser:

    CONST = _Const()

    webpage = "https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E904&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&_includeSSTC=on&sortByPriceDescending=&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&newHome=&auction=false"

    results = []

    def __init__(self):
        pass

    def __getSearchPage(self):
        page = requests.get(self.webpage)
        return page

    def __clearData(self):
        results = []

    def search(self):
        self.__clearData();
        page = self.__getSearchPage()

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')

            for div in soup.find_all("div", {"id": lambda value : value and value.startswith("property"),
                                             "class": "l-searchResult" }):
                idtext = div.attrs.get("id")
                id = idtext[len("property-"):]

                pricecard = div.find("a", {"class": "propertyCard-priceLink"})
                if pricecard:
                    priceDesc = pricecard.text.strip()
                    if priceDesc:
                        #pattern = re.compile(r'(.*)\s*(.*)', re.UNICODE)
                        pattern = re.compile(r'[£0-9,]+', re.UNICODE)
                        m = pattern.search(priceDesc)
                        if m:
                            price = m.group()
                        else:
                            price = "N/A"

                propertysection = div.find("div", {"class": "propertyCard-section"})
                housedesctag = propertysection.find("h2")

                if housedesctag:
                    housedesc = housedesctag.text.strip()
                else:
                    housedesc = "N/A"

                addresstag = div.find("address")

                if addresstag:
                    spantag = addresstag.find("span")
                    if spantag:
                        address = addresstag.text.strip()
                    else:
                        address = "N/A"

                branchtag = div.find("div", {"class": "propertyCard-branchSummary"})

                if branchtag:
                    datespantag = branchtag.find("span", {"class": "propertyCard-branchSummary-addedOrReduced"})
                    if datespantag:
                        datedesc = datespantag.text.strip()
                        pattern = re.compile(r'\d{1,2}/\d{1,2}/\d{4}', re.UNICODE)
                        m = pattern.search(datedesc)
                        if m:
                            date = m.group()
                        else:
                            date = "N/A"

                        pattern = re.compile(r'Reduced', re.UNICODE)
                        m = pattern.search(datedesc)
                        if m:
                            reduced = m.group()
                        else:
                            reduced = False

                    agenttag = div.find("span", {"class": "propertyCard-branchSummary-branchName"})
                    if agenttag:
                        agentdesc = agenttag.text.strip()
                        pattern = re.compile(r'by (.*)', re.UNICODE)
                        m = pattern.search(agentdesc)
                        if m:
                            agent = m.group(1)
                        else:
                            agent = "N/A"

                item = RightMoveItem(id, housedesc, address, price, date, reduced, agent)
                self.results.append(item)
        return page.content

