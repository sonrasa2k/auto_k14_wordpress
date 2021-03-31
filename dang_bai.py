import re
import time
import random
import win32clipboard


from find_content import Get_Link_k14
import requests
from bs4 import BeautifulSoup
from autoup import AutoUp
from tkinter import filedialog
import tkinter as tk
#---------------------------------------------------------------------------
#  Convenience functions to do the most common operation

def HasHtml():
    """
    Return True if there is a Html fragment in the clipboard..
    """
    cb = HtmlClipboard()
    return cb.HasHtmlFormat()


def GetHtml():
    """
    Return the Html fragment from the clipboard or None if there is no Html in the clipboard.
    """
    cb = HtmlClipboard()
    if cb.HasHtmlFormat():
        return cb.GetFragment()
    else:
        return None


def PutHtml(fragment):
    """
    Put the given fragment into the clipboard.
    Convenience function to do the most common operation
    """
    cb = HtmlClipboard()
    cb.PutFragment(fragment)


#---------------------------------------------------------------------------

class HtmlClipboard:

    CF_HTML = None

    MARKER_BLOCK_OUTPUT = \
        "Version:1.0\r\n" \
        "StartHTML:%09d\r\n" \
        "EndHTML:%09d\r\n" \
        "StartFragment:%09d\r\n" \
        "EndFragment:%09d\r\n" \
        "StartSelection:%09d\r\n" \
        "EndSelection:%09d\r\n" \
        "SourceURL:%s\r\n"

    MARKER_BLOCK_EX = \
        "Version:(\S+)\s+" \
        "StartHTML:(\d+)\s+" \
        "EndHTML:(\d+)\s+" \
        "StartFragment:(\d+)\s+" \
        "EndFragment:(\d+)\s+" \
        "StartSelection:(\d+)\s+" \
        "EndSelection:(\d+)\s+" \
        "SourceURL:(\S+)"
    MARKER_BLOCK_EX_RE = re.compile(MARKER_BLOCK_EX)

    MARKER_BLOCK = \
        "Version:(\S+)\s+" \
        "StartHTML:(\d+)\s+" \
        "EndHTML:(\d+)\s+" \
        "StartFragment:(\d+)\s+" \
        "EndFragment:(\d+)\s+" \
           "SourceURL:(\S+)"
    MARKER_BLOCK_RE = re.compile(MARKER_BLOCK)

    DEFAULT_HTML_BODY = \
        "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">" \
        "<HTML><HEAD></HEAD><BODY><!--StartFragment-->%s<!--EndFragment--></BODY></HTML>"

    def __init__(self):
        self.html = None
        self.fragment = None
        self.selection = None
        self.source = None
        self.htmlClipboardVersion = None


    def GetCfHtml(self):
        """
        Return the FORMATID of the HTML format
        """
        if self.CF_HTML is None:
            self.CF_HTML = win32clipboard.RegisterClipboardFormat("HTML Format")

        return self.CF_HTML


    def GetAvailableFormats(self):
        """
        Return a possibly empty list of formats available on the clipboard
        """
        formats = []
        try:
            win32clipboard.OpenClipboard(0)
            cf = win32clipboard.EnumClipboardFormats(0)
            while (cf != 0):
                formats.append(cf)
                cf = win32clipboard.EnumClipboardFormats(cf)
        finally:
            win32clipboard.CloseClipboard()

        return formats


    def HasHtmlFormat(self):
        """
        Return a boolean indicating if the clipboard has data in HTML format
        """
        return (self.GetCfHtml() in self.GetAvailableFormats())


    def GetFromClipboard(self):
        """
        Read and decode the HTML from the clipboard
        """

        # implement fix from: http://teachthe.net/?p=1137

        cbOpened = False
        while not cbOpened:
            try:
                win32clipboard.OpenClipboard(0)
                src = win32clipboard.GetClipboardData(self.GetCfHtml())
                src = src.decode("UTF-8")
                #print(src)
                self.DecodeClipboardSource(src)

                cbOpened = True

                win32clipboard.CloseClipboard()
            except Exception as err:
                # If access is denied, that means that the clipboard is in use.
                # Keep trying until it's available.
                if err.winerror == 5:  # Access Denied
                    pass
                    # wait on clipboard because something else has it. we're waiting a
                    # random amount of time before we try again so we don't collide again
                    time.sleep( random.random()/50 )
                elif err.winerror == 1418:  # doesn't have board open
                    pass
                elif err.winerror == 0:  # open failure
                    pass
                else:
                    print( 'ERROR in Clipboard section of readcomments: %s' % err)

                    pass

    def DecodeClipboardSource(self, src):
        """
        Decode the given string to figure out the details of the HTML that's on the string
        """
        # Try the extended format first (which has an explicit selection)
        matches = self.MARKER_BLOCK_EX_RE.match(src)
        if matches:
            self.prefix = matches.group(0)
            self.htmlClipboardVersion = matches.group(1)
            self.html = src[int(matches.group(2)):int(matches.group(3))]
            self.fragment = src[int(matches.group(4)):int(matches.group(5))]
            self.selection = src[int(matches.group(6)):int(matches.group(7))]
            self.source = matches.group(8)
        else:
            # Failing that, try the version without a selection
            matches = self.MARKER_BLOCK_RE.match(src)
            if matches:
                self.prefix = matches.group(0)
                self.htmlClipboardVersion = matches.group(1)
                self.html = src[int(matches.group(2)):int(matches.group(3))]
                self.fragment = src[int(matches.group(4)):int(matches.group(5))]
                self.source = matches.group(6)
                self.selection = self.fragment


    def GetHtml(self, refresh=False):
        """
        Return the entire Html document
        """
        if not self.html or refresh:
            self.GetFromClipboard()
        return self.html


    def GetFragment(self, refresh=False):
        """
        Return the Html fragment. A fragment is well-formated HTML enclosing the selected text
        """
        if not self.fragment or refresh:
            self.GetFromClipboard()
        return self.fragment


    def GetSelection(self, refresh=False):
        """
        Return the part of the HTML that was selected. It might not be well-formed.
        """
        if not self.selection or refresh:
            self.GetFromClipboard()
        return self.selection


    def GetSource(self, refresh=False):
        """
        Return the URL of the source of this HTML
        """
        if not self.selection or refresh:
            self.GetFromClipboard()
        return self.source


    def PutFragment(self, fragment, selection=None, html=None, source=None):
        """
        Put the given well-formed fragment of Html into the clipboard.
        selection, if given, must be a literal string within fragment.
        html, if given, must be a well-formed Html document that textually
        contains fragment and its required markers.
        """
        if selection is None:
            selection = fragment
        if html is None:
            html = self.DEFAULT_HTML_BODY % fragment
        if source is None:
            source = "file://HtmlClipboard.py"

        fragmentStart = html.index(fragment)
        fragmentEnd = fragmentStart + len(fragment)
        selectionStart = html.index(selection)
        selectionEnd = selectionStart + len(selection)
        self.PutToClipboard(html, fragmentStart, fragmentEnd, selectionStart, selectionEnd, source)


    def PutToClipboard(self, html, fragmentStart, fragmentEnd, selectionStart, selectionEnd, source="None"):
        """
        Replace the Clipboard contents with the given html information.
        """

        try:
            win32clipboard.OpenClipboard(0)
            win32clipboard.EmptyClipboard()
            src = self.EncodeClipboardSource(html, fragmentStart, fragmentEnd, selectionStart, selectionEnd, source)
            src = src.encode("UTF-8")
            #print(src)
            win32clipboard.SetClipboardData(self.GetCfHtml(), src)
        finally:
            win32clipboard.CloseClipboard()


    def EncodeClipboardSource(self, html, fragmentStart, fragmentEnd, selectionStart, selectionEnd, source):
        """
        Join all our bits of information into a string formatted as per the HTML format specs.
        """
        # How long is the prefix going to be?
        dummyPrefix = self.MARKER_BLOCK_OUTPUT % (0, 0, 0, 0, 0, 0, source)
        lenPrefix = len(dummyPrefix)

        prefix = self.MARKER_BLOCK_OUTPUT % (lenPrefix, len(html)+lenPrefix,
                        fragmentStart+lenPrefix, fragmentEnd+lenPrefix,
                        selectionStart+lenPrefix, selectionEnd+lenPrefix,
                        source)
        return (prefix + html)


