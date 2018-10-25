from bs4 import BeautifulSoup
from rightmoveitem import RightMoveItem
import requests
import re
import numpy as np
import csv as csv
import sys
import pandas as pd
from lxml import html

class _Const(object):

    def NA(self):
        def fset(self, value):
            raise TypeError
        def fget(self):
            return "N/A"


class RightMoveParser:

    results = None

    def __init__(self):
        pass

    def __getSearchPage(self, webpage):
        """
        Download (request) the page from the url
        :param webpage: the url
        :return: the page
        """
        page = requests.get(webpage)
        return page

    def __clearData(self):
        """
        Clear the results
        :return: no return valute
        """
        self.results = []

    def __get_page(self, page_number, min_price=None, max_price=None):
        """
        Private function to get the url for a right move page
        :param page_number: the page number (1 to 42)
        :param min_price: the minimum price. Must be a multiple of 10000
        :param max_price: the maximum price. Must be a multiple of 10000
        :return: the webpage as a string
        """
        if page_number == 1:
            webpage = "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E904&includeSSTC=false"
        else:
            index = (page_number - 1) * 24
            webpage = "https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E904&index=" + str(index) + "&includeSSTC=false"

        if min_price or max_price:
            if max_price:
                extension = "&maxPrice=" + str(max_price)
            if min_price:
                extension = extension + "&minPrice=" + str(min_price)
            webpage = webpage + extension
        return webpage

    def search(self, debug=True):
        """
        Search through each page
        :param debug: if debug is true, print info to screen
        :return: no return value
        """
        inc=10000
        for price in range(0, 50000, inc):
            if debug:
                print("From " + str(price) + " to " + str(price + inc))
            res = self.__search(1, set_page_count=True, min_price=price, max_price=price + inc);
            if self.results is not None:
                self.results.append(res)
            else:
                self.results = res

            print(self.page_count)
            for page_number in range(2, self.page_count + 1):
                if debug:
                    print("Getting page: " + str(page_number))
                res = self.__search(page_number, min_price=price, max_price=price + inc)
                if self.results is not None:
                    self.results.append(res)
                else:
                    self.results = res

    @staticmethod
    def get_id_regex(id_text: str) -> int:
        '''
        Get id of property
        :param id_text: 
        :return: the property id
        '''
        property_id = int(id_text[len("property-"):])
        return property_id

    @staticmethod
    def get_date_regex(datedesc: str) -> str:
        pattern = re.compile(r'\d{1,2}/\d{1,2}/\d{4}', re.UNICODE)
        m = pattern.search(datedesc)
        if m:
            date = m.group()
        else:
            date = None
        return date

    @staticmethod
    def get_price_regex(pricedesc: str) -> int:
        pattern = re.compile(r'[0-9,]+', re.UNICODE)
        m = pattern.search(pricedesc)
        if m:
            price = int(m.group().replace(",", ""))
        else:
            price = None
        return price

    def __search(self, page_number, clear_data = False, set_page_count=False, min_price=None, max_price=None):
        """
        Parse info from page number
        :param page_number: the page number. Can range from 1 to a maximum of 42 (set by rightmove)
        :param clear_data: do we want to clear the data in the class. I'll probably remove this parameter
        :param set_page_count: set the page count (which you can find from each search). the page count is the number
            of pages for the search parameters
        :param min_price: the minimum price in the search
        :param max_price: the maximum price in the search
        :return: returns the page, otherwise None
        """
        if clear_data:
            self.__clearData();
        webpage = self.__get_page(page_number, min_price, max_price)
        page = self.__getSearchPage(webpage)

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'lxml')
            tree = html.fromstring(page.content)

            if set_page_count:
                span_results_count = soup.find("span", {"class": "searchHeader-resultCount"})
                if span_results_count:
                    span_results_count_text = span_results_count.text.strip()
                    pattern = re.compile(r'[0-9,]+', re.UNICODE)
                    m = pattern.search(span_results_count_text)
                    if m:
                        results_count = int(m.group().replace(",", ""))
                        self.page_count = int(results_count / 24.0 + 0.5)
                    else:
                        results_count = "N/A"
                        self.page_count = -1

            xp_id = '//*[contains(@id, "property") and starts-with(@class, "l-searchResult")]/@id'
            xp_desc = '//*[starts-with(@id, "property-")]/div/div[1]/div[4]/div[1]/div[2]/a/h2/text()'
            xp_price = '//*[starts-with(@id, "property-")]/div/div[1]/div[3]/div/a/div[1]/text()'
            xp_address = '//*[starts-with(@id, "property-")]/div/div[1]/div[4]/div[1]/div[2]/a/address/span/text()'
            xp_date_added = '//*[starts-with(@id, "property-")]/div/div[1]/div[4]/div[2]/div[3]/span[1]/text()'
            xp_agent = '//*[starts-with(@id, "property-")]/div/div[1]/div[4]/div[2]/div[3]/span[2]/text()'

            id = tree.xpath(xp_id)
            id[:] = [RightMoveParser.get_id_regex(x) for x in id]

            desc = tree.xpath(xp_desc)
            desc[:] = [x.strip() for x in desc]

            prices = tree.xpath(xp_price)
            prices[:] = [RightMoveParser.get_price_regex(x.strip()) for x in prices]

            addresses = tree.xpath(xp_address)

            date_added = tree.xpath(xp_date_added)
            date_added[:] = [RightMoveParser.get_date_regex(x.strip()) for x in date_added]

            agents = tree.xpath(xp_agent)


            data = [id, desc, prices, addresses, date_added, agents]
            temp_df = pd.DataFrame(data)
            temp_df = temp_df.transpose()
            temp_df.columns = ["id", "description", "price", "address", "date added", "agent"]

            temp_df = temp_df[temp_df["address"].notnull()]

            return temp_df

    def save(self, filename):
        """this function needs fixing"""
        with open(filename, "w+") as my_csv:
            csv_writer = csv.writer(my_csv, delimiter=',')
            csv_writer.writerows([[item.id, item.desc, item.address, item.price, item.date, item.reduced, item.agent] for item in self.results])


