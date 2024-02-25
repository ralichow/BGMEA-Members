
#%%

#This is used to collect the data from each of the details page


#***Issues are listed below***

#Need to add all the details in all tabs

#Only works till page=9

"""
This module scrapes member details from a website and exports the data to a CSV file.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_member_details(member_url):
    try:
        response = requests.get(member_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve member details from {member_url}. Error: {e}")
        return ['N/A'] * 6  # Return a list with 6 'N/A' values to match the expected number of columns

    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract relevant details based on the HTML structure
    bgmea_reg_no = soup.find('th', text='BGMEA Reg. No.').find_next('td').get_text(strip=True)
    epb_reg_no = soup.find('th', text='EPB Reg No.').find_next('td').get_text(strip=True)
    # Extract director information table
    director_table = soup.find('th', text='Director Informaiton').find_next('table')
    # Extract director details
    director_rows = director_table.find_all('tr')[1:]  # Skip the header row
    director_data = []

    for row in director_rows:
        columns = row.find_all('td')
        dir_position = columns[0].get_text(strip=True)
        dir_name = columns[1].get_text(strip=True)
        dir_mobile = columns[2].get_text(strip=True)
        dir_email = columns[3].get_text(strip=True)
        director_data.extend([dir_position, dir_name, dir_mobile, dir_email])
    result = [bgmea_reg_no, epb_reg_no] + director_data
    if len(result) != 6:
        print(f"Error: Data format is incorrect. Expected 6 columns, got {len(result)}")
        return ['N/A'] * 6  # Return a list with 6 'N/A' values
    return result



def scrape_all_members(BASE_URL_PARAM, TOTAL_PAGES):
    all_data = []
    for page in range(1, TOTAL_PAGES + 1):
        member_url = f"{BASE_URL_PARAM}{page}"
        member_details = scrape_member_details(member_url)
        all_data.append(member_details)
    return all_data

# Example base URL for member pages
BASE_URL_PARAM = 'https://www.bgmea.com.bd/member/'
TOTAL_PAGES = 4363

# Define the column names
column_names = ['BGMEA Reg. No.', 'EPB Reg No.', 'Position', 'Name', 'Mobile No.', 'Email']

# Scrape details for all members
all_member_data = scrape_all_members(BASE_URL_PARAM, TOTAL_PAGES)

# Create a DataFrame with the collected data
df = pd.DataFrame(all_member_data, columns=column_names[:len(all_member_data[0])])

# Display the DataFrame
#print(df)

# Save the DataFrame to a CSV file
df.to_csv('AllDetails.csv', index=False)
