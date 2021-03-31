import requests
from bs4 import BeautifulSoup
class Get_Link_k14:
    def __init__(self):
        self.link = None
    def get_link(self,url):
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')

        new = soup.find_all('div',{"class":"klw-top-news clearfix"})

        url = []
        for i in new:
            i = i.find_all("a")
            for j in i:
                url.append(j.get("href"))
        i = 0
        list_url_final = []
        while i < len(url):
            list_url_final.append(url[i])
            i += 3
        link_dau = "https://kenh14.vn"
        for i in range(0,len(list_url_final)):
            list_url_final[i] = link_dau + list_url_final[i]
        return list_url_final[0]
