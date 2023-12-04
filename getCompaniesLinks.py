import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time

count=0
# Initialize a WebDriver
driver = webdriver.Edge()

# Open the file "job_links.csv" and read the links
job_links = []
with open("job_links.csv", "r", encoding='utf-8') as file:
    job_links = file.readlines()

with open('companies_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Create a set to store the scraped companies
    scraped_companies = set()
    
    # Iterate through the job links
    for job_link in job_links:
        job_url = job_link.strip()  # Remove leading/trailing whitespace
        
        # Open the job URL
        driver.get(job_url)
        
        # Wait for some time to let the page load (you can adjust the time as needed)
        time.sleep(5)
        
        # Get the page source after it has loaded
        page_source = driver.page_source
        
        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find the company name and URL
        company_element = soup.find('a', {'class': 'css-p7pghv'})
        if company_element:
            company_name = company_element.text
            company_url = company_element['href']
            
            # Check if the company has already been scraped
            if company_name not in scraped_companies:
                csv_writer.writerow([company_name, company_url])
                scraped_companies.add(company_name)
                print(f"Company Name: {company_name}, Company URL: {company_url}")
            else:
                print("Company already saved")
        count+=1
        print(f"finished {count}/1389")
        
# Close the WebDriver
driver.quit()
