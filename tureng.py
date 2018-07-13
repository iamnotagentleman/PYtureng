# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import frames
import sys
main_url = "http://tureng.com/tr/turkce-ingilizce/{}"
def word_crawler(word,type):
    webpage = requests.get(main_url.format(word))
    content = webpage.content
    soup = BeautifulSoup(content,"lxml")
    mytds = soup.findAll("td", {"class": "{}".format(type)})
    return mytds

def word_remaker(word_t,type):
    words = ""
    sayac = 0
    for i in word_crawler(word_t,type):
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
    word = str(word).encode("utf-8")
    word = word.decode("utf-8")
    word = word.replace("['","")
    word = word.replace("']","")
    webpage = requests.get(main_url.format(word))
    content = webpage.content
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

def writer(main_word,type):
    if type == "en tm":
        frame1 = frames.frame1_tr
    if type == "tr ts":
        frame1 = frames.frame1_en
    subject = subject_remaker(main_word) ## dict
    turkish_word = word_remaker(main_word,type).split("\n") ## turkce
    counter2 = 1
    print(frame1)
    for i in turkish_word:
        try:
            counter_sub = len(subject.get(counter2))
        except:
            break
        i = str(i).replace("</a> <i>","")
        i = i.replace(r" </i>\n</td>']","")
        i = i.replace(r' </i>\n</td>"]',"")
        i = i.replace('["',"")
        i = i.replace("i.","")
        main_word = str(main_word).replace("['","")
        main_word = main_word.replace("']","")
        a = frames.frame2.format(str(counter2)+" "*(4 -len(str(counter2))),subject.get(counter2)+(16-counter_sub)*" ",main_word,i)
        counter_a = len(a)
        a += ((82 - counter_a)*" " +"|")
        print(a)
        counter2 += 1
    print(frames.frame_last)
if __name__ == "__main__":
    if sys.argv[1:2] == ['en']:
        writer(sys.argv[2:3],"en tm")
    elif sys.argv[1:2] == ['tr']:
        writer(sys.argv[2:3],"tr ts")
