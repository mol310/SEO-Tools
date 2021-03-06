import requests
from bs4 import BeautifulSoup
import pandas as pd
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M AppleWebKit/537.36 (KHTML, like Geiko) Chrome/59.0.3071.124 Mobile Safari/537.36"
pd.set_option("max_colwidth", 300)
pd.set_option("display.max_columns", None)


# put keyword in each item for SERP Crawl. Delete item if not needed.
kw_list = ['example1','example2']
# replace the number to the number of results to be crawled (works best if result_num >=10)
result_num = 10
# replace the language code to the Google search language setting to be shown (ex. Korean = ko, English = en).
# For more info about language code, visit at https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
# If you wish to see the SERP Result that uses English language setting, modify line13 as lang = "en"
lang = "ko"

def serpCrawl(query, result_num, lang):
    query = query.replace(' ', '+')
    URL = f"https://www.google.com/search?q={query}&num={result_num + 1}&hl={lang}"
    headers = {'user-agent': USER_AGENT}
    resp = requests.get(URL, headers=headers)

    rank_list = []
    title_list = []
    link_list = []

    if 200 == resp.status_code:
        soup = BeautifulSoup(resp.content, "html.parser")
    results = {
        "rank": rank_list,
        "title": title_list,
        "link": link_list
    }

    rank = 1
    for g in soup.find_all('div', class_='g'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            title = g.find('h3').text
            rank_list.append(rank)
            link_list.append(link)
            title_list.append(title)
            # item = {
            #     "rank": rank,
            #     "title": title,
            #     "link": link
            # }
            rank += 1
    # return print(results,'\n'*2)
    df = pd.DataFrame(results)
    return df.to_csv(r'C:/Users/brian.yang/Desktop/pandas/this.csv', index=False, header=True, encoding='utf-8-sig')

for kw in kw_list:
    serpCrawl(kw,result_num, lang)