def DumpHtml():

    cb = HtmlClipboard()
    print("GetAvailableFormats()=%s" % str(cb.GetAvailableFormats()))
    print("HasHtmlFormat()=%s" % str(cb.HasHtmlFormat()))
    if cb.HasHtmlFormat():
        cb.GetFromClipboard()
        print("prefix=>>>%s<<<END" % cb.prefix)
        print("htmlClipboardVersion=>>>%s<<<END" % cb.htmlClipboardVersion)
        print("GetSelection()=>>>%s<<<END" % cb.GetSelection())
        print("GetFragment()=>>>%s<<<END" % cb.GetFragment())
        print("GetHtml()=>>>%s<<<END" % cb.GetHtml())
        print("GetSource()=>>>%s<<<END" % cb.GetSource())

def get_file_link():
    new = Get_Link_k14()
    url1 = new.get_link('https://kenh14.vn/star/sao-viet.chn')
    url2 = new.get_link('https://kenh14.vn/star.chn')
    url3 = new.get_link('https://kenh14.vn/star/hoi-ban-than-showbiz.chn')
    with open("data.txt","w+",encoding="utf-8") as f:
        f.write(str(url1)+"\n")
        f.write(str(url2) + "\n")
        f.write(str(url3) + "\n")
    f.close()
    return "get file data link thanh cong"

