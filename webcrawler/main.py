import requests
from bs4 import BeautifulSoup

URL = "https://cryptidz.fandom.com/wiki/List_of_Cryptids"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

main_tag = soup.findAll('div',{'id':'mw-content-text'})[0]

headers = main_tag.find_all('h3')
ui_list = main_tag.find_all('ul')
for i in range(len(headers)):
    print(headers[i].span.get_text())
    print('\n -'.join(ui_list[i].get_text().split('\n')))
sections = zip((x.span.get_text() for x in headers), ('\n -'.join(x.get_text().split('\n')) for x in ui_list))
