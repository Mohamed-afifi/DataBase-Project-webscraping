import csv
from bs4 import BeautifulSoup
import requests

base_url = "https://wuzzuf.net/a/IT-Software-Development-Jobs-in-Egypt?start={}"
job_links = []
total_links = 0

page = 0

# Specify the encoding as 'utf-8' when opening the CSV file
with open('job_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)

    while total_links < 1389:
        url = base_url.format(page)

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}. Status code:", response.status_code)
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        #Find job links using the specified class and 'rel' attribute
        job_link_elements = soup.find_all('a', {'class': 'css-o171kl', 'rel': 'noreferrer'})
        
        # Extract and store the href attributes in job_links
        for job_link_element in job_link_elements:
            job_url = job_link_element.get('href')
            print(job_url)
            csvwriter.writerow([job_url])
            total_links += 1
            if total_links >= 1389:
                break

        page += 1  # Increase the start index by 1 for the next page

print("Job links have been saved to job_links.csv")