def get_content(url):
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
    kq = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
    title = kq.find_all("h1", {"class": "kbwc-title"})
    title = title[0].get_text()
    title2 = kq.find_all("h2", {"class": "knc-sapo"})[0]
    content = kq.find_all("div", {"class": ["knc-content"]})[0]
    content.insert(0,title2)
    return (title,content)
def upload_wp(title,content,username,passwd):
    PutHtml(str(content))
    new = AutoUp()
    new.login("https://vnshowbiz.net/wp-admin/", username, passwd)
    new.Auto_UpPost("https://vnshowbiz.net/wp-admin/post-new.php", title, GetHtml())
    return "Dang bai thanh cong ♥"

root = tk.Tk()
root.title("Auto Dang Bai")

# setting the windows size
root.geometry("600x400")

username = tk.StringVar()
passwd = tk.StringVar()


def submit():
    global username
    global passwd
    username = username.get()
    passwd = passwd.get()
    if username == "" or passwd == "":
        username = "honghue"
        passwd = "honghue12t@gmail.com"
    while True:
        new = Get_Link_k14()
        url1 = new.get_link('https://kenh14.vn/star/sao-viet.chn')
        url2 = new.get_link('https://kenh14.vn/star.chn')
        url3 = new.get_link('https://kenh14.vn/star/hoi-ban-than-showbiz.chn')
        list_url_true = []
        with open("data.txt",'r',encoding="utf-8") as f:
            data = f.readlines()
            if str(data[0]).strip() != str(url1):
                list_url_true.append(url1)
            if str(data[1]).strip() != str(url2):
                list_url_true.append(url2)
            if str(data[2]).strip() != str(url3):
                list_url_true.append(url3)
        if len(list_url_true) == 0:
            print("Chua co post moi , tool se dung trong 5p")
            time.sleep(300)
        else:
            list_url_true = list(set(list_url_true))
            print(list_url_true)
            for i in list_url_true:
                title,content = get_content(i)
                print(upload_wp(title,content,username,passwd))
                time.sleep(5)
            print(get_file_link())
            time.sleep(300)
label1 = tk.Label(root, text='Username', font=('calibre', 10, 'bold'))
label2 = tk.Label(root, text='Password', font=('calibre', 10, 'bold'))
user = tk.Entry(root, textvariable=username, font=('calibre', 10, 'normal'))
passwd = tk.Entry(root, textvariable=passwd, font=('calibre', 10, 'normal'))
button = tk.Button(root, text='Submit', command=submit)

label1.grid(row=0, column=0)
user.grid(row=0, column=1)

label2.grid(row=1, column=0)
passwd.grid(row=1, column=1)
button.grid(row=2, column=0)
root.mainloop()