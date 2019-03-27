"""
https://www.kugou.com/yy/rank/home/1-8888.html?from=homepage

"""

import requests, random, time, csv
from bs4 import BeautifulSoup

def get_kg(url):
    User_agent_list = [
        "User-Agent:Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    ]
    user_agent = random.choice(User_agent_list)
    headers = {
        "user - agent":user_agent
    }


    rsp = requests.get(url,headers=headers)
    soup = BeautifulSoup(rsp.text,'lxml')
    nums = soup.select('.pc_temp_num')
    titles = soup.select('.pc_temp_songname')
    times = soup.select('.pc_temp_time')
    for num,title,time_ in zip(nums,titles,times):
        num = num.get_text().strip()
        song = title.get_text().split('-')[-1].strip()
        songer = title.get_text().split('-')[0].strip()
        song_url = title.get('href')
        time_ = time_.get_text().strip()
        print(num+"--"+song+"--"+songer+"--"+time_+"--"+song_url)
        try:
            writer.writerow((num,song,songer,time_,song_url))
        except Exception as e:
            print("写入失败")
            print(e)
        time.sleep(1)


if __name__ == '__main__':
    url_list = ["https://www.kugou.com/yy/rank/home/{0}-8888.html?from=homepage".format(str(i)) for i in range(1,24)]
    csvfile = open("kg_top500.csv","a")
    writer = csv.writer(csvfile)
    writer.writerow(('排名','歌曲名称','歌手','时间','播放地址'))
    for url in url_list:
       get_kg(url)