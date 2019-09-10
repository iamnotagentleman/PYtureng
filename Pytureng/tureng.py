# -*- coding: utf-8 -*-
import re
import sys
import requests
from bs4 import BeautifulSoup
import frames
import json
import os
import logging
class Translater:
    def __init__(self,):
        self.main_url = "http://tureng.com/tr/turkce-ingilizce/{}"
        self.subject_dict = {}
        self.mytds = ""
        self.json_file_name = "data.json"
        self.json_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.json_file_name)
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
            print("Network Error, Please Check our Connection", con_Err)
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

    def history(self):
        data = [json.loads(line) for line in open(self.json_file_path, 'r')]
        for i in range(len(data)):
            print(i+1, "-)", data[i]['query_word'][0])

    def writer(self, main_word, type, is_history=False):
        write_time = 20
        counter2 = 1
        outcome_list = []
        if type == "en tm":
            frame1 = frames.frame_en
        elif type == "tr ts":
            frame1 = frames.frame_tr
        self.subject_remaker(main_word)
        print(frame1)
        for i in self.word_remaker(main_word, type).split("\n"):
            if counter2 < write_time+1:
                counter_sub = self.subject_dict.get(counter2)
                if counter_sub is not None:
                    i = i.replace("</td>", "").replace("</a> <i>i. </i>", "").replace("</a> <i> </i>", "")\
                        .replace("</a>", "").replace("<i>", "").replace("</i>", "")
                    if len(i) > 1:
                        counter_sub = len(counter_sub)
                        a = frames.frame2.format(
                            str(counter2) + " " * (4 - len(str(counter2))),
                            self.subject_dict.get(counter2) + (16 - counter_sub) * " ",
                            main_word[0],
                            i, )
                        if counter2 == 1 or counter2 == 2:
                            outcome_list.append(i)
                            outcome_list.append(self.subject_dict.get(counter2))
                        counter_a = len(a)
                        a += ((82 - counter_a) * " " + "|")
                        print(a)
                        counter2 += 1
            else:
                break
        else:
            pass
        if is_history is False:
            data = {
                'query_word': main_word,
                'query_type': type,
                'outcome_word': outcome_list[0],
                'outcome_subject': outcome_list[1],
            }
            try:
                outcome_list[2]
                outcome_list[3]
            except IndexError:
                print("")
            else:
                data["outcome_word1"] = outcome_list[2]
                data["outcome_subject1"] = outcome_list[3]
            with open(self.json_file_path, 'a', encoding="utf8") as outfile:
                if os.stat(self.json_file_path).st_size != 0:
                    outfile.write("\n")
                json.dump(data, outfile, ensure_ascii=False)
        print(frames.frame_last)


if __name__ == "__main__" or __name__ == "tureng":
    main = Translater()
    if sys.argv[1] == "tr":
        main.writer(sys.argv[2:], "en tm")
    elif sys.argv[1] == "en":
        main.writer(sys.argv[2:], "tr ts")
    elif sys.argv[1] == "history":
        try:
            sys.argv[2]
        except IndexError:
            logging.info("History Log Printing.. ")
            main.history()
        else:
            if sys.argv[2]:
                print("sysargv2")
                data = [json.loads(line) for line in open(main.json_file_path, 'r')]
                try:
                    get_query = data[int(sys.argv[2])]
                except IndexError as ixerr:
                    print(ixerr)
                else:
                    logging.info(f"Printing Translated Sentence from history {get_query['query_word']}")
                    main.writer(get_query['query_word'],
                                get_query['query_type'],
                                is_history=True,
                                )
