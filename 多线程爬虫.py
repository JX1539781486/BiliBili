import csv
import time
from fake_useragent import UserAgent
import requests
import datetime
from concurrent import futures

ua = UserAgent()
count = 0

def get_data(url):
    global count
    headers = {
        "User-Agent": ua.random
    }

    try:
        # url = f'https://api.bilibili.com/x/web-interface/view?aid={i}'
        r = requests.get(url, headers)
        json_data = r.json()
        if json_data['code'] == -412:
            print(json_data['message'])
            print('睡眠300s')
            time.sleep(300)
            print(json_data['message'])
        if json_data['code'] == 0:
            count = count + 1
            list_data = json_data['data']
            """row = [视频标题,作者,分类,播放数,弹幕数,投币数,点赞量,分享数,收藏数,视频链接]"""
            row = [list_data['title'], list_data['owner']['name'], list_data['tname'], list_data['stat']['view'],
                   list_data['stat']['danmaku'],
                   list_data['stat']['coin'], list_data['stat']['like'], list_data['stat']['share'],
                   list_data['stat']['favorite'], 'https://www.bilibili.com/video/' + list_data['bvid']]
            with open('D:\项目合集\毕业设计-B站视频信息可视化\爬虫\数据\\data1.csv', 'a', encoding='utf-8-sig',
                      newline='') as data:
                csv.writer(data).writerow(row)
                print(f"第{count}条数据保存成功！")
    except Exception as e:
        print(f'报错原因{e}')
        # time.sleep(300)
        # print(f'循环次数{i}')


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    print(f"开始时间：{start_time}")
    # 初始化线程池，最大任务量为5
    pool = futures.ThreadPoolExecutor(max_workers=5)
    fs = []
    for url in [f'https://api.bilibili.com/x/web-interface/view?aid={i}' for i in range(10000000, 11000000)]:
        # 提交任务到线程池
        f = pool.submit(get_data, url)
        fs.append(f)
    # 等待任务全部完成
    futures.wait(fs)
    # get_data()
    end_time = datetime.datetime.now()
    print(f"结束时间：{end_time}")
    print(f'共耗时：{end_time - start_time}')
