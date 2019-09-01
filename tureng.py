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
        webpage = requests.get(self.main_url.format(word[0]))
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
                words += "".join(str(td_finder[1]) + "\n")
            else:
                break
        return words

    def subject_crawler(self, word):
        try:
            webpage = requests.get(self.main_url.format(word[0]))
        except requests.exceptions.ConnectionError as con_Err:
            print("Network Error, Please Check our Connection", con_Err  )
            sys.exit()
        content = webpage.content
        soup = BeautifulSoup(content, "lxml")
        self.mytds = soup.findAll("td", {"class": "hidden-xs"})

    def subject_remaker(self, word_t):
        pool = []
        counter = 0
        self.subject_crawler(word_t)
        for i in self.mytds:
            i = i.get_text()
            if len(i) >= 4:
                pool.append(i)
                counter += 1
                self.subject_dict.update({counter: i})

    def writer(self, main_word, type):
        print(type)
        if type == "en tm":
            frame1 = frames.frame_en
        elif type == "tr ts":
            frame1 = frames.frame_tr
        write_time = 20
        counter2 = 1
        self.subject_remaker(main_word)
        print(frame1)
        for i in self.word_remaker(main_word, type).split("\n"):
            if counter2 < write_time:
                counter_sub = self.subject_dict.get(counter2)
                if counter_sub is not None:
                    counter_sub = len(counter_sub)
                    a = frames.frame2.format(
                        str(counter2) + " " * (4 - len(str(counter2))),
                        self.subject_dict.get(counter2) + (16 - counter_sub) * " ",
                        main_word[0],
                        i, )
                    counter_a = len(a)
                    a += ((82 - counter_a) * " " + "|")
                    print(a)
                    counter2 += 1
            else:
                break
        else:
            pass
        print(frames.frame_last)


if __name__ == "__main__" or __name__ == "tureng":
    main = Translater()
    if sys.argv[1:2] == ['tr']:
        main.writer(sys.argv[2:], "en tm")
    elif sys.argv[1:2] == ['en']:
        main.writer(sys.argv[2:], "tr ts")
