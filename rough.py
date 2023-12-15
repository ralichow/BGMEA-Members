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
        
        # Extract information from the "Address Information" tab
        address_tab = soup.find('a', {'data-target': '#address_info'})
        address_table = soup.find('div', {'id': 'address_info'}).find('table')
        address_rows = address_table.find_all('tr')
        address_data = []
        for row in address_rows:
            columns = row.find_all('td')
            if len(columns) == 2:
                address_data.extend([columns[0].get_text(strip=True), columns[1].get_text(strip=True)])
        
        return [bgmea_reg_no, epb_reg_no] + director_data + address_data  # Add the extracted data from the "Address Information" tab
    else:
        print(f"Failed to retrieve member details from {member_url}. Status code: {response.status_code}")
        return ['N/A'] * 14  # Return a list with 14 'N/A' values to match the expected number of columns
