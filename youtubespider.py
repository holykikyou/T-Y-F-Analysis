# -*- coding: utf-8 -*-
"""
爬取CNN(美国有线电视新闻网)视频题目、观看次数、发表时间
CNN:806w订阅，14w视频
"""
import csv
import locale
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# watch_counts = open(r"./data/题目、观看人数、时间、链接.txt", 'w+', encoding='utf-8')

# 替换为自己的chrome驱动位置
chrome_driver = r"D:\Anaconda3\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"
chrome_option = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images': 2}
chrome_option.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_option)


# 即CNN的频道url
url = "https://www.youtube.com/user/CNN/videos"
driver.get(url)

count1 = 0  # 记录是否写入评论数
count2 = 0  # 记录当前写入的评论数
count3 = 0  # 每循环10次 输出一次时间
flag_exit = 0  # 记录是否应该退出
pre_height = 0
now_height = 0


csv_file_path = "./data/题目、观看人数、发表时间.csv"

csv_file = open(csv_file_path, "w+", encoding="utf-8", newline='')
writer = csv.writer(csv_file)

while True:
    try:
        driver.execute_script("scrollBy(0,10000)")  # 执行拖动滚动条操作
        time.sleep(1)

        if count3 % 20 == 0:
            print("count:" + str(count3))
            now_height = driver.execute_script("return document.documentElement.scrollHeight;")
            if now_height == pre_height:  # 判断拖动滚动条后的最大高度与上一次的最大高度的大小，相等表明到了最底部
                break
            pre_height = now_height

        count3 += 1

        videos = driver.find_elements_by_xpath("//div[@id='details' and @class='style-scope ytd-grid-video-renderer']")
        print(len(videos))
        for i in range(count2, len(videos)):
            video_a = driver.find_element_by_xpath(
                "//div[@id='items' and @class='style-scope ytd-grid-renderer']/ytd-grid-video-renderer"
                "[@class='style-scope ytd-grid-renderer'][" +
                str(i + 1) + "]/div/div[@id='details']/div[@id='meta']/h3/a")
            video_title = video_a.text
            video_href = video_a.get_attribute("href")
            video_detail = video_a.get_attribute("aria-label")
            writer.writerow([i+1, video_detail, video_href])
            if i % 20 == 0:
                print("write:" + str(i))
        count2 = len(videos)
    except Exception as e:
        print(e)
csv_file.close()

# -*- coding: utf-8 -*-
import time

import selenium
import csv

from selenium import webdriver

# 视频的链接， 可以从之前爬取的文件中读取
hrefs = list()
# hrefs.append("https://www.youtube.com/watch?v=Hi7zs5K0n78")
# hrefs.append("https://www.youtube.com/watch?v=sLdtBBXwdCk")
with open(r"../data/5hrefs.txt") as f:
    line = f.readline()
    while line:
        hrefs.append(str(line).strip())
        line = f.readline()

chrome_path = r"D:\Program Files\Anaconda3\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe"
scroll_js_5k = "scrollBy(0, 5000)"
scroll_js_10w = "scrollBy(0, 100000)"

