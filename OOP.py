import requests
from bs4 import BeautifulSoup
import pandas as pd

class Member:
    def __init__(self, bgmea_reg_no, epb_reg_no, directors):
        self.bgmea_reg_no = bgmea_reg_no
        self.epb_reg_no = epb_reg_no
        self.directors = directors

class Scraper:
    def __init__(self, base_url_param, total_pages):
        self.base_url_param = base_url_param
        self.total_pages = total_pages

    def scrape_member_details(self, member_url):
        # Implementation of scraping logic goes here
        pass

    def scrape_all_members(self):
        # Implementation of scraping all members goes here
        pass

class DataHandler:
    def __init__(self, column_names):
        self.column_names = column_names

    def save_to_csv(self, data, filename):
        # Implementation of saving data to CSV goes here
        pass

# Example usage
BASE_URL_PARAM = 'https://www.bgmea.com.bd/member/'
TOTAL_PAGES = 5
column_names = ['BGMEA Reg. No.', 'EPB Reg No.', 'Position', 'Name', 'Mobile No.', 'Email']

scraper = Scraper(BASE_URL_PARAM, TOTAL_PAGES)
all_member_data = scraper.scrape_all_members()

data_handler = DataHandler(column_names)
data_handler.save_to_csv(all_member_data, 'AllDetails.csv')
