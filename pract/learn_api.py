import requests as req
import bs4


res = req.get('https://codeforces.com/problemset/submission/4/2525485')
# file = open('pract/main.html','w')
# file.write(res.text)
# file.close()


soup = bs4.BeautifulSoup(res.text, 'html.parser')

mydivs = soup.find_all("div", class_ = "file input-view")


file = open('roundbox.html', 'wb')


for divs in mydivs:
    file.write(divs.encode("utf-8"))




# .encode("utf-8") if we get encoding error
