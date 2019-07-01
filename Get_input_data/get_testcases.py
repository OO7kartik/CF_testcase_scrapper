import requests as req
import bs4

url = 'enter the url here'

res = req.get(url)

soup = bs4.BeautifulSoup(res.text, 'html.parser')
file = open('Testcases.txt', 'w')

i = 1
for mydivs in soup.find_all("div", class_ = "file input-view"):
    divs = mydivs.find('div', class_ = "text")
    file.write("case #" + str(i) + ":" + "\n")
    file.write(divs.get_text())
    i+=1
file.close()
