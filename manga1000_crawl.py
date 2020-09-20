#https://manga1000.com/
#本代码用于爬取某盗版漫画网站的某漫画全部图片
import requests  
import time
import os
import string
# 导入selenium的浏览器驱动接口
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#################################################################################
def diary_write(str,path):#日记
    fo = open(path+"/diary.txt", "a",encoding='utf-8')
    fo.write(str+'\n')
    fo.close()

def img_dl(driver,url,path):#每一话的下载
    driver.get(url)
    time.sleep(3)
    ims = driver.find_elements_by_class_name("aligncenter")#这个可能会变化，注意查看
    h = ims[0].get_attribute('alt')
    os.mkdir(path+'/'+h)#创建路径
    for i in ims:
        imurl = str(i.get_attribute('src'))
        n = str(i.get_attribute('onload'))
        #print(imurl)
        r = requests.get(imurl,verify=False)#https问题，要加verify参数，这里代研究
        #print(r.status_code) # 返回状态码
        if r.status_code == 200: #这里的代码是借鉴他人的，状态码什么意思待学习
            imgname = h+'_'+n + '.jpg'
            filepath = path+'/'+h+'/'+imgname
            open(filepath, 'wb').write(r.content) # 将内容写入图片
            #print(imgname+" success")
        del r
    return

def search_chapterlist(driver,url):#返回一个每一话链接的列表
    driver.get(url)
    #img_group_list = driver.find_elements_by_tag_name或者 class等返回一个满足的列表而selector返回第一个符合的定位
    list = driver.find_element_by_tag_name('tbody').find_elements_by_tag_name('a')
    # 收集所有章节的链接
    urllist=[]
    for i in list:
        href = str(i.get_attribute('href'))
        #print(href)
        urllist.append(href)
    #将收集到的链接写入文件
    #f = open('C://Users//LENOVO//Downloads//temp//dakr//tmp//diary.txt', 'a', encoding='utf-8')
    #f.write('\n'.join(imgurl_list))
    #f.close()
    time.sleep(1)
    return urllist
    
###########  main  ############
if __name__ == '__main__':
    url = 'https://manga1000.com/%e3%82%a4%e3%83%b3%e3%83%95%e3%82%a7%e3%82%af%e3%82%b7%e3%83%a7%e3%83%b3-raw-free/'
    save_path = "E:/CODE/PY/manga1000_crawl/tmp"
    diary_write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' start crawl',save_path)
    chrome_options = Options()
    chrome_options.add_argument('--headless')#无头模式
    driver = webdriver.Chrome(chrome_options=chrome_options)
    #driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)#视当时的网速环境调整
    list = search_chapterlist(driver,url)
    schap = float(input('请输入下载章节的一端（较小的数）'))
    index_schap = len(list)-schap
    bchap = float(input('请输入下载的章节的另一端（较大的数）'))
    index_bchap = len(list)-bchap 
    for k in list:
        if (list.index(k)>=index_bchap) and (list.index(k)<=index_schap):
            driver.get(k)
            driver.refresh()#避免有时候会卡在上个页面
            time.sleep(3)
            try:#如果有错误比如之前爬过的话数，文件夹已经创建会报错直接跳过
                img_dl(driver,k,save_path)
                diary_write('话数'+str(list.index(k))+" success！",save_path)
            except:
                print(k+' error')
                diary_write('话数'+str(list.index(k))+" error！",save_path)
                continue
    # 关闭浏览器
    diary_write(('\n')+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' END Normally'+('\n'),save_path)
    driver.quit()