#本代码用于爬取某盗版漫画网站的某漫画全部图片，一时撸完的py小练习
import requests  
import time
import os
import string
# 导入selenium的浏览器驱动接口
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#################################################################################
def diary_write(str,path):
    fo = open(path+"/diary.txt", "a",encoding='utf-8')
    fo.write(str+'\n')
    fo.close()

def img_dl(driver,url,path,h,n):
    driver.get(url)
    time.sleep(1)
    imurl = driver.find_element_by_css_selector("div[id='images']").find_element_by_css_selector('img').get_attribute('src')#这个可能会变化，注意查看
    print(str(imurl))
    r = requests.get(str(imurl))
    print(r.status_code) # 返回状态码
    if r.status_code == 200: #这里的代码是借鉴他人的，状态码什么意思待学习
        imgname = str(h)+'_'+str(n) + '.jpg'
        filename = path+'/'+imgname
        open(filename, 'wb').write(r.content) # 将内容写入图片
        diary_write(filename+' done',save_path)
        print(filename)
        print("done")
    del r
    return

def search_chapterlist(driver,url):
    driver.get(url)
    #img_group_list = driver.find_elements_by_tag_name或者 class等返回一个满足的列表而selector返回第一个符合的定位
    img_group_list = driver.find_element_by_css_selector('div.chapter-body').find_elements_by_tag_name('a')
    # 收集所有章节的链接
    imgurl_list=[]
    for img in img_group_list:
        imgurl = img.get_attribute('href')
        print(imgurl)
        imgurl_list.append(str(imgurl))
    #将收集到的链接写入文件
    f = open('C://Users//LENOVO//Downloads//temp//dakr//tmp//diary.txt', 'a', encoding='utf-8')
    f.write('\n'.join(imgurl_list))
    f.close()
    time.sleep(1)
    return imgurl_list

###########  main  ############
url = 'http://www.90mh.com/manhua/zaiyishijiemigongkaihougong/'
save_path = "C:/Users/LENOVO/Downloads/temp/dakr/tmp/nl"
diary_write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' start crawl',save_path)
chrome_options = Options()
chrome_options.add_argument('--headless')#无头模式
driver = webdriver.Chrome(chrome_options=chrome_options)
#driver = webdriver.Chrome()
driver.get(url)
time.sleep(6)#视当时的网速环境调整
list = search_chapterlist(driver,url)
i=0
while i<len(list):
    driver.get(list[i])
    driver.refresh()
    time.sleep(1)
    temptxt = driver.find_element_by_xpath('/html/body/div/div[2]/span').get_attribute('textContent')
    print(str(temptxt))
    fpage = int(temptxt[str(temptxt).find('/')+1:-1])
    temptxt2 = driver.find_element_by_xpath('/html/body/div/div[2]/h2').get_attribute('textContent')
    print(str(temptxt2))
    k=1
    while k<fpage+1:
        try:
            driver.get(list[i]+'#p='+str(k))
            driver.refresh()#刷新的目的是这个网站直接输入网址后不能马上跳到下一页
            time.sleep(1)
            img_dl(driver,list[i]+'#p='+str(k),save_path,str(temptxt2),str(k))
        except Exception as er:
            diary_write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" error "+list[i]+'#p='+str(k),save_path)
            diary_write(str(er),save_path)
        k=k+1
    i = i+1

# 关闭浏览器
diary_write(('\n')+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' END Normally'+('\n'),save_path)
driver.quit()

