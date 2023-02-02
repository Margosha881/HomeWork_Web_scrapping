import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json



HOST = 'https://spb.hh.ru/'
keywords = ('Django','Flask')

def get_headers():
    return Headers(browser='firefox',os='win').generate()

def get_vacancy_list(currency_code=None):
    uri = f'{HOST}/search/vacancy'
    params = {
        'text': ['Python','Django','Flask'],
        'area': [1 , 2],
        'currency_code':currency_code
    }
    return requests.get(uri,headers=get_headers(),params=params).text

def parsed_vacancy():
    soup = BeautifulSoup(get_vacancy_list(), features='lxml')
    all_jobs = soup.find('div', class_='vacancy-serp-content')
    vacancy_list = all_jobs.find_all('div', class_='vacancy-serp-item__layout')
    parsed = []
    for vacancy in vacancy_list:
        try:
            vacancy_requriement = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
        except AttributeError:
            continue
        if set(keywords).issubset(vacancy_requriement.split()):
            city = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
            link_search = vacancy.find('a', class_='serp-item__title')
            link_absolute = link_search['href']
            company = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0',' ')
            try:
                salary = vacancy.find('span', class_='bloko-header-section-3').text.replace('\u202f',' ')
            except AttributeError:
                continue
            vacancy_info = {
                'link': link_absolute,
                'salary': salary,
                'company': company,
                'city': city
            }
            parsed.append(vacancy_info)
    return parsed

if __name__ == '__main__':
    all_vacancy = parsed_vacancy()
    with open('all_vacancy.json', 'w', encoding='utf-8') as outfile:
        json.dump(all_vacancy, outfile, ensure_ascii=False, indent=4)












