import csv
import random
import faker

# Create a Faker generator for generating random data
fake = faker.Faker()

# Define the number of dummy records you want to generate
num_users = 500
num_applications = 500

# Initialize sets to keep track of generated data
generated_emails = set()
generated_job_posting_urls = set()

# Generate dummy data for Users
users_data = []
while len(users_data) < num_users:
    email = fake.email()
    if email not in generated_emails:
        username = fake.user_name()
        gender = random.choice(['Male', 'Female', 'Other'])
        birthdate = fake.date_of_birth(minimum_age=18, maximum_age=50)
        gpa = round(random.uniform(1.0, 4.0), 2)  # Random GPA between 1.00 and 4.00
        skills = fake.text(max_nb_chars=200)
        users_data.append([email, username, gender, birthdate, gpa, skills])
        generated_emails.add(email)

# Save Users data to a CSV file
with open('Users.csv', 'w', newline='') as users_csv:
    users_writer = csv.writer(users_csv)
    users_writer.writerow(['Email', 'Username', 'Gender', 'Birthdate', 'GPA', 'Skills'])
    users_writer.writerows(users_data)

# Generate dummy data for JobApplications
applications_data = []
while len(applications_data) < num_applications:
    application_date = fake.date_between(start_date='-1y', end_date='today')
    job_posting_url = fake.uri()
    if job_posting_url not in generated_job_posting_urls:
        cover_letter = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
        applications_data.append([application_date, cover_letter, job_posting_url])
        generated_job_posting_urls.add(job_posting_url)

# Save JobApplications data to a CSV file
with open('JobApplications.csv', 'w', newline='') as applications_csv:
    applications_writer = csv.writer(applications_csv)
    applications_writer.writerow(['ApplicationDate', 'CoverLetter', 'JobPostingURL'])
    applications_writer.writerows(applications_data)
