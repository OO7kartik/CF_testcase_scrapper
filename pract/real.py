import requests as req
import bs4


res = req.get('https://codeforces.com/problemset/submission/4/2525485')

soup = bs4.BeautifulSoup(res.text, 'html.parser')
title = soup.select('title')
print(title)

file = open('main.html', 'w')
file.write(title[0].getText())




# .encode("utf-8") if we get encoding error
