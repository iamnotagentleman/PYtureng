# -*- coding: utf-8 -*-
import re
import sys

import requests
from bs4 import BeautifulSoup
import frames






class Translater:

    def __init__(self):
        self.main_url = "http://tureng.com/tr/turkce-ingilizce/{}"
        self.subject_dict = {}
        self.mytds = ""

    def word_crawler(self, word, type):
        webpage = requests.get(self.main_url.format(word))
        content = webpage.content
        soup = BeautifulSoup(content, "lxml")
        self.mytds = soup.findAll("td", {"class": "{}".format(type)})

    def word_remaker(self, word_t, type):
        words = ""
        sayac = 0
        self.word_crawler(word_t, type)
        for i in self.mytds:
            if sayac != 1:
                td_finder = re.sub("^<td{}".format("." * 54), " ", str(i))
                td_finder = re.sub("</a> </td>$", " ", str(td_finder))
                td_finder = td_finder.split('">')
                words += "".join(str(td_finder[1:]) + "\n")
                words = words.replace(" ']", "")
                words = words.replace("['", "")
            else:
                break
        return words

    def subject_crawler(self, word):
        word = str(word).encode("utf-8")
        word = word.decode("utf-8")
        word = word.replace("['", "")
        word = word.replace("']", "")
        try:
            webpage = requests.get(self.main_url.format(word))
        except requests.exceptions.ConnectionError:
            print("Network Error, Please Check our Connection")
            sys.exit()
        content = webpage.content
        soup = BeautifulSoup(content, "lxml")
        self.mytds = soup.findAll("td", {"class": "hidden-xs"})

    def subject_remaker(self, word_t):
        pool = ""
        counter = 1
        self.subject_crawler(word_t)
        for i in self.mytds:
            i = str(i)
            i = i.replace('<td class="rc0 hidden-xs">1</td>', "")
            i = i.replace(
                '<td class="rc4 hidden-xs"><span class="glyphicon glyphicon-option-horizontal"></span></td>', "")
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
                self.subject_dict.update({counter: i})
                counter += 1

    def writer(self, main_word, type):
        frame1 = None
        write_time = 20
        counter2 = 1
        if type == "en tm":
            frame1 = frames.frame1_tr
        elif type == "tr ts":
            frame1 = frames.frame1_en
        if counter2 > write_time:
            sys.exit()
        self.subject_remaker(main_word)
        print(frame1)
        for i in self.word_remaker(main_word, type).split("\n"):
            counter_sub = self.subject_dict.get(counter2)
            if counter_sub is not None:
                counter_sub = len(counter_sub)
                i = str(i).replace("</a> <i>", "")
                i = i.replace(r" </i>\n</td>']", "")
                i = i.replace(r' </i>\n</td>"]', "")
                i = i.replace('["', "")
                i = i.replace("i.", "")
                main_word = str(main_word).replace("['", "")
                main_word = main_word.replace("']", "")
                a = frames.frame2.format(
                    str(counter2) + " " * (4 - len(str(counter2))),
                    self.subject_dict.get(counter2) + (16 - counter_sub) * " ",
                    main_word,
                    i, )
                counter_a = len(a)
                a += ((82 - counter_a) * " " + "|")
                print(a)
                counter2 += 1
        else:
            pass
        print(frames.frame_last)


if __name__ == "__main__" or "tureng":
    main = Translater()
    if sys.argv[1:2] == ['en']:
        main.writer(sys.argv[2:], "en tm")
    elif sys.argv[1:2] == ['tr']:
        main.writer(sys.argv[2:], "tr ts")