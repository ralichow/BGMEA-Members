#%%

#This is used to collect the data from each of the details page


#***Issues are listed below***

#Need to add all the details in all tabs

#Only works till page=9 



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
        
        return [bgmea_reg_no, epb_reg_no] + director_data
    else:
        print(f"Failed to retrieve member details from {member_url}. Status code: {response.status_code}")
        return ['N/A'] * 10  # Return a list with 10 'N/A' values to match the expected number of columns

def scrape_all_members(base_url, total_pages):
    all_data = []
    for page in range(1, total_pages + 1):
        member_url = f"{base_url}{page}"
        member_details = scrape_member_details(member_url)
        all_data.append(member_details)
    return all_data

# Example base URL for member pages
base_url = 'https://www.bgmea.com.bd/member/'
total_pages = 9



# Scrape details for all members
all_member_data = scrape_all_members(base_url, total_pages)

# Create a DataFrame with the collected data
columns_names = ['BGMEA Reg. No.', 'EPB Reg No.', 'Position', 'Name', 'Mobile No.', 'Email']
df = pd.DataFrame(all_member_data, columns=columns_names[:len(all_member_data[0])])

# Display the DataFrame
print(df)


df.to_csv('AllDetails.csv')