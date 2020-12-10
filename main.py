import urllib.request
import time
import requests, bs4

def download_file(url, destination):
    # скачиваем файл
    start_time = time.time()

    # устанавливаем заголовок, иначе очень долго качает
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, destination)

    print("--- %s seconds ---" % (time.time() - start_time))

    pass

def open_page(url_prefix):
    # страница с сылками на аудио -- сюда прилетают айдишники
    page_prefix = 'https://dlc.library.columbia.edu/catalog/cul:'
    base_url = page_prefix + url_prefix

    headers = {'accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
    session = requests.Session()
    s1 = session.get(base_url, headers=headers)
    bsoup = bs4.BeautifulSoup(s1.text, 'html.parser')

    # получаем название заголовка и переделываем его под название файла
    file_prefix = bsoup.title.text.split('with ')[1].split(' - ')[0].replace(' ','_')
    print(file_prefix)
    blocks = bsoup('img')

    for index,it in enumerate(blocks, start=1):
        # получаем ссылки на файлы
        ids = it.get('src').split(':')[2].split('/')[0]
        file = f'https://dlc.library.columbia.edu/catalog/cul:{ids}/bytestreams/access/content?download=true'
        dest = file_prefix + '_' + str(index) + '.m4a'
        print(ids)
        print(file)
        print('file rename ', dest)
        download_file(file, dest)
    pass


base_url = 'https://dlc.library.columbia.edu/catalog?f%5Blanguage_language_term_text_ssim%5D%5B%5D=Russian&f%5Blib_collection_sim%5D%5B%5D=Radio+Liberty+project&per_page=100&q=radio+liberty+oral+history&search_field=all_text_teim'
headers = {'accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'}
session = requests.Session()
s0 = session.get(base_url, headers=headers)

bsoup = bs4.BeautifulSoup(s0.text, 'html.parser')
blocks = bsoup('a')

ids = []

for it in blocks:
    link = it.get('data-context-href')
    if link is not None:
        ids.append(link.split(':')[1].split('/')[0])

# удаляем дубликаты
ids = set(ids)
print(ids)
print('Количество ссылок на воспоминания', len(ids))

# открываем и скачиваем
for it in ids:
    print(f'Качаем страницу id --- {id}')
    open_page(it)



