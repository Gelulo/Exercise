import requests, random,os
from lxml import etree

def getPage(url):
    User_agent_list = [
        "User-Agent:Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    ]
    user_agent = random.choice(User_agent_list)
    headers = {
        "user - agent": user_agent
    }
    rsp = requests.get(url, headers=headers)

    html = etree.HTML(rsp.text)
    return html
def getVideo(html):
    title = html.xpath("//div[@class='video-titbox']/a/span/text()")
    # print(title)
    src = html.xpath("//div[@class='video-play']/video/@src")
    video = zip(src, title)
    return video
    # for i in src:
    #     src = "https:" + i
    #     # print(src)
    #     User_agent_list = [
    #         "User-Agent:Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    #         "User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    #         "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    #     ]
    #     user_agent = random.choice(User_agent_list)
    #     headers = {
    #         "user - agent": user_agent
    #     }
    #     rsp = requests.get(src, headers=headers)
    #     video = rsp.content
    #     return video


def downlod_video(video):
    for src, title in video:
        src = "https:" + src
        # print(src)
        rsp = requests.get(src)
        filename = title +".mp4"
        # print(filename)
        root_dir = "ibaotu_video"
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)
        with open(root_dir+"/"+filename,"wb") as f:
            f.write(rsp.content)
            print(filename + "-->"+"下载成功")
def main():
    url_list = ["https://ibaotu.com/shipin/7-0-0-0-0-{}.html".format(str(i)) for i in range(1,4)]
    for url in url_list:
        html = getPage(url)
        video = getVideo(html)
        downlod_video(video)
if __name__ == '__main__':
    main()