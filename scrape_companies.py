import csv
from selenium import webdriver
import time
from bs4 import BeautifulSoup

# Initialize a WebDriver
driver = webdriver.Edge()
count = 0

# Open the file "companies_links.csv" and read the links from the "Link" column
with open("D:\Study\DB\MS2\companies_links.csv", "r") as file:
    reader = csv.DictReader(file)
    companies_links = [row["Link"] for row in reader]

with open('Companies_Info.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)

    csv_writer.writerow([
        'Company name', 'Company URL', 'Location', 'Founded',
        'Industry', 'Company size', 'Description'
    ])

    # Loop through the job links
    for link in companies_links:
        url = link.strip()  # Remove any leading/trailing whitespace
        driver.get(url)
        time.sleep(10)
        page_html = driver.page_source
        soup = BeautifulSoup(page_html, 'html.parser')

        company_name_element = soup.select_one('#app > div > div:nth-child(2) > div > div > div.css-12e2e2p > div.css-1eoy87d > h1')
        if company_name_element:
            company_name = company_name_element.get_text()
        else:
            company_name = "Could not find company name"

        company_url = link

        company_location_element = soup.select_one('#profile-section > div > span:nth-child(1) > span.css-16heon9')
        if company_location_element:
            company_location = company_location_element.get_text()
        else:
            company_location = "Location not provided"

        company_foundation_element = soup.select_one('#profile-section > div > span:nth-child(2) > span.css-6whuzn')
        if company_foundation_element:
            company_foundation = company_foundation_element.get_text()
        else:
            company_foundation = "Foundation date not provided"

        company_industry_element = soup.select_one('#profile-section > div > span:nth-child(3) > span.css-16heon9 > span > a')
        if company_industry_element:
            company_industry = company_industry_element.get_text()
        else:
            company_industry = "Industry not provided"

        company_size_element = soup.select_one('#profile-section > div > span:nth-child(4) > span.css-16heon9')  
        if company_size_element:
            company_size = company_size_element.get_text()
        else:
            company_size = "Size not provided"
        
        description_element=soup.select_one('#profile-section > p') # I forgot to add this one, description while scrapping so I did not scrape, but this is the code and it is working
        if description_element:
            description=description_element.get_text()
        else:
            description="No Description was found"

        count += 1

        print(f"Company Name: {company_name}")
        print(f"Finished Scraping and saving for company URL: {url}\n")
        print(f"Location: {company_location}")
        print(f"Founded: {company_foundation}")
        print(f"Industry: {company_industry}")
        print(f"Company Size: {company_size}")
        print(f"Description: {description}")
        print(f"{count}/{len(companies_links)}")
        csv_writer.writerow([
            company_name, company_url, company_location, company_foundation,
            company_industry, company_size, description,""
        ])

# Close the WebDriver
driver.quit()
