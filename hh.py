import requests
import fake_headers
import bs4
import json


result = []
try:
    while True:
        headers = fake_headers.Headers(browser='firefox', os='win')
        headers_data = headers.generate()

        main_html = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2",
                                 headers=headers_data).text
        main_soup = bs4.BeautifulSoup(main_html, 'lxml')

        tag_content = main_soup.find('div', id='a11y-main-content')
        div_item_tags = tag_content.find_all('div', class_='serp-item')

        for div_item_tag in div_item_tags:
            vacancy = div_item_tag.find('h3')
            link = vacancy.find('a').get('href')
            try:
                salary = div_item_tag.find('span', class_='bloko-header-section-3').text.replace('\u202f', '')
            except:
                salary = 'Не указана'
            company = div_item_tag.find('a', class_='bloko-link bloko-link_kind-tertiary').text.replace('\xa0', '')
            city = div_item_tag.find('div', class_='vacancy-serp-item__info').contents[1].contents[0]
            result.append(
                {
                    "вакансия": vacancy.text,
                    "ссылка": link,
                    "зарплата": salary,
                    "название компании": company,
                    "город": city
                }
            )

except:
    print(f'Добавлено {len(result)} вакансий')

    if __name__ == "__main__":
        with open('result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=5)