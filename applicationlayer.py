import mysql.connector
# Establishing a connection
server = 'db4free.net'
port = 3306
database = 'afifi_ms3'
username = 'mohamed_afifi'
password = 'steam@1412'

# Constructing the connection dictionary
db_config = {
    'host': server,
    'port': port,
    'database': database,
    'user': username,
    'password': password,
}

# Creating a MySQL connection object
connection = mysql.connector.connect(**db_config)

# Creating a cursor object
cursor = connection.cursor()

def execute_query(query):
    
    try:
        cursor.execute(query)
        print("Executed")
        # connection.commit()
        print("Commited")
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Error executing the query: {err}")
        connection.rollback()
        return None



def insert_query(query):
    
    try:
        cursor.execute(query)
        print("Executed")
        connection.commit()
        print("Commited")
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Error executing the query: {err}")
        connection.rollback()
        return None


# Register a user
def register_user(email, username, gender, birthdate, gpa, skills):
    query = f"""
        INSERT INTO Users_info (Email, Username, Gender, Birthdate, GPA, Skills)
        VALUES ('{email}', '{username}', '{gender}', '{birthdate}', {gpa}, '{skills}');
    """
    return insert_query(query)

# Add a new user application for an existing Job posting
def add_user_application(application_date, cover_letter, job_posting_url):
    query = f"""
        INSERT INTO JobApplications_info (ApplicationDate, CoverLetter, JobPostingURL)
        VALUES ('{application_date}', '{cover_letter}', '{job_posting_url}');
    """
    return insert_query(query)

# Show all the job postings for a given sector
def get_job_postings_by_sector(sector):
    query = f"""
        SELECT * FROM JobPostings
        WHERE JobCategories LIKE '%{sector}%';
    """
    return execute_query(query)

# Show all the job postings for a given set of skills
def get_job_postings_by_skills(skills):
    query = f"""
        SELECT * FROM JobPostings
        WHERE SkillsAndTools LIKE '%{skills}%';
    """
    return execute_query(query)

# Show the top 5 sectors by the number of job posts and the average salary range for each
def get_top_5_sectors_and_average_salary():
    query = """
        SELECT JobCategories, COUNT(*) AS JobCount, AVG(CAST(REPLACE(Salary, '$', '') AS DECIMAL(10,2))) AS AverageSalary
        FROM JobPostings
        GROUP BY JobCategories
        ORDER BY JobCount DESC
        LIMIT 5;
    """
    return execute_query(query)

# Show the top 5 skills that are in the highest demand
def get_top_5_demand_skills():
    query = """
        SELECT Skills, COUNT(*) AS SkillCount
        FROM Users_info
        GROUP BY Skills
        ORDER BY SkillCount DESC
        LIMIT 5;
    """
    return execute_query(query)

# Show the top 5 growing startups in Egypt by the amount of vacancies they have compared to their foundation date
def get_top_5_growing_startups():
    query = """
        SELECT Company_name, Founded, COUNT(JobTitle) AS VacancyCount
        FROM Companies_Info ci
        JOIN JobPostings jpi ON ci.Company_name = jpi.CompanyName
        WHERE (jpi.Location LIKE '%Egypt%' OR jpi.Location LIKE '%Cairo%' OR jpi.Location LIKE '%Giza%')
        GROUP BY Company_name, Founded
        ORDER BY VacancyCount DESC
        LIMIT 5;
    """
    return execute_query(query)

# Show the top 5 most paying companies in the field in Egypt
def get_top_5_paying_companies():
    query = """
        SELECT Company_name, AVG(CAST(REPLACE(Salary, '$', '') AS DECIMAL(10,2))) AS AverageSalary
        FROM Companies_Info ci
        JOIN JobPostings jpi ON ci.Company_name = jpi.CompanyName
        WHERE jpi.Location LIKE '%Egypt%' OR jpi.Location LIKE '%Cairo%' OR jpi.Location LIKE '%Giza%'
        GROUP BY Company_name
        ORDER BY AverageSalary DESC
        LIMIT 5;
    """
    return execute_query(query)

