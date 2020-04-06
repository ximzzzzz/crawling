from urllib.request import urlopen
from urllib import request
from bs4 import BeautifulSoup
import bs4
import re
import numpy as np
import requests

class kjan:
    
    def __init__(self, linkout_bs):
        self.linkout_bs = linkout_bs
    
    def get_meta_info(self, linkout_bs):
        meta_info ={}
        title = linkout_bs.find('meta', {'name' : 'citation_title'}).get('content')
        first_author = linkout_bs.find('meta',{'name' : 'citation_author'}).get('content')
        second_author = linkout_bs.find('meta',{'name' : 'citation_author'}).next.next.next.next.get('content')
        date = linkout_bs.find('meta', {'name' : 'citation_date'}).get('content')
        key_words = linkout_bs.find('meta', {'name' : 'citation_keywords'}).get('content')

        meta_info['title'] = title
        meta_info['first_author'] = first_author
        meta_info['second_author'] = second_author
        meta_info['date'] = date
        meta_info['key_words'] = key_words

        return meta_info
    
    def text_crawling(self, linkout_bs):
        text_list = []
        div_stage = linkout_bs.find('div',{'id' : 'article-level-0-body'}).div

        while bool(div_stage):
            if re.compile('\n', re.DOTALL).match(str(div_stage)):
                div_stage = div_stage.next_sibling
                continue

            for idx, div in enumerate(div_stage):

                if idx==1:
                    text_list.append('\n')
                    text_list.append(div.find('div',{'class' : 'tl-main-part'}).contents[0])

                elif not re.compile('^\n$').match(str(div)):
                    div_p = div.find_all('p')

                    if len(div_p)!=0:    
                        for p_tag in div_p:
                            if len(p_tag.contents[0])!=0:
                                text_list.append(str(p_tag.contents[0]).strip('[|]|(|)'))

                    else:
                        div_p = div.find_next('p')
                        for p_tag in div_p.contents:
                            if not re.compile('.*/.*>').match(str(p_tag)):
                                text_list.append(p_tag.strip('[|]|(|)|.| '))

            div_stage = div_stage.next_sibling

        return text_list
    

    def save_paper(self, meta_info, text_list, directory_path='papers/'):
        save_path = directory_path + (meta_info['title'])+'.txt'
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(meta_info['title']+'\n')
            f.write(meta_info['first_author']+'\n')
            f.write(meta_info['second_author'] + '\n')
            f.write(meta_info['date']+'\n')
            f.write(meta_info['key_words']+'\n')

            for i in range(len(text_list)):
                f.write(text_list[i])
                f.write('\n')
                

                
    
class jkaoh:
    def __init__(self, query_bs):
        self.query_bs = query_bs

    def get_paper(self, query_bs):
        basic_url = 'https://synapse.koreamed.org/'
        linkout_addr = query_bs.find('span',{'id' : 'ctl11_ctl01_ctl00_doia'}).select('a')[0].get('href')
        linkout_html = urlopen(linkout_addr)
        linkout_bs = BeautifulSoup(linkout_html, 'html.parser')
        pdf_link = linkout_bs.find('div', {'id': 'ArticleContentsTopIconBar'}).select('a')[2].get('href')
        pdf_link = basic_url + pdf_link

        parsed = tkparser.from_buffer(urlopen(pdf_link), xmlContent=True)
        pdf_bs = BeautifulSoup(parsed['content'], 'lxml')


        self.get_paper_index(pdf_bs)

        text_list = []
        p_tags = pdf_bs.find('body').find_all('p')
        for idx in range(self.start_idx, self.end_idx):
            text_list.append(p_tags[idx].get_text())

        self.text_list = text_list
        # return text_list


    def get_meta_info(self, pdf_bs):

        meta_info = {}
        title = pdf_bs.find('div', {'class': 'page'}).find_all('p')[1].get_text()
        author = re.compile('\d').sub('', pdf_bs.find('div', {'class': 'page'}).find_all('p')[2].get_text())
        for p_tag in pdf_bs.find('div', {'class': 'page'}).find_all('p'):
            if re.compile('.*Accepted.*').match(str(p_tag)):
                date = p_tag.get_text()

            elif re.compile('.*Key Words.*').match(str(p_tag)):
                key_words = p_tag.get_text()

        meta_info['title'] = title
        meta_info['author'] = author
        meta_info['date'] = date
        meta_info['key_words'] = key_words

        return meta_info

    def get_paper_index(self, pdf_bs):

        for idx, p_tag in enumerate(pdf_bs.find('body').find_all('p')):
            if re.compile('.*서.*론.*').match(str(p_tag)):
                start_idx = idx
                break

        for idx, p_tag in enumerate(pdf_bs.find('body').find_all('p')):
            if re.compile('.*References.*').match(str(p_tag)):
                end_idx = idx
                break

        self.start_idx = start_idx
        self.end_idx = end_idx

    def save_paper(self, directory_path='papers/'):
        save_path = directory_path + meta_info['title'] + '.txt'
        meta_info = self.get_meta_info(pdf_bs)

        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(meta_info['title'] + '\n')
            f.write(meta_info['author'] + '\n')
            f.write(meta_info['date'] + '\n')
            f.write(meta_info['key_words'] + '\n')

            for i in range(len(self.text_list)):
                f.write(text_list[i]+'\n')

