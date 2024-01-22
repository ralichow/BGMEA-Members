# BGMEA-Members


The code defines two functions: scrape_page(url) to scrape data from a single page and scrape_all_pages(base_url, total_pages) to scrape data from all pages.
The script uses the requests library to make HTTP GET requests to web pages and BeautifulSoup to parse the HTML content.
Data is extracted from HTML tables on each page, and the results are stored in a list (all_data).
The collected data is then used to create a pandas DataFrame (df) with specific column names.
Optionally, the script can print the DataFrame (print(df)) to display the results.
Finally, the DataFrame is saved to a CSV file named 'data.csv' using the to_csv method.
