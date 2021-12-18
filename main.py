import requests
from bs4 import BeautifulSoup


def read_webpage(page_link, headers):
    '''Ф-ия получает ссылку на WEB страницу и headers к ней. Делает GET запрос и возвращает объект BeautifulSoup'''
    resp = requests.get(page_link, headers=headers)
    resp.raise_for_status()
    text = resp.text
    return BeautifulSoup(text, features='html.parser')

def find_in_article(article_item, search_list):
    '''Ф-ия получает объект BeautifulSoup со страницы статей Хабр.
    Находит в описании статьи слова из списка search_list и выводит список с датой, названием и ссылкой,
    None - если ничего не найдено.'''
    for keyword in search_list:
        if keyword in article_item.text:
            title_block = article_item.find('a', class_='tm-article-snippet__title-link')
            title = title_block.find('span').text

            date_block = article_item.find('span', class_='tm-article-snippet__datetime-published')
            date = date_block.find('time').attrs['title']

            link = 'https://habr.com' + title_block.attrs['href']
            return [date, title, link]
    return None

def article_reader(article_item, search_list):
    '''Ф-ия получает объект BeautifulSoup со страницы статей Хабр. Определяет ссылку на текущую статью,
    открывает и прочитывает её. Выводит список с датой, названием и ссылкой, если в тексте статьи были
    найдены слова из списка search_list, None - если ничего не найдено.'''
    article_link = article_item.find('a', class_='tm-article-snippet__title-link').attrs['href']
    link = 'https://habr.com' + article_link
    article_soup = read_webpage(link, HEADERS)
    article_content = article_soup.find('article').text
    for keyword in search_list:
        if keyword in article_content:
            article_head = article_soup.find('div', class_='tm-article-snippet tm-article-presenter__snippet')
            title = article_head.find('h1').find('span').text
            date = article_head.find('time').attrs['title']
            return [date, title, link]
    return None

def date_title_link(data_list):
    return f"<{data_list[0]}> - <{data_list[1]}> - <{data_list[2]}>"


if __name__ == '__main__':

    HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
               'Connection': 'keep-alive',
               'Cookie': '_ym_uid=1577900963171279125; _ym_d=1637351627; _ga=GA1.2.817503028.1637351628; hl=ru; fl=ru; __gads=ID=ca035f2597de0f18-229a700c05cd00c0:T=1637351631:S=ALNI_MaciBbAokc3Chdae_boSAkgWwi5LA; visited_articles=254773; cto_bundle=iOxtKF9MRjBLVUw0QlNkOHAlMkJOcXlNRFZYMDYxVEZ5MVZzMWhvVXA2NDR1dUlwdEtOaENNJTJCWCUyQjRMOUpQaVE0T1Z5REF1VXJzNmY0MFJRNVNLJTJCT3daZyUyRmlGcm8zanBWZldicWluUFc4ckZSdnBtU1ZsZmYlMkJ3ZEZQTlVOJTJGQzNZa0VTek5tdEo4M2cxbkU4bmVIbmwzTnJkeWpYZnE5R3hpY2klMkJwJTJCUElEUkQlMkJCRzQlMkJzJTNE; habr_web_home=ARTICLES_LIST_ALL; _ym_isad=2; _gid=GA1.2.1413196526.1639811364',
               'Host': 'habr.com',
               'Sec-Fetch-Dest': 'document',
               'Sec-Fetch-Mode': 'navigate',
               'Sec-Fetch-Site': 'none',
               'Sec-Fetch-User': '?1',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'
    }
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']

    webpage = 'https://habr.com/ru/all/'

    soup = read_webpage(webpage, HEADERS)
    articles = soup.find_all('article')

    print('KEYWORDS в описании:')
    for article in articles:
        search_result_1 = find_in_article(article, KEYWORDS)
        if search_result_1:
            print(date_title_link(search_result_1))

    print('KEYWORDS в тексте:')
    for article in articles:
        search_result_2 = article_reader(article, KEYWORDS)
        if search_result_2:
            print(date_title_link(search_result_2))