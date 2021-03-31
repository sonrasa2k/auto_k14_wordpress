from find_content import Get_Link_k14
import requests
from bs4 import BeautifulSoup
new = Get_Link_k14()
list_url = new.get_link()
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8',
}
kq = BeautifulSoup(requests.get(list_url[0],headers=headers).text,"html.parser")
title = kq.find_all("h1",{"class":"kbwc-title"})
title = title[0].get_text()
content = kq.find_all("div",{"class":["knc-content"]})

#print(content[0].get_text())


# list_content = ""
# h2 = kq.find_all("h2",{"class":"knc-sapo"})
# for i in h2:
#     list_content += i.get_text()
# for i in content:
#     a = i.get_text().strip()
#     list_content += a
# list_content = list_content.strip("\n")
# list_content = list_content.split("Nguồn")
# final_content = list_content[0]
# nguon = "\nNguồn: Kenh 14"
# print(final_content+nguon)
#
#
# img = kq.find_all("div",{"class":"VCSortableInPreviewMode"})
# print(img)
# for i in img:
#     print(i.find_all("img"))


from autoup import AutoUp

from tkinter import filedialog
import tkinter as tk

root = tk.Tk()
root.title("Auto Dang Bai")

# setting the windows size
root.geometry("600x400")
def submit():
    global username
    global passwd
    username = username.get()
    passwd = passwd.get()
    if username == "" or passwd =="":
        username = "honghue"
        passwd = "honghue12t@gmail.com"
    new = AutoUp()
    new.login("https://vnshowbiz.net/wp-admin/",username,passwd)
    new.Auto_UpPost("https://vnshowbiz.net/wp-admin/post-new.php",title,content[0].get_text())

username= tk.StringVar()
passwd = tk.StringVar()
label1 = tk.Label(root, text='Username', font=('calibre', 10, 'bold'))
label2 = tk.Label(root, text='Password', font=('calibre', 10, 'bold'))
user = tk.Entry(root, textvariable=username, font=('calibre', 10, 'normal'))
passwd = tk.Entry(root, textvariable=passwd, font=('calibre', 10, 'normal'))
button = tk.Button(root, text='Submit', command=submit)

label1.grid(row=0,column =0)
user.grid(row=0,column =1)

label2.grid(row =1 , column = 0 )
passwd.grid(row=1,column =1 )
button.grid(row = 2,column = 0)
root.mainloop()

# print(list_url)
# for link in list_url:
#     kq = requests.get(link)
#     soup = BeautifulSoup(kq.text, 'html.parser')
#     print(soup)