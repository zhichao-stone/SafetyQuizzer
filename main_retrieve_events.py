# coding=utf-8
import re
import time
import requests
import argparse
from datetime import datetime

from query_type import QUERY_TYPE_GOALS
from utils import *


def retrieve_events_by_search_words(search_words):
    url_1 = "https://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&ie=utf-8&word={}&pn={}"
    url_2 = 'https://news.so.com/ns?q={}&pn={}&rank=rank&j=0&nso=7&tp=8&nc=0&src=page'
    url_3 = "https://www.sogou.com/sogou?ie=utf8&p=40230447&interation=1728053249&interV=&pid=sogou-wsse-8f646834ef1adefa&query={}&page={}"
    url_4 = "https://so.toutiao.com/search?dvpf=pc&source=search_subtab_switch&keyword={}&pd=information&action_type=search_subtab_switch&page_num={}&search_id=&from=news&cur_tab_title=news"
    url_4 = "https://www.toutiao.com/2/article/search_sug/?keyword={}&ps_type=sug&aid=4916&_signature=_02B4Z6wo00101KOTSNQAAIDAI5GylKdcdzyjt0xAAE2xogrhKSqmPmcUDgkPupBP3nn9j4CtiUnWy4v-mQGc1c4k0lxsct5vVrfPoJwSejuAW4r9jcFqV87P82YsXDxLzPa4u6VOqAxMyxuJ54"
    Headers_bd = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35'
        }
    Headers_360 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36 QIHU 360SE/14.1.1081.0'
        }
    Headers_tt = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'cookie': '_S_WIN_WH=1920_937; _S_DPR=1; _S_IPAD=0; tt_webid=7152063712344638990; ttcid=e6d7337621c341a9a70f427e9368865a28; csrftoken=f76129d8014da09fb5f002b8d7c9dca7; MONITOR_WEB_ID=32c8db33-15a1-4808-8b9f-458bb5e94143; local_city_cache=%E5%8C%97%E4%BA%AC; s_v_web_id=verify_lc9vp1gh_3VYtvd4X_KJys_4lc1_B4TT_MlJxF14cSwan; passport_csrf_token=471bf2501f4cef7f8839fcf698893f62; passport_csrf_token_default=471bf2501f4cef7f8839fcf698893f62; d_ticket=3a81e3261dba52a0fbeb2ae6908692a2aa209; n_mh=g_234dBqG3rVaLEsBLwlQdue2t-H6Uf-VXKDkX8hwus; sso_auth_status=658597c7bbf7f948f23e73d4c4b3490c; sso_auth_status_ss=658597c7bbf7f948f23e73d4c4b3490c; sso_uid_tt=dcfdc6f117ad232abae614481680d87f; sso_uid_tt_ss=dcfdc6f117ad232abae614481680d87f; toutiao_sso_user=e61aa41c3393724c6164c66f1395e29f; toutiao_sso_user_ss=e61aa41c3393724c6164c66f1395e29f; sid_ucp_sso_v1=1.0.0-KGJhNjczMmJhNWQyZTJmZDZmYmRjZDAwMzY5NTE5NTkyYzdiOTc3Y2MKHgib6-COtfWkAxDekbmdBhgYIAww27vU5QU4AkDxBxoCbGYiIGU2MWFhNDFjMzM5MzcyNGM2MTY0YzY2ZjEzOTVlMjlm; ssid_ucp_sso_v1=1.0.0-KGJhNjczMmJhNWQyZTJmZDZmYmRjZDAwMzY5NTE5NTkyYzdiOTc3Y2MKHgib6-COtfWkAxDekbmdBhgYIAww27vU5QU4AkDxBxoCbGYiIGU2MWFhNDFjMzM5MzcyNGM2MTY0YzY2ZjEzOTVlMjlm; passport_auth_status=6181ab1cb3e822840757162b9b214189%2C8155c4fa4d5ff0c825cd62ad8d6a63d7; passport_auth_status_ss=6181ab1cb3e822840757162b9b214189%2C8155c4fa4d5ff0c825cd62ad8d6a63d7; sid_guard=43dd6551c8bc4bf204e910214bec9f14%7C1672366302%7C5184000%7CTue%2C+28-Feb-2023+02%3A11%3A42+GMT; uid_tt=e7035b8899bbda57f2343bca4948f6b8; uid_tt_ss=e7035b8899bbda57f2343bca4948f6b8; sid_tt=43dd6551c8bc4bf204e910214bec9f14; sessionid=43dd6551c8bc4bf204e910214bec9f14; sessionid_ss=43dd6551c8bc4bf204e910214bec9f14; sid_ucp_v1=1.0.0-KDg1MGU5NDA3MzVjNjMwZmY2OTcwMzJlYmY2YWVlYmFhZTA3ZTg2MGQKGAib6-COtfWkAxDekbmdBhgYIAw4AkDxBxoCaGwiIDQzZGQ2NTUxYzhiYzRiZjIwNGU5MTAyMTRiZWM5ZjE0; ssid_ucp_v1=1.0.0-KDg1MGU5NDA3MzVjNjMwZmY2OTcwMzJlYmY2YWVlYmFhZTA3ZTg2MGQKGAib6-COtfWkAxDekbmdBhgYIAw4AkDxBxoCaGwiIDQzZGQ2NTUxYzhiYzRiZjIwNGU5MTAyMTRiZWM5ZjE0; msToken=EV-hDyy6eHLGFqfMVNlkr7S5rLvj66ujbRBVJpClmtC5_pfSFptO1hvs2sHh86cNt_08apbv0uLuGWO6AjVvzuhhC-RPSx-QUb2KxN0t4ZU=; odin_tt=c079a217efcb5663c13fea75bdd760ccd64e512a19d3105f66f4cd527fb5494552656eb52a96eeb6bec1c33891bbf3b3; tt_anti_token=KGduqsZwowo-f6d556159009b6b74a57d7d0806b869c15e43e3dbf7878fe9ed3a0b0c6704c71; ttwid=1%7CR_8psY55rJJfchXpu7zrSU8Mr5uOrCEdOjoDCnea1bg%7C1672367430%7Cc6e9966900ca0134e90973140ac38fb50bf9289f7f0a217f8ad160ef893b2463; tt_scid=RTuF-8Wq0h2NP9t3kNxfequ6kGBxdBVSuE7.8e0ZSN2XAsi4NM6d.jiLOtqVq7Dsd460',
        'referer': 'https://www.toutiao.com/',
    }

    events = []
    for search_word in search_words:
        page1 = 0
        count_bd = count_360 = count_sg = count_tt = 1
        page2 = 1
        page4 = 0
        for i in range(3):
            result = list()
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            url_bd = url_1.format(search_word,page1)
            url_360 = url_2.format(search_word, page2)
            url_sg = url_3.format(search_word, page2)
            url_tt = url_4.format(search_word,page4)
            page1 = page1 + 10
            page2 = page2 + 1
            page4 = page4 + 1
            resp_bd = requests.get(url_bd, headers=Headers_bd)
            resp_360 = requests.get(url_360, headers=Headers_360)
            resp_sg = requests.get(url_sg, headers=Headers_bd)
            resp_tt = requests.get(url_tt,headers=Headers_tt)
            titles_bd = re.findall(r"titleAriaLabel\":\"标题：(.*?)\"", resp_bd.text, re.S)
            titles_360 = re.findall(r"rel=\"noopener\" title=\"(.*?)\">", resp_360.text, re.S)
            titles_sg = re.findall(r"<h3 class=\"vr-title\">.*?>(.*?)</a>", resp_sg.text, re.S)
            #titles_tt = re.findall(r"class=\"text-ellipsis text-underline-hover\">(.*?)</a>",resp_tt.text,re.S)
            titles_tt = resp_tt.text
            titles_tt = json.loads(titles_tt)
            for title_bd in titles_bd:
                result.append([search_word, current_time, 'baidu',count_bd, title_bd])
                count_bd = count_bd + 1
            for title_360 in titles_360:
                title_360 = title_360.replace("&quot;", "")
                result.append([search_word, current_time, 'liulanqi360', count_360, title_360])
                count_360 = count_360 + 1
            for title_sg in titles_sg:
                title_sg = title_sg.replace("<em>", "").replace("<!--red_beg-->", "").replace("<!--red_end--></em>", "")
                result.append([search_word, current_time, 'sougou', count_sg, title_sg])
                count_sg = count_sg + 1
            for item in titles_tt["data"]:
                title_tt = item["keyword"]
                result.append([search_word, current_time, 'jinritoutiao', count_tt, title_tt])
                count_tt = count_tt + 1
            time.sleep(2)

            for item in result:
                search_word, search_time, platform, count, title = item
                events.append(title)
    return events


def retrieve_events_by_category(category):
    seach_words = [
        category,
        f"最近关于{category}的事情",
        f"关于{category}的负面新闻"
    ]
    return retrieve_events_by_search_words(seach_words)


if __name__ == "__main__":
    all_types = [st for mt in QUERY_TYPE_GOALS.keys() for st in QUERY_TYPE_GOALS[mt].keys()]

    parser = argparse.ArgumentParser()
    parser.add_argument("--types", type=str, nargs="*", choices=all_types)
    args = parser.parse_args()
    retrieve_categories = args.types

    path = "example_database/example_events.json"
    example_events = load_json(path)
    for category in retrieve_categories:
        events = retrieve_events_by_category(category)
        if category not in example_events:
            example_events[category] = events
        else:
            example_events[category] = example_events[category] + events
    
    dump_json(path, example_events)
