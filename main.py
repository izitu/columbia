import urllib.request
import time




# скачиваем файл
start_time = time.time()

destination = '1.m4a'
url = 'https://dlc.library.columbia.edu/catalog/cul:xgxd254971/bytestreams/access/content?download=true'

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')] # устанавливаем заголовок, иначе очень долго качает
urllib.request.install_opener(opener)
urllib.request.urlretrieve(url, destination)

print("--- %s seconds ---" % (time.time() - start_time))