from bs4 import BeautifulSoup
import requests
import re


job_keywords='+'.join(input("Job title, keyword or company: ").split())
job_postings=int(input("How many job postings would you like to see?"))
jobs_database=[0]
job_id=1
pages=0
bool=True

while bool:
    url =f"https://www.indeed.com/jobs?q={job_keywords}&l=New+York%2C+NY&start={pages}"
    indeed=requests.get(url)
    soup = BeautifulSoup(indeed.content,'html.parser')
    results=soup.find('td', id="resultsCol")

    def findJobs(tag):
        return tag.has_attr('class') and tag.has_attr('id') and tag.has_attr("data-tn-component") and tag.has_attr("data-jk")
    jobs=results.find_all(findJobs)

    for job in jobs:
        if len(jobs_database)<=job_postings:
            job_title=job.find('h2', class_='title')
            job_company=job.find('span', class_='company')
            job_location=job.find('span', class_=re.compile("location"))
            job_link=job.find('a')
            if None in (job_title,job_company, job_location, job_link):
                continue
            print(f"Job title #{job_id}:{job_title.text.strip()}")
            print(f"Job company: {job_company.text.strip()}")
            print(f"Job location: {job_location.text.strip()}")
            print(f"Job link: https://www.indeed.com{job_link['href']}")
            print(f"Job id: {job_id}")
            print('#'*75)
            jobs_database.append("https://www.indeed.com"+job_link['href'])
            job_id+=1
        else: bool=False
    pages+=1



skills=input("What are you main skills? (Please separate by a space): ").split()
matched_skills=[]
x=None

while type(x) is not int:
    try:
        x=int(input("In order to check whether your skills match the job you're interested in, enter the job id: "))
    except ValueError:
        print(f'{x} is not a valid job id')

url=jobs_database[x]
indeed=requests.get(url)
soup = BeautifulSoup(indeed.content,'html.parser')

for skill in skills:
    results = soup.find_all(string= lambda text: skill.lower() in text.lower())
    if len(results)>0:
        matched_skills.append([skill, results])
    results=0

print("This job matches the following skills:")
for i in range(0, len(matched_skills)):
    print(f'\n{matched_skills[i][0]} :')
    for j in range(0,len(matched_skills[i][1])):
        if len(matched_skills[i][1][j].strip('\n'))<250 and ('jobs' and 'Indeed.com' and 'job') not in matched_skills[i][1][j]:
            print(matched_skills[i][1][j].strip('\n'), end='\n')
