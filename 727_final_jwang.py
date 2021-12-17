#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/12/03 16:33
# @Author : JXWANG
# @Version：V 0.1
# @File : user_twitter.py
import datetime
import json
import random
import re
import time
import urllib

import openpyxl
import pymysql
import requests
from ODtools import RedisClient
from dateparser.search import search_dates

Introduction:
    
My Little Pony: Friendship Is Magic is a cartoon television show about friendship, compassion, and a group of magical horses who live in a fantastical land called Equestria.
It’s marketed to children. Nevertheless, it has a highly dedicated adult fandom, mostly made up of men, known as “bronies.”
There has been discussion about the political affiliation of these men as most of these men are straight-oriented, college-aged white American males.
Some point out that many of these men are vocal white supremacists, with evidence found from Twitter. However, when using the geographic information of the US bronies to map out their residence, 
one would find that their residence pattern follows the residence of Hillary supporters in the 2016 election.
A Twitter text mining and a sentiment analysis were conducted to develop a deeper understanding of the phenomenon.

Hypothesis:

Bronies are trump supporters.

Methodology:

First, scrapping 15,000 tweets of 6103 followers of @HorseNewsMLP with the keyword “Trump”, starting from 2016.
Second, conducting text cleaning, including tokenization, removing stop words, etc.
Thrid, calculating the most used words in these Trump related tweets (Top 200) and visualized the top 20 used words in these tweets.
Forth, using Textblob to analyze the polarity of the Trump related tweets



#proxies
proxies = {'http': 'socks5://127.0.0.1:10808', "https": "socks5://127.0.0.1:10808"}

#Request header
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
]

#Generate the headers of excel worksheet
wb = openpyxl.Workbook()
ws = wb.active
ws.title = 'Sheet1'
ws.append((["u_id","m_content","m_content_id","r_comment_num","g_publish_time","r_like_num","r_trans_num"]))

#Get the current time
def get_spider_time():
    g_spider_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return g_spider_time

