import requests
import os, random
import json,time
from pypinyin import lazy_pinyin
from lxml import etree

User_agent_list = [
    "User-Agent:Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
]
user_agent = random.choice(User_agent_list)
headers = {
    "User-Agent":user_agent
}

def getMusic(url):

    rsp = requests.get(url,headers=headers)
    html = etree.HTML(rsp.text)
    #获取专辑地址部分信息列表
    href_list = html.xpath("//div[@class='content']/ul/li/div/div/a/@href")
    #print(href_list)
    for href in href_list:
        albumId = href.split("/")[-2]
        #访问专辑页并获取专辑名字和专辑页中下一页地址
        rsp = requests.get("https://www.ximalaya.com"+href+"p1", headers=headers)
        html = etree.HTML(rsp.text)
        name = html.xpath("//div[@class='info _t4_']/h1/text()")
        next_page = html.xpath("//div[@class='pagination _OO']/nav/ul/li[@class='page-next page-item _dN2']/a/@href")
        href_ = href
        # print(name)
        # print(next_page)

        #调用判断下载函数判断当前专辑的具体页数并执行相应的下载方式
        nextPage(next_page,name,albumId,href_,1)
        time.sleep(1)

def nextPage(next_page,name,albumId,href_,i):

    if len(next_page) != 0:
        #如果当前专辑有多页则先调用下载函数下载第一页
        url = "https://www.ximalaya.com/revision/play/album?albumId="+albumId+"&pageNum="+str(i)+"&sort=-1&pageSize=30"
        rsp = requests.get(url,headers=headers)
        # print(rsp.text)
        data = json.loads(rsp.text)
        # print(data)
        downlod_music(data,name)

        #下载完第一页后请求下一页，并再次进行判断
        i = i+1
        url = "https://www.ximalaya.com" + href_ + "p" + str(i)
        rsp = requests.get(url,headers=headers)
        # print(url)
        html = etree.HTML(rsp.text)
        newnext_page = html.xpath("//div[@class='pagination _OO']/nav/ul/li[@class='page-next page-item _dN2']/a/@href")
        nextPage(newnext_page,name,albumId,href_,i)

    else:
        # 如果当前专辑只有一页，则直接调用下载函数下载该页
        url = "https://www.ximalaya.com/revision/play/album?albumId=" + albumId + "&pageNum="+str(i)+"&sort=-1&pageSize=30"
        rsp = requests.get(url, headers=headers)
        # print(url)
        # print(rsp.text)
        data = json.loads(rsp.text)
        print(data)
        downlod_music(data,name)

def downlod_music(data,name):
    #专辑名称
    filename = name[0]
    #保存路径
    root_dir = "ximalaya_music/"+ filename
    #判断保存路径是否存在
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    #获取歌曲名称和下载地址信息
    titles = data['data']['tracksAudioPlay']
    for title in titles:
        #判断歌曲名称中是否含有和路径会引起冲突的字符，如果有则替换
        if '/' in title['trackName']:
            title['trackName'] = title['trackName'].replace("/","-")
        #下载文件并保存到相应位置
        try:
            rsp = requests.get(title['src'],headers=headers)
            print("正在下载"+ "-->" + title['trackName'] )
            with open(root_dir+'/'+title['trackName'],"wb") as f:
                f.write(rsp.content)
            print(title['trackName']+"-->"+"下载完成哈哈哈")
        except Exception as e:
            print("title['trackName']"+"下载失败啦啦啦啦啦啦啦")
            print(e)






def main():
    type = input("请输入您要下载的歌曲种类：")
    type = lazy_pinyin(type)
    type = "".join(type)
    page = input("请输入您要下载的页数：")
    for i in range(1,int(page)+1 ):
        url = "https://www.ximalaya.com/yinyue/" + type + '/p' + str(i)
    # url = "https://www.ximalaya.com/yinyue/" + "liuxing" + '/p1'
        getMusic(url)

if __name__ == '__main__':
    main()
