from bs4 import BeautifulSoup
import requests
import time
import os


print('Put some skill theat you are not familiar with')
unfamiliar_skill = input('>')
print(f'Filtering out {unfamiliar_skill}')
url = f'https://m.timesjobs.com/mobile/jobs-search-result.html?txtKeywords={
    unfamiliar_skill}&txtLocation=&cboWorkExp1=-1'


def find_jobs():
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li')
    for index, job in enumerate(jobs):
        try:
            job_published_date = job.find('span', class_='posting-time').text
        except:
            job_published_date = 'few'
        if not 'few' in job_published_date:
            company_name = job.find('h4').text.strip()
            skills = job.find('div', class_='srp-keyskills').text.strip()
            more_info = job.h3.a['href']
            if unfamiliar_skill not in skills:
                if not os.path.exists(f'posts/{index}.txt'):
                    mode = 'x'
                else:
                    mode = 'w'
                with open(f'posts/{index}.txt', mode) as f:
                    f.write(job_published_date)
                    f.write(f'''
                    Company Name: {company_name}
                    Required Skills: {skills}
                    More info: {more_info}
                        ''')
                print(f'File saved {index}')


if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait*60)
