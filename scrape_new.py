import requests
from bs4 import BeautifulSoup
import pandas as pd



#thsi code scrapes factory name, address and the export type abd also ovverrides the error 404 pages



# Function to scrape company name from <th> element
def scrape_company_name(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    th_element = soup.find('th', class_='p-3')
    if th_element:
        return th_element.get_text(strip=True)
    else:
        return 'N/A'

# Function to scrape factory address from table
def scrape_factory_address(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    th_element = soup.find('th', text='Factory Address')
    if th_element:
        td_element = th_element.find_next('td')
        return td_element.get_text(separator='\n', strip=True)
    else:
        return 'N/A'

# Function to scrape principal exportable product from table
def scrape_exportable_product(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    th_element = soup.find('th', text='Principal Exportable Product')
    if th_element:
        td_element = th_element.find_next('td')
        return td_element.get_text(strip=True)
    else:
        return 'N/A'

# Function to scrape member details from the URL
def scrape_member_details(member_url):
    try:
        response = requests.get(member_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve member details from {member_url}. Error: {e}")
        return ['N/A'] * 3  # Return a list with 3 'N/A' values

    company_name = scrape_company_name(response.text)
    factory_address = scrape_factory_address(response.text)
    exportable_product = scrape_exportable_product(response.text)

    return [company_name, factory_address, exportable_product]

# Example base URL for member pages
BASE_URL_PARAM = 'https://www.bgmea.com.bd/member/'
TOTAL_PAGES = 4363

# Scrape details for all members
all_member_data = []
for page in range(1, TOTAL_PAGES + 1):
    member_url = f"{BASE_URL_PARAM}{page}"
    member_details = scrape_member_details(member_url)
    all_member_data.append(member_details)

# Create a DataFrame with the collected data
df = pd.DataFrame(all_member_data, columns=['Company Name','Factory Address','Principal Exportable Product'])

# Save the DataFrame to an Excel file
excel_file = 'company_details.csv'
df.to_csv(excel_file, index=False)

print(f"Data has been scraped and saved to '{excel_file}'.")
