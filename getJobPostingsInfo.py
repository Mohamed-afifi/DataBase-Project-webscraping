import csv
from selenium import webdriver
import time
from bs4 import BeautifulSoup


# Initialize a WebDriver
driver = webdriver.Edge()
count=0
# Open the file "job_links.txt" and read the links
with open("D:\Study\DB\MS2\job_links.csv", "r") as file:
    job_links = file.readlines()

with open('scraped.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)



    csv_writer.writerow([
            'Job Title', 'Job URL', 'Experience Needed', 'Company Name',
            'Location', 'Career Level', 'Education Level', 'Salary',
            'Job Categories', 'Skills and Tools', 'Job Description', 'Job Requirements'
        ])


    # Loop through the job links
    for link in job_links:
        url = link.strip()  # Remove any leading/trailing whitespace
        driver.get(url)
        time.sleep(10)
        page_html = driver.page_source
        soup = BeautifulSoup(page_html, 'html.parser')

        # Extract job title
        job_title_element = soup.select_one('#app > div > main > section.css-dy1y6u > div > h1')
        if job_title_element:
            job_title = job_title_element.get_text()
        else:
            job_title="N/A"
            


        # Extract experience text
        experience_element = soup.select_one('#app > div > main > section.css-3kx5e2 > div:-soup-contains("Experience Needed") > span.css-47jx3m > span')
        if experience_element:
            experience_text = experience_element.get_text()
        else:
            experience_text="No experince needed"

        # Extract the company name and location
        company_location_elements = soup.find_all('strong', {'class': 'css-9geu3q'})
        company_name = "N/A"
        location = "N/A"

        for element in company_location_elements:
            text = element.get_text(strip=True)
            last_hyphen = text.rfind('-')

            if last_hyphen != -1:
                company_name = text[:last_hyphen].strip()
                location = text[last_hyphen + 1:].strip()

        career_level_element=soup.select_one('#app > div > main > section.css-3kx5e2 > div:nth-child(3) > span.css-47jx3m > span')
        if career_level_element:
            career_level_text=career_level_element.get_text()
        else:
            career_level_text="No career level needed"

        
        
        educational_level_element=soup.select_one('#app > div > main > section.css-3kx5e2 > div:nth-child(4) > span.css-47jx3m > span')
        if educational_level_element:
            educational_level_text=educational_level_element.get_text()
        else :
            educational_level_text="No educational level found"


        salary_element=soup.select_one('#app > div > main > section.css-3kx5e2 > div:nth-child(5) > span.css-47jx3m > span')
        if salary_element:
            salary_text=salary_element.get_text()
        else:
            salary_text="No Salary was found"


        job_categories_element=soup.select_one('#app > div > main > section.css-3kx5e2 > div.css-13sf2ik > ul > li > a > span')
        if job_categories_element:
            job_categories_text=job_categories_element.get_text()
        else:
            job_categories_text="No job categories were found"


        skills_div = soup.find('div', class_='css-s2o0yh')
        skills_and_tools = []
        if skills_div:
            skill_links = skills_div.find_all('a', class_='css-g65o95')

        for link in skill_links:
            skill_name = link.text.strip()
            skills_and_tools.append(skill_name)
        else:
            skills_and_tools.append("No skills and tools found")

        # Locate the job description section
        
        job_description_element=soup.select_one('#app > div > main > section:nth-child(3) > div')
        if job_description_element:
            job_description_text=job_description_element.get_text()
        else:
            job_description_text="No Job description was found"

        job_requirments_element=soup.select_one('#app > div > main > section:nth-child(4) > div')
        if job_requirments_element:
            job_requirments_text=job_requirments_element.get_text()
        else:
            job_requirments_text="No Job requirments found"

        # Print or store the job title and experience text for this job
        print(f"Job Title: {job_title}")
        print(f"Job URL: {url}")
        print(f"Experience Needed: {experience_text}\n")
        print(f"Company Name: {company_name}")
        print(f"Location: {location}\n")
        print(f"Career Level :{career_level_text}\n")
        print(f"Education Level: {educational_level_text}\n")
        print(f"Salary : {salary_text}\n")
        print(f"Job Categories {job_categories_text}\n")
        print(f"Skills and tools : {skills_and_tools}\n")
        print(f"Job Description:{job_description_text}\n")
        print(f"Job Requirements:{job_requirments_text}\n")
        
        csv_writer.writerow([
                job_title, url, experience_text, company_name, location,
                career_level_text, educational_level_text, salary_text,
                job_categories_text, ', '.join(skills_and_tools), job_description_text, job_requirments_text
            ])
        
        count+=1

        print(f"Finsished Scraping and saving for Job URL: {url}\n")
        print(f"{count}/1389")



# Close the WebDriver
driver.quit()
