import requests as req
import bs4


res = req.get('https://codeforces.com/problemset/submission/4/2525485')

soup = bs4.BeautifulSoup(res.text, 'html.parser')
file = open('main_code.html', 'wb') # note should be opened in binary mode
file.write(soup.encode("utf-8"))




# .encode("utf-8") if we get encoding error