#Format time
def get_time(a):
    a = a.replace("+0000", "")
    time_str = search_dates(a)
    times = time_str[0][-1]
    print(times, type(times))
    publish_time_end = (times + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")
    return publish_time_end

#Request parameters
def get_session():
    s = requests.session()
    s.keep_alive = False
    s.proxies = proxies
    s.allow_redirects = False
    s.verify = False
    return s


def get_html(url):
    s = get_session()
    num = 0
    while num<50:
        try:
            num += 1
            headers = {
                'Referer': 'https://twitter.com/algore',
                'Origin': 'https://twitter.com',
                'User-Agent': random.choice(user_agents),
                'x-guest-token': 1466778441425031171,
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
            }
            print("start requesting url", url)
            """{'errors': [{'code': 200, 'message': 'Forbidden.'}]},Rate limit exceeded"""
            """{'errors': [{'code': 34, 'message': 'Sorry, that page does not exist.'}]}"""
            r = s.get(url, headers=headers, proxies=proxies, timeout=20)
            res = str(r.json())
            if "Rate limit exceeded" in res or 'Forbidden' in res or "Sorry, that page does not exist" in res:
                s = get_session()
                continue
            else:
                return r
        except Exception as e:
            s = get_session()
            print(e)


def get_twitter_info(j):
    cursors = ''
    num = 0
    while num < 50:
        num += 1
        try:
            # interface
            url = 'https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&send_error_codes=true&simple_quoted_tweet=true&q=trump(from%3A{})&count=20&query_source=typed_query{}&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2CvoiceInfo%2CsuperFollowMetadata'.format(
                 j, cursors)
            res = get_html(url)
            # json
            res_dict = res.json()
            # get the lists of tweets
            if res_dict['globalObjects']['tweets']:
                # get the article of tweets
                get_twitter_article(res_dict['globalObjects'],j)
                try:
                    #get the parameters of the next page
                    if res_dict['timeline']['instructions'][0]['addEntries']['entries'][-1]:
                        page_next = res_dict['timeline']['instructions'][0]['addEntries']['entries'][-1]
                        print(page_next)
                        cursor = page_next['content']['operation']['cursor']['value']
                        print(cursor)
                        cursor = urllib.parse.quote(cursor)
                        cursors = "&cursor={}".format(cursor)
                except Exception as e:
                    print("next page parameters error", e)
                    break
            else:
                break
        except Exception as e:

            print("next page error:", e)
            break


def get_twitter_article(data,keyword):
    try:
        if data:
            for key, i in data['tweets'].items():
                print('------------------------------')
                info = {}
                # content id 
                m_content_id = i['conversation_id_str']
                info['m_content_id'] = m_content_id
                # text
                try:
                    m_content = i['full_text']
                    info['m_content'] = m_content
                except:
                    m_content = ''
                    info['m_content'] = ''
                # number of comments
                try:
                    r_comment_num = i['reply_count']
                    info['r_comment_num'] = r_comment_num
                    print(r_comment_num)
                except:
                    r_comment_num = ''
                    info['r_comment_num'] = ''
                # publish time
                try:
                    print(i['created_at'])
                    # g_publish_time = get_time(i['created_at'])
                    g_publish_time = i['created_at']
                    info['g_publish_time'] = g_publish_time
                    print(g_publish_time)
                except:
                    g_publish_time = ''
                    info['g_publish_time'] = ''
                # number of likes
                try:
                    r_like_num = i['favorite_count']
                    info['r_like_num'] = r_like_num
                    print(r_like_num)
                except:
                    r_like_num = ''
                    info['r_praised_num'] = ''
                # number of retweets
                try:
                    r_trans_num = i['retweet_count']
                    print(r_trans_num)
                    info['r_trans_num'] = r_trans_num
                except:
                    r_trans_num = ''
                    info['r_trans_num'] = ''
                # user id 
                try:
                    user_id_str = i['user_id_str']
                    info['u_id'] = user_id_str
                except:
                    user_id_str= ''
                    info['u_id'] = ''
                # scrapping time 
                g_spider_time = get_spider_time()
                info['g_spider_time'] = g_spider_time

                print(info)

                ws.append((user_id_str,m_content,m_content_id,r_comment_num,g_publish_time,r_like_num,r_trans_num))
                wb.save("diagnosedanxiety.xlsx")
                try:
                    insert_info_sql = """insert ignore twitter_info(u_id,m_content,m_content_id,r_comment_num,g_publish_time,r_like_num,r_trans_num) values (%s,%s,%s,%s,%s,%s,%s)"""
                    if info and info['m_content']:
                        return_info_result = []
                        return_info_result.append(
                            (user_id_str,m_content,m_content_id,r_comment_num,g_publish_time,r_like_num,r_trans_num)
                        )
                        cur.executemany(insert_info_sql, return_info_result)
                        conn.commit()
                        print("success")
                except Exception as e:
                    import traceback
                    traceback.print_exc()

        else:
            print("last page")
    except Exception as e:
        traceback.print_exc()
        print(e)


def time_end_start(i,start_time):
    aaa = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    threeDayAgo = (aaa + datetime.timedelta(days=i))
    threeDayAgosss = (threeDayAgo - datetime.timedelta(days=1))
    return threeDayAgo, threeDayAgosss




def run():
    # get the information of the scrapped accounts
    with open('idddddd.txt','r',encoding='utf-8') as f:
         res = f.read()
    res = res.split('\n')
    for i in res:
        get_twitter_info(i)


def get_id():
    page = ''
    while True:
        # request headers
        headers = {
            'authority': 'twitter.com',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'x-twitter-client-language': 'en',
            'x-csrf-token': '7a7fdb28f916f99b6f2336e0489659ceb918184bf200166987fa57570d741ede976fa9e3d931f6887f875d67fecf65c382f7f6f5f242d9efd23cdd7d1f2be78d38c9bcb103e0df66a6d808039c8ba654',
            'sec-ch-ua-mobile': '?0',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-active-user': 'yes',
            'sec-ch-ua-platform': '"Windows"',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://twitter.com/HorseNewsMLP/followers',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'guest_id_marketing=v1%3A163765951951409047; guest_id_ads=v1%3A163765951951409047; _ga=GA1.2.853820460.1637659531; _gid=GA1.2.477021695.1638075553; _sl=1; kdt=gfQrzLbO7gGmQN6wzRxqUmJTb4BfJOUR2bJvCOwz; lang=en; dnt=1; personalization_id="v1_+wRN+/x8COmm0x3TDBBWkg=="; guest_id=v1%3A163815106826079443; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCJcGcGl9AToMY3NyZl9p%250AZCIlODg5NjExNTA2MGM2OTIzMzYwNTk2OWVjZjk2NDAwOWE6B2lkIiVjYTRj%250AYzhkMDBjYzY1ZTY5ZDA0MzJmYjA3ZTZmZjg0Nw%253D%253D--c5fd2a9505e3ebbcb30a045dd3cfaa17830d02f5; auth_token=1c4710220ea72e2dec0b8604f514688a90f06bf4; ct0=7a7fdb28f916f99b6f2336e0489659ceb918184bf200166987fa57570d741ede976fa9e3d931f6887f875d67fecf65c382f7f6f5f242d9efd23cdd7d1f2be78d38c9bcb103e0df66a6d808039c8ba654; twid=u%3D1143712812503486465; att=1-XZEvHtox669nMCt6QbnomCGAVVC98tJgExhNDjQR',
        }
        ddd = {"userId":"2291850470","count":20,"cursor":page,"withTweetQuoteCount":0,"includePromotedContent":0,"withSuperFollowsUserFields":0,"withUserResults":0,"withBirdwatchPivots":0,"withDownvotePerspective":0,"withReactionsMetadata":0,"withReactionsPerspective":0,"withSuperFollowsTweetFields":1}
        ddd = json.dumps(ddd)
        params = (
            ('variables',ddd),
        )
        # request

        response = requests.get('https://twitter.com/i/api/graphql/TQzc7juZfthVhwg-5WUbeg/Followers', headers=headers,
                                params=params, proxies=proxies)

        res = response.json()
        # regex match user id, store in excel
        id = re.findall(r"'screen_name': '(.*?)', '",str(res),re.S)
        print(id)
        page = re.findall(r"'value': '(.*?)', 'cursorType'",str(res),re.S)[0]
        print("page",page)
        for j in id:
            with open('idddddd.txt','a',encoding='utf-8') as f:
                f.write(j+"\n")
                print(j)

if __name__ == '__main__':
    # get the information of the followers 
    get_id()
    # get the informatio of the posts of the followers
    run()

    import pandas as pd
    from nltk.tokenize import word_tokenize
    from textblob import TextBlob
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud

    # text cleaning，tokenization, remove stopwords, calculate the frequency of the words used. 
    df = pd.read_excel('twitter_1130.xlsx')
    df['m_content'] = df['m_content'].astype('str')
    data = df['m_content']
    # tokenization
    data1 = []
    for i in data:
        try:
            text_cut = word_tokenize(i)  
            data1.extend(text_cut)
        except:
            data1.append(i)


    # remove stopwords.
    def stopwordslist(filepath):
        stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
        return stopwords


    stop = stopwordslist('stopword.txt')


    def is_number(string):
        if string.endswith('%'):  
            string = string.replace('%', '')
        try:
            if string == 'NaN':
                return False
            float(string)
            return True
        except ValueError:
            return False


    data2 = []
    for i in data1:
        i = str(i).lower()
        if i not in stop:
            if is_number(i) == False:
                try:
                    data2.append(i)
                except:
                    print(i)
    # calculate the frequency of the words used
    import collections

    word_counts = collections.Counter(data2)
    word_counts_top200 = word_counts.most_common(200)
    name1 = []
    for i in word_counts_top200:
        name1.append(i[0])
    frequency = []
    for i in word_counts_top200:
        frequency.append(i[1])
    dict_ = {
        'Words': name1,
        'frequency': frequency
    }
    df_200 = pd.DataFrame(dict_)
    df_200.to_excel('200.xlsx')
    s = pd.read_excel('1.xlsx')
    s = s['Words'].tolist()
    df_screen = df_200[~df_200['Words'].isin(s)]
    df_screen = df_screen.sort_values('frequency')
    df_screen.index = range(len(df_screen))

    # use matplotlib to draw a most used words frequency distribution bar plot
    plt.figure(figsize=(12, 12))
    plt.barh(list(range(len(df_screen20))), df_screen20['frequency'], label="Example one")
    plt.xlabel('bar number', fontsize=15)
    plt.ylabel('Most used words', fontsize=15)
    plt.yticks(list(range(len(df_screen20))), df_screen20['Words'].tolist(), fontsize=12)
    plt.title('frequency distribution', fontsize=20)
    plt.savefig('1.png', pci=500)
    plt.show()


    # sentiment analysis
    def Score(data):
        fraction = TextBlob(data['m_content']).sentiment[0]
        return fraction


    df['Emotion_score'] = df.apply(Score, axis=1)


    def Score1(data):
        data = data['Emotion_score']
        if data < 0:
            return 'negative'
        elif data > 0:
            return 'positive'
        else:
            return 'neutral'


    df['Emotional_polarity'] = df.apply(Score1, axis=1)
    del df['Emotion_score']
    df.to_excel('arrangement.xlsx')
    # use matplotlib to draw a bar plot of the emotional polarity of the trump related tweets.
    plt.figure(figsize=(12, 8))
    plt.bar(list(range(3)), df.groupby('Emotional_polarity').agg('size').values.tolist(), width=0.5)
    plt.xlabel('Emotion classification of Brony tweets', fontsize=15)
    plt.ylabel('Number of tweets', fontsize=15)
    plt.xticks(list(range(3)), df.groupby('Emotional_polarity').agg('size').index.tolist(), fontsize=12)
    plt.title('Emotional polarity', fontsize=22)
    plt.savefig('2.png', pci=500)  # save the pic
    

Discussion:
    
There is no evidence to prove bronies are mostly trump supporters. When looking at the most used words of these tweets, 
one would find that most of the words are negative. In particular, the word "supporters" "support" "supporter" appear a lot in these tweets.
The takeaway here is that trump supporters dont use the word "supporter" to address themselves, so chances are that these tweets are not posted by 
trump suppoeters. Although the sentiment analysis shows that more rrump related tweeets are positive, it may be the result of an inaccurate sentiment analysis.
A supervised text classification might be a better way to analyze the sentiment of these trump related tweets.