# Show all the postings for a given company / organization
def get_postings_by_company(company_name):
    query = f"""
        SELECT * FROM JobPostings
        WHERE CompanyName = '{company_name}';
    """
    return execute_query(query)

# Show the top 5 categories (other than IT/Software Development) that the postings are cross-listed under based on the volume of postings
def get_top_5_categories():
    query = """
        SELECT JobCategories, COUNT(*) AS CategoryCount
        FROM JobPostings
        WHERE JobCategories NOT LIKE '%IT/Software Development%'
        GROUP BY JobCategories
        ORDER BY CategoryCount DESC
        LIMIT 5;
    """
    return execute_query(query)


# Menu function
def display_menu():
    print("\nMenu:")
    print("1- Register a user")
    print("2- Add a new user application for an existing Job posting")
    print("3- Show all the job postings for a given sector")
    print("4- Show all the job postings for a given set of skills")
    print("5- Show the top 5 sectors by number of job posts, and the average salary range for each")
    print("6- Show the top 5 skills that are in the highest demand")
    print("7- Show the top 5 growing startups in Egypt by the amount of vacancies they have compared to their foundation date")
    print("8- Show the top 5 most paying companies in the field in Egypt")
    print("9- Show all the postings for a given company / organization")
    print("10- Show the top 5 categories (other than IT/Software Development) that the postings are cross-listed under based on the volume of postings")
    print("Type 'no' to exit")



# Main loop
while True:
    
    display_menu()
    
    # Get user input
    choice = input("Enter your choice (1-10 or 'no' to exit): ")

    if choice.lower() == 'no':
        break

    # Perform corresponding function based on user input
    if choice == '1':
        # Register a user
        # Get user details as input
        email = input("Enter email: ")
        username = input("Enter username: ")
        gender = input("Enter gender: ")
        birthdate = input("Enter birthdate: ")
        gpa = input("Enter GPA: ")
        skills = input("Enter skills: ")

        # Call the function
        result = register_user(email, username, gender, birthdate, gpa, skills)
        print(result)

    elif choice == '2':
        # Add a new user application for an existing Job posting
        # Get application details as input
        application_date = input("Enter application date: ")
        cover_letter = input("Enter cover letter: ")
        job_posting_url = input("Enter job posting URL: ")

        # Call the function
        result = add_user_application(application_date, cover_letter, job_posting_url)
        print(result)

    elif choice == '3':
        # Show all the job postings for a given sector
        sector = input("Enter sector: ")
        str_sector=str(sector)
        result = get_job_postings_by_sector(str_sector)
        print(result)
    elif choice == '4':
        # Show all the job postings for a given set of skills
        skills = input("Enter skills: ")
        str_skills=str(skills)
        result = get_job_postings_by_skills(str_skills)
        print(result)
    elif choice == '5':
        # Show the top 5 sectors by the number of job posts, and the average salary range for each
        result = get_top_5_sectors_and_average_salary()
        print(result)
    elif choice == '6':
        # Show the top 5 skills that are in the highest demand
        result = get_top_5_demand_skills()
        print(result)
    elif choice == '7':
        # Show the top 5 growing startups in Egypt by the amount of vacancies they have compared to their foundation date
        result = get_top_5_growing_startups()
        print(result)
    elif choice == '8':
        # Show the top 5 most paying companies in the field in Egypt
        result = get_top_5_paying_companies()
        print(result)
    elif choice == '9':
        # Show all the postings for a given company / organization
        company_name = input("Enter company name: ")
        str_company_name=str(company_name)
        result = get_postings_by_company(str_company_name)
        print(result)
    elif choice == '10':
        # Show the top 5 categories (other than IT/Software Development) that the postings are cross-listed under based on the volume of postings
        result = get_top_5_categories()
        print(result)
    # Closing the cursor and connection
    cursor.close()
    connection.close()    


