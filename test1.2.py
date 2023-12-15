
#dont knwo what reason i was using thsi code for.....


import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_page(url):
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        data = []
        for row in table.find_all('tr')[1:]:
            columns = row.find_all('td')
            row_data = [column.get_text(strip=True) for column in columns]
            
            # Extract link from the last column
            details_link = columns[-1].find('a')['href']
            
            # Retrieve data from the linked page
            details_data = scrape_details_page(details_link)
            
            # Append details_data to row_data
            row_data.extend(details_data)
            
            data.append(row_data)
        return data
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

def scrape_details_page(link):
    full_url = f"https://www.bgmea.com.bd{link}"  # Assuming links are relative URLs
    response = requests.get(full_url, timeout=10)
    
    if response.status_code == 200:
        details_soup = BeautifulSoup(response.text, 'html.parser')
        
        # Replace 'your-details-class' with the actual class or tag to find the details
        details_data = details_soup.find('div', class_='your-details-class').get_text(strip=True)
        
        return [details_data]
    else:
        print(f"Failed to retrieve details page. Status code: {response.status_code}")
        return ['N/A']

def scrape_all_pages(base_url, total_pages):
    all_data = []
    for page in range(1, total_pages + 1):
        url = f"{base_url}{page}"
        page_data = scrape_page(url)
        if page_data:
            all_data.extend(page_data)
    return all_data

base_url = 'https://www.bgmea.com.bd/page/member-list?page='
total_pages = 190  # Update this to the total number of pages

all_data = scrape_all_pages(base_url, total_pages)

# Use a different variable name for columns in the local scope
columns_names = ['Member/Company Name', 'BGMEA Reg No', 'Contact Person', 'Email Address', 'Details']
df = pd.DataFrame(all_data, columns=columns_names)

df.to_csv('data_with_details.csv')

