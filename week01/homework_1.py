# 使用requests和bs4获取猫眼电影

import requests

from bs4 import BeautifulSoup as bs

import pandas as pd


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

header = {'Cookie':'__mta=220435111.1593175907653.1593191724978.1593192743136.3; uuid_n_v=v1; uuid=CCD4F320B7AB11EA974289B279A7041DBF96C9D5587B4A47A53DA14CED8F962F; mojo-uuid=fd0189a8fb76b40f1ec4e26b7bbbd7fa; _lxsdk_cuid=172f0af1cfec8-0181faf54fa5f3-4353760-1fa400-172f0af1cfec8; _lxsdk=CCD4F320B7AB11EA974289B279A7041DBF96C9D5587B4A47A53DA14CED8F962F; _csrf=13cb96e373c142a388e0dc41a23f92c9f45f2fcd0f596bf7d90e8d823b2d66cf; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593175908,1593191725; mojo-session-id={"id":"857d46695e75cc52517a641fa54936fc","time":1593199003161}; mojo-trace-id=3; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593200380; __mta=220435111.1593175907653.1593192743136.1593200380487.4; _lxsdk_s=172f20f832d-9e3-af8-9e9%7C%7C7',
          'user-agent':user_agent}

maoyan_url = 'https://maoyan.com/films?showType=3'

r = requests.get(maoyan_url, headers = header)

# print(r.url)

# print(f'返回码是: {r.status_code}')

movie_list = []


soup = bs(r.text, "html.parser")    # 第一个参数是要被解析的文档字符串或是文件句柄,第二个参数用来指定解析器（lxml，html.parser）

for infos in soup.find_all('div', attrs = {'class':'movie-hover-info'}, limit = 10):
    for title in infos.find_all('div', attrs = {'class':'movie-hover-title'}):
        movie_name = title.get('title')
        span = title.find('span')
        if span.text == '类型:':
            movie_type = span.find_parent('div').text.split()[-1]
        if span.text == '上映时间:':
            movie_date = span.find_parent('div').text.split()[-1]  

    #print(movie_name, movie_type, movie_date)
    movie_list.append((movie_name, movie_type, movie_date))

# print(movie_list)

df = pd.DataFrame(movie_list, columns=["电影","类型","上映日期"])
df.to_csv('maoyan_movie_10.csv',encoding='utf8',index=False)
