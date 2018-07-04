import  urllib.request
from bs4 import BeautifulSoup
import re
import frames
import sys
main_url = "http://tureng.com/tr/turkce-ingilizce/{}"
def word_crawler(word):
    webpage = urllib.request.urlopen(main_url.format(word))
    content = webpage.read()
    soup = BeautifulSoup(content,"lxml")
    mytds = soup.findAll("td", {"class": "tr ts"})
    return mytds

def word_remaker(word_t):
    words = ""
    sayac = 0
    for i in word_crawler(word_t):
        if sayac != 1:
            td_finder = re.sub("^<td{}".format("."*54)," ",str(i))
            td_finder = re.sub("</a> </td>$"," ", str(td_finder))
            td_finder = td_finder.split('">')
            words += "".join(str(td_finder[1:])+"\n")
            words = words.replace(" ']" ,"")
            words = words.replace("['", "")
        else:
            break
    return words

def subject_crawler(word):
    webpage = urllib.request.urlopen(main_url.format(word))
    content = webpage.read()
    soup = BeautifulSoup(content, "lxml")
    mytds = soup.findAll("td", {"class": "hidden-xs"})
    return mytds

def subject_remaker(word_t):
    subejct_dict = {}
    pool = ""
    counter = 1
    for i in subject_crawler(word_t):
        i = str(i)
        i = i.replace('<td class="rc0 hidden-xs">1</td>', "")
        i = i.replace('<td class="rc4 hidden-xs"><span class="glyphicon glyphicon-option-horizontal"></span></td>', "")
        i = i.replace('<td class="rc0 hidden-xs">', "")
        i = i.replace("</td>", "")
        try:
            i = int(i)
            i = ""
        except:
            i = i
        i = i.replace('<td class="hidden-xs">', "")
        i = i + ","
        pool += i
        pool = pool.replace(",,,", ",")
        pool = pool.replace(",,", ",")
        if pool.startswith(","):
            pool = "" + pool[1:]
    pool = pool.split(",")
    for i in pool:
        if i != "":
            subejct_dict.update({counter:i})
            counter += 1
    return subejct_dict

def printer(main_word):
    frame2="| {}"
    subject = subject_remaker(main_word) ## dict
    turkish_word = word_remaker(main_word).split("\n") ## türkce
    sayac2 = 1
    print(frames.frame1)
    for i in turkish_word:
        try:
            counter_sub = len(subject.get(sayac2))
        except:
            break
        a = frames.frame2.format(str(sayac2)+" "*(4 -len(str(sayac2))),subject.get(sayac2)+(16-counter_sub)*" ",main_word,i)
        counter_a = len(a)
        a += ((82 - counter_a)*" " +"|")
        print(a)
        sayac2 += 1
    print(frames.frame_last)
if __name__ == "__main__":
    if sys.argv[1:2] == ['en']:
        printer(sys.argv[2:3])
