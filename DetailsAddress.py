import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_member_details(member_url):
    response = requests.get(member_url, timeout=10)
    
    if response.status_code == 200:
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
            director_position = columns[0].get_text(strip=True)
            director_name = columns[1].get_text(strip=True)
            director_mobile = columns[2].get_text(strip=True)
            director_email = columns[3].get_text(strip=True)
            director_data.extend([director_position, director_name, director_mobile, director_email])
        
        # Extract address information table
        address_table = soup.find('a', text='Address Information').find_next('table')
        
        # Extract address details
        address_rows = address_table.find_all('tr')[1:]  # Skip the header row
        address_data = []
        for row in address_rows:
            columns = row.find_all('td')
            address_label = columns[0].get_text(strip=True)
            address_value = columns[1].get_text(strip=True)
            address_data.extend([address_label, address_value])
        
        return [bgmea_reg_no, epb_reg_no] + director_data + address_data
    else:
        print(f"Failed to retrieve member details from {member_url}. Status code: {response.status_code}")
        return ['N/A'] * 16  # Return a list with 16 'N/A' values to match the expected number of columns

def scrape_all_members(base_url, total_pages):
    all_data = []
    max_columns = 0
    
    for page in range(1, total_pages + 1):
        member_url = f"{base_url}{page}"
        member_details = scrape_member_details(member_url)
        all_data.append(member_details)
        
        # Update max_columns based on the length of the current member_details
        max_columns = max(max_columns, len(member_details))
    
    return all_data, max_columns

# Example base URL for member pages
base_url = 'https://www.bgmea.com.bd/member/'
total_pages = 190

# Scrape details for all members and determine the maximum number of columns
all_member_data, max_columns = scrape_all_members(base_url, total_pages)

# Create a DataFrame with the collected data
columns_names = ['BGMEA Reg. No.', 'EPB Reg No.', 'Director Position', 'Director Name', 'Director Mobile No.', 'Director Email',
                  'Address Label', 'Address Value']
df = pd.DataFrame(all_member_data, columns=columns_names[:max_columns])

# Display the DataFrame
print(df)