for i in range(len(hrefs)):
    file_name = "../data/comments_full/" + str(i + 1) + ".csv"
    href = hrefs[i]
    with open(file_name, "a+", errors="ignore", newline='') as f:
        writer = csv.writer(f)

        # 获取浏览器
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=chrome_options)
        driver.set_window_position(x=400, y=0)
        driver.get(href)
        time.sleep(2)
        driver.execute_script(scroll_js_5k)
        time.sleep(2)

        # 获取题目、发布时间、观看人数、顶、踩、评论数
        title = driver.find_element_by_xpath(
            "//h1[@class='title style-scope ytd-video-primary-info-renderer']/yt-formatted-string").text
        publish_time = driver.find_element_by_xpath(
            "//div[@id='date']/yt-formatted-string[@class='style-scope ytd-video-primary-info-renderer']").text
        watch_count = driver.find_element_by_xpath(
            "//span[@class='view-count style-scope yt-view-count-renderer']").text
        nice_count = driver.find_element_by_xpath(
            "//div[@id='menu-container']/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-formatted-string").text
        bad_count = driver.find_element_by_xpath(
            "//div[@id='menu-container']/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[2]/a/yt-formatted-string").text
        comment_count = driver.find_element_by_xpath(
            "//yt-formatted-string[@class='count-text style-scope ytd-comments-header-renderer']").text
        writer.writerow([title, publish_time, watch_count, nice_count, bad_count, comment_count])

        # 获取排序方式按钮并点击
        order_btn = driver.find_element_by_xpath("//div[@id='icon-label' and @class='style-scope yt-dropdown-menu']")
        order_btn.click()
        time.sleep(2)

        # 按时间排序
        time_comment_btn = driver.find_element_by_xpath(
            "//a[@class='yt-simple-endpoint style-scope yt-dropdown-menu']/paper-item/paper-item-body/"
            "div[@class='item style-scope yt-dropdown-menu']")
        time_comment_btn.click()
        time.sleep(1)

        # 用来判断是否到底
        count_1 = 0
        now_height = 0
        pre_height = 0

        count_2 = 0  # 每隔100条输出一下评论数
        count_3 = 0  # 计数器，记住当前爬取的评论数
        while True:
            driver.execute_script(scroll_js_10w)
            time.sleep(2)

            # 向下滑动
            count_1 += 1
            count_2 += 1
            if count_1 % 20 == 0:
                now_height = driver.execute_script("return document.documentElement.scrollHeight;")
                if now_height == pre_height:
                    break
                pre_height = now_height

            # 获取评论数量
            comments = driver.find_elements_by_xpath(
                "//div[@id='contents']/ytd-comment-thread-renderer[@class='style-scope ytd-item-section-renderer']")
            if count_2 % 5 == 0:
                print("评论数：" + str(len(comments)))

            # 循环获取评论信息并写入文件
            for j in range(count_3, len(comments)):
                try:
                    if j % 20 == 0:
                        print(j)
                    # 点赞数
                    ok_count = driver.find_element_by_xpath(
                        "//div[@id='contents']/ytd-comment-thread-renderer[@class='style-scope "
                        "ytd-item-section-renderer'][" +
                        str(j + 1) + "]/ytd-comment-renderer/div[@id='body']/div[@id='main']"
                                     "/ytd-comment-action-buttons-"
                                     "renderer/div[@id='toolbar']/span[@id='vote-count-middle']").text
                    ok_count = str(ok_count).strip()

                    # 评论人的名
                    comment_name = driver.find_element_by_xpath(
                        "//div[@id='contents']/ytd-comment-thread-renderer[@class='style-scope "
                        "ytd-item-section-renderer'][" +
                        str(j + 1) + "]/ytd-comment-renderer/div[@id='body']/div[@id='main']/div[@id='header']/"
                                     "div[@id='header-author']/a/span[@class='style-scope ytd-comment-renderer']").text
                    comment_name = str(comment_name).strip()

                    # 评论时间
                    comment_time = driver.find_element_by_xpath(
                        "//div[@id='contents']/ytd-comment-thread-renderer[@class='style-scope "
                        "ytd-item-section-renderer'][" +
                        str(j + 1) + "]/ytd-comment-renderer/div[@id='body']/div[@id='main']/div[@id='header']/"
                                     "div[@id='header-author']/yt-formatted-string/a[@class='yt-simple-endpoint "
                                     "style-scope yt-formatted-string']").text
                    comment_time = str(comment_time).strip()

                    # 评论内容
                    comment_content = driver.find_element_by_xpath(
                        "//div[@id='contents']/ytd-comment-thread-renderer[@class='style-scope "
                        "ytd-item-section-renderer'][" +
                        str(j + 1) + "]/ytd-comment-renderer/div[@id='body']/div[@id='main']/ytd-expander"
                                     "[@id='expander']/"
                                     "div[@id='content']/yt-formatted-string[@id='content-text']").text
                    comment_content = str(comment_content).strip()

                    writer.writerow([comment_name, comment_time, ok_count, comment_content])
                except Exception as e:
                    print(e)
            count_3 = len(comments)
            time.sleep(2)
        driver.close()

