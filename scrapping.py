from bs4 import BeautifulSoup
import requests
import time

t_start = time.time()

def beyt_scrapper(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    beyts_soup = soup.find_all('div', class_=('m1', 'm2'))
    global book_list
    for mesra in beyts_soup:
        book_list.append(mesra.text)



book_list = []
book_page = 'http://www.nosokhan.com/Library/Part/0NV'
r = requests.get(book_page)
soup = BeautifulSoup(r.content, "html.parser")
ghazal_soup = soup.find_all('a')
i = 0
temp = []
for mesra in ghazal_soup:
    if mesra.has_attr('href'):
        if mesra['href'][-10:-5] == 'Topic':
            ghazal_link = 'http://www.nosokhan.com'+mesra['href']
            temp.append(ghazal_link)
            beyt_scrapper(ghazal_link)


with open('book.txt', 'w', encoding="utf8")as bk:
    bk.write("\n".join(book_list))

t_end = time.time()
print("The whole book is scrapped within {} seconds".format(t_end-t_start))