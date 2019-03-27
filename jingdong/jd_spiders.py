from selenium import webdriver
import pymongo
#expected conditions 负责条件的发起，触发
from selenium.webdriver.support import expected_conditions as EC
"""
selenium主要提供隐性等待和显示等待
driver:传入webdriver的实例
 timeout：超时时间，等待的最长时间（考虑隐性等待时间）
 poll_frequency=POLL_FREQUENCY:调用until或者until_not中的方法的时间间隔，默认：0.5秒
  ignored_exceptions=None：忽略异常，如果在调用until或者until_not的过程中抛出元组中的异常，则不中断代码，继续等待
                                    如果抛出的是元组以外的异常，则中断代码，抛出异常
"""
from selenium.webdriver.support.ui import WebDriverWait
import  time
#捕获超时异常
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


#启动浏览器
browser = webdriver.Chrome()
wait = WebDriverWait(browser,70)

#链接数据库
client = pymongo.MongoClient("127.0.0.1",27017)
db = client.jd_computer
collection = db.computer

def to_mongodb(data):
    try:
        collection.insert(data)
        print("数据存入成功")
    except:
        print("数据存入失败......")

def search():
    browser.get("https://www.jd.com/")
    try:
        #查找搜索框与搜索按钮，输入信息后点击
        inputs = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#key")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#search > div > div.form > button")))
        # print(inputs)
        inputs[0].send_keys("笔记本")
        submit.click()


        #查找笔记本按钮和销量按钮
        button1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#J_selector > div:nth-child(2) >div > div.sl-value > div.sl-v-list > ul > li:nth-child(1) > a")))
        button1.click()
        button2 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#J_filter > div.f-line.top > div.f-sort > a:nth-child(2)")))
        button2.click()

        #获取总页数
        page = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#J_bottomPage > span.p-skip > em:nth-child(1) > b")))
        # print(page)
        return page[0].text
    #如果异常，则请求超时，重新调用搜索函数，再次请求
    except TimeoutException:
        search()

#获取下一页
def next_page(page_num):
    #滑动到浏览器底部，加载所有商品信息
    try:
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(10)
        html = browser.page_source
        parse_html(html)
        while page_num ==101:
            exit()
        #查找下一页按钮，并点击
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#J_bottomPage > span.p-num > a.pn-next > em")))
        button.click()
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#J_goodsList > ul > li:nth-child(60)")))
        #判断翻页是否成功
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,"#J_bottomPage > span.p-num > a.curr"),str(page_num)))
    except ImportError:
        return next_page(page_num)




def parse_html(html):
    data = {}
    soup = BeautifulSoup(html,"lxml")
    goods_info = soup.select('.gl-item')
    #查看商品加载数量，是否加载完成
    quantity = str(len(goods_info))
    print(quantity)
    for info in goods_info:
        #获取商品名称
        title = info.select(".p-name.p-name-type-2 a em")[0].text.strip()
        data["_id"] = title
        #获取商品价格
        price = info.select(".p-price i")[0].text.strip()
        price = int(float(price))
        data["price"] = price
        #获取评论
        commit = info.select(".p-commit strong")[0].text.strip()
        commit = commit.replace("条评价","")
        if "万" in commit:
            commit = commit.split("万")
            commit = int(float(commit[0]))*10000
        else:
            commit = int(float(commit.replace("+","")))
        data['commit'] = commit
        #获取是否自营
        shop_property = info.select(".p-icons i")
        if len(shop_property) >=1:
            mess = shop_property[0].text.strip()
            if mess == "自营":
                data['shop_property'] = "自营"
            else:
                data['shop_property'] = "非自营"
        else:
            data['shop_property'] ="非自营"

        to_mongodb(data)
        print(data)
        print("..................................................")

def main():
    #通过search函数打开相应的商品展示页，并获取总页数信息
    total = int(search())  #商品总页数
    for i in range(2,total+2):
        time.sleep(20)
        print("第",i-1,"页")
        next_page(i)

if __name__ == '__main__':
    main()
