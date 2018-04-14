from bs4 import BeautifulSoup # importing beautiful soup to take care of the
import requests
import time
import glob

t_start = time.time()
print ('Program started ...')

book_set = set()
poet_link_set = set()
book_list = ["begin", "middle1", "middle2", "end"]
daftar_list = []
poet_name = 'first.txt'
t_poet_start = 0
t_poet_end = 0
wait = 60
mesra_counter = 0
worked_list = glob.glob("poets/*.*")
print(worked_list)
worked_list = [x[6:] for x in worked_list]
print(worked_list)


def beyt_scrapper(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, "html.parser")
    beyts_soup = soup.find_all('div', class_=('m1', 'm2'))
    if not beyts_soup:
        print("this link is not a poem, might be a daftar")
        daftar_scrapper(link)
    global book_list
    global mesra_counter
    for mesra in beyts_soup:
        book_list.append(mesra.text.replace("\u200c"," "))
        mesra_counter += 1



def daftar_scrapper(daftar_page):
    r = requests.get(daftar_page)
    soup = BeautifulSoup(r.content, "lxml")
    daftar_soup = soup.find_all('a')
    for link in daftar_soup:
        if link.has_attr('href'):
            if link['href'].startswith(daftar_page) and link['href'] != daftar_page:
                hekayat_link = link['href']
                print("parsing this page:\t"+hekayat_link)
                beyt_scrapper(hekayat_link)




def book_scrapper(book_page):
    r = requests.get(book_page)
    soup = BeautifulSoup(r.content, "lxml")
    book_soup = soup.find_all('a')
    for link in book_soup:
        if link.has_attr('href'):
            if link['href'].startswith(book_page) and link['href'] != book_page and link['href'] not in poet_link_set:
                daftar_link = link['href']
                print("parsing this daftar:\t"+daftar_link)
                daftar_scrapper(daftar_link)





def ganjoor_scrapper(ganjoor_page):
    global poet_link_set
    r = requests.get(ganjoor_page)
    soup = BeautifulSoup(r.content, "lxml")
    ganjoor_soup = soup.find_all('a')
    for link in ganjoor_soup:
        if link.has_attr('href') :
            if link['href'].startswith(ganjoor_page) and link['href'] != ganjoor_page and link['href'] not in poet_link_set:
                # defining some global variables to access from within the function
                global poet_name
                global book_list
                global book_set
                global t_poet_start
                global t_poet_end
                global wait
                global mesra_counter
                poet_link = link['href']
                temp_poet = "".join(poet_link[19:]).replace("/","").replace(".","")+".txt"
                if temp_poet in worked_list:
                    continue
                book_list.append("number of beyts:\t"+str(mesra_counter//2))
                book_list = [book_list[0]] + [book_list[-1]] +book_list[1:-2]
                with open(r"poets/"+poet_name, 'w', encoding="utf8")as bk:
                    bk.write("\n".join(book_list))
                t_poet_end = time.time()
                print('#'*50)
                print("scrapping "+poet_name[:-4]+" took {} seconds including {} sec delay.".format(t_poet_end-t_poet_start, wait))
                print('#'*50)
                print('#'*50)
                book_list = []
                book_set = set()
                poet_name = "".join(poet_link[19:]).replace("/","").replace(".","")+".txt"
                book_list.append(poet_name)
                print('*'*35)
                print("parsing this poet:\t\t"+poet_name[:-4])
                print('*'*35)
                t_poet_start = time.time()
                book_scrapper(poet_link)
                print("waiting {} second to disconnect from the server...".format(wait))
                time.sleep(wait)


        poet_link_set.update([link['href']])
        print



ganjoor_link = 'https://ganjoor.net/'
#book_link = 'https://ganjoor.net/anvari/divan-anvari/robaeea/'
#daftar_link = 'https://ganjoor.net/khayyam/robaee/'
#ghazal_link = 'https://ganjoor.net/moulavi/shams/ghazalsh/sh1787/'

ganjoor_scrapper(ganjoor_link)
#book_scrapper(book_link)
#daftar_scrapper(daftar_link)
#beyt_scrapper(ghazal_link)
print("Scraping is finished ...")
print("Outputing the book to IO ...")



print("Book is outputed ...")
t_end = time.time()
print("The whole book is scrapped within {} seconds".format(t_end-t_start))