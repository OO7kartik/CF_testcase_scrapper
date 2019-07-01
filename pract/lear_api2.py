import requests as req
import bs4


res = req.get('https://codeforces.com/problemset/submission/4/2525485')
# file = open('pract/main.html','w')
# file.write(res.text)
# file.close()


soup = bs4.BeautifulSoup(res.text, 'html.parser')
file = open('roundbox.html', 'w')

for mydivs in soup.find_all("div", class_ = "file input-view"):
    # # div = mydivs.find('div', class_ = "name")
    # for divs in mydivs:
    divs = mydivs.find('div', class_ = "text")
    file.write(divs.get_text() + '\n')

file.close()





# .encode("utf-8") if we get encoding error