class sportsmed(jkaoh):
    def __init__(self, query_bs):
        self.query_bs = query_bs

    def get_paper(self):
        self.get_title()
        linkout_addr = query_bs.find('span', {'id': 'ctl11_ctl01_ctl00_doia'}).select('a')[0].get('href')
        linkout_html = urlopen(linkout_addr)
        linkout_bs = BeautifulSoup(linkout_html, 'html.parser')

        pdf_link = linkout_bs.find('div', {'id': 'ArticleContentsTopIconBar'}).select('a')[2].get('href')
        base_url = 'https://synapse.koreamed.org/'
        pdf_link = base_url + pdf_link

        parsed = tkparser.from_buffer(urlopen(pdf_link), xmlContent=True)
        pdf_bs = BeautifulSoup(parsed['content'], 'lxml')
        super(sportsmed, self).get_paper_index()

        text_list = []
        p_tags = pdf_bs.find('body').find_all('p')
        for idx in range(self.start_idx, self.end_idx):
            text_list.append(p_tags[idx].get_text())

        self.text_list = text_list
        self.text_refining()


    def text_refining(self):
        text_refined = []
        for sentence in self.text_list:
            if len(re.compile('[가-힣]').findall(sentence)) > len(sentence) * 0.3:
                text_refined.append(sentence.replace('\n', ''))
            else:
                text_refined.append(sentence)

        text_refined2 = []
        for idx, sentence in enumerate(text_refined):
            if re.compile('다[.]').search(sentence):
                m = re.compile('다[.]').search(sentence).span()[1]
                text_refined2.append(sentence[:m] + '\n' + sentence[m:])
            else:
                text_refined2.append(sentence)

        text_refined3 = []
        for idx, sentence in enumerate(text_refined2):
            if re.compile('다[0-9][.]').search(sentence):
                m = re.compile('다[0-9][.]').search(sentence).span()[1]
                text_refined3.append(sentence[:m - 2] + sentence[m - 1] + '\n' + sentence[m:])

            elif re.compile('다[0-9]').search(sentence):
                m = re.compile('다[0-9]').search(sentence).span()[1]
                text_refined3.append(sentence[:m - 1].join('.') + '\n' + sentence[m:])
            else:
                text_refined3.append(sentence)

        self.text_refined  = text_refined3

    def get_title(self):
        title = self.query_bs.find('span', {'id' : 'ctl11_ctl01_ctl00_title_kor'}).get_text()
        self.title = title

    @override
    def save_paper(self, directory_path='papers/'):
        save_path = directory_path + self.title + '.txt'

        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(self.title + '\n')
            for i in range(len(self.text_refined)):
                f.write(self.text_refined[i])