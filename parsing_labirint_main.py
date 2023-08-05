import json
import time

import requests
from bs4 import BeautifulSoup
import datetime
import csv

start_time = time.time()
def get_data():
    current_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%m')

    # Открываем файл на запись
    with open(f'file_books_{current_time}.csv', 'w', encoding='utf-8') as file:
        # создаём обьект писателя
        writer = csv.writer(file)
        # Сначало записываем заголовки столбцов
        writer.writerow(
            (
                'Название книги',
                'Автор',
                'Издательство',
                'Цена со скидкой',
                'Цена без скидки',
                'Скидка',
                'Наличие на складе',
                'Ссылка на издательство'
            )
        )
        # в цикле после итерации будем дописывать новые строки

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    url = 'https://www.labirint.ru/genres/2308/?display=table&page=1'
    response = requests.get(url, headers=headers)
    # первый аргумент текс ответа, а вторым lxml-парсер
    soup = BeautifulSoup(response.text, 'lxml')
    # Находим div с классом
    pages_count = int(
    soup.find('div', class_='pagination-number-viewport').findAll('a')[-2].text)
    books_data = []
    # создадим цикл for - где будем пробегать по всем страница с книгами
    for page in range(1, pages_count + 1):
    # for page in range(1, 2):
        url = f'https://www.labirint.ru/genres/2308/?display=table&page={page}'
        # отправляем get() - запрос
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        # И соберём все карточки в список
        book_cards = soup.find('tbody', class_='products-table__body').findAll('tr')
        # Список из карточек книг готов
        # Теперь нужно пробежатся по все tr - тегам и спарсить все что лежит в тегах td
        for td_teg in book_cards:
            book_data = td_teg.findAll('td')
            try:
                book_name = book_data[0].find('a').text.strip()
            except:
                book_name = 'Нет названия книги'

            try:
                book_author = book_data[1].text.strip()

            except:
                book_author = 'Нет автора'

            try:
                book_bublishing = book_data[2].findAll('a')
                book_bublishing = ': '.join([bk.text for bk in book_bublishing])
            except:
                book_bublishing = 'Нет издательства'

            try:
                book_author_url = 'https://www.labirint.ru' + book_data[2].findAll('a')[
                    0].get('href')
            except:
                book_author_url = 'Нет ссылки'

            try:
                book_price_sale = int(
                    book_data[3].find('div', class_='price').find('span').find(
                        'span').text.replace(' ', ''))
            except:
                book_price_sale = 'Нет новой цены'

            try:
                book_price_old = int(book_data[3].find('div', class_='price').find('span',
                                                                                   class_='price-old').find(
                    'span').text.replace(' ', ''))
            except:
                book_price_old = 'Нет старой цены'

            try:
                book_sale = round(100 - (book_price_sale / (book_price_old / 100)))
            except:
                book_sale = 'Нет скидки'

            try:
                stock_availability = book_data[5].find('div',
                                                       class_='mt3 rang-available').text.strip()
            except:
                stock_availability = 'Нет на складе'
                # теперь создадим список под собранные данные
                # Сохраним все данные в csv

            # print(book_name)
            # print(book_author)
            # print(book_bublishing)
            # print(book_price_sale)
            # print(book_price_old)
            # print(book_sale)
            # print(stock_availability)
            # print(book_author_url)
            # print('#' * 15)

            books_data = (
                {
                    'book_name': book_name,
                    'book_author': book_author,
                    'book_bublishing': book_bublishing,
                    'book_price_sale': book_price_sale,
                    'book_price_old': book_price_old,
                    'book_sale': book_sale,
                    'stock_availability': stock_availability,
                    'book_author_url': book_author_url
                }
            )

            with open(f'file_books_{current_time}.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        book_name,
                        book_author,
                        book_bublishing,
                        book_price_sale,
                        book_price_old,
                        book_sale,
                        stock_availability,
                        book_author_url

                    )
                )
                # выведим в терминал промежуточный вариант работы
        print(f'Обработана {page} / {pages_count}')
        time.sleep(1)
        # сохраняем данные в json файл
    with open(f'labirint_{current_time}.json', 'w', encoding='utf-8') as file:
        # сначало добавляем нащ список потом файл, оступ indent, и параметр ensure_ascii=False
        json.dump(books_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()
    finish_time = time.time() - start_time
    print(f'Затраченное время на запись данных - {finish_time}')


if __name__ == '__main__':
    main()
