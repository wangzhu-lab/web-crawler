from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import sqlite3  # 进行SQLite数据库操作
import numpy as np
import pyecharts

def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1.爬取网页
    datalist = getData(baseurl)
    datalist1 = barchart(baseurl)
    datalist2 = fanchart(baseurl)
    datalist3 = labelchart(baseurl)
    datalist4 = worldmap(baseurl)
    savepath = "豆瓣电影Top250.xls"
    # dbpath = "movie250.db"
    saveData(datalist, savepath)
    #saveData(datalist2, savepath)
    # saveDate2DB(datalist,dbpath)
    # askURL("https://movie.douban.com/top250?start=")





#影片详情链接的规则
findLink = re.compile(r'<a class="" href="(.*?)">')     #创建正则表达式对象，表示规则(字符串的模式)
#影片图片
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)      #re.S让换行符包含在字符中
#影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
#影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
#找到评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
#找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
#找到影片的相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)



def getData(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取页面信息的函数，0-9 10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码
        # 2.解析数据--逐一解析
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串，形成列表
            # print(item)      #测试：查看电影item全部信息
            data = []  # 保存一部电影的所有信息
            item = str(item)

            # 影片详情的链接
            link = re.findall(findLink, item)[0]  # re库用来通过正则表达式查找指定的字符串
            data.append(link)  # 添加链接

            imgSrc = re.findall(findImgSrc, item)[0]
            data.append(imgSrc)  # 添加图片

            titles = re.findall(findTitle, item)
            if (len(titles) == 2):
                ctitle = titles[0]  # 添加中文名
                data.append(ctitle)
                otitle = titles[1].replace("/", "")  # 去掉无关的符号
                data.append(otitle)  # 添加外文名
            else:
                data.append(titles[0])
                data.append(' ')  # 外文名字留空

            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加评分

            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)  # 添加评价人数

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", ",")  # 去掉句号
                data.append(inq)
            else:
                data.append(" ")  # 留空

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s)?/>(\s+)?', " ", bd)  # 去掉<br/>
            bd = re.sub('/', " ", bd)  # 替换/
            data.append(bd.strip())  # 去掉前后的空格
            datalist.append(data)  # 拔处理好的一部电影信息放入datalist
    # print(datalist)
    return datalist

# 爬取网页
def barchart(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取页面信息的函数，0-9 10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码
        # 2.解析数据--逐一解析
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串，形成列表
            # print(item)      #测试：查看电影item全部信息
            data = []  # 保存一部电影的所有信息
            item = str(item)


            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加评分


            datalist.append(data)  # 拔处理好的一部电影信息放入datalist


    a = np.array(datalist)
    from itertools import chain
    a_a = chain.from_iterable(a)
    # print(a_a)
    b = np.array(list(a_a))
    b_b = b.astype(np.float)
    # print(b_b)
    c = [elem * 10 for elem in b_b]

    from pyecharts import Bar

    atter = ["评分>9.2", "9.0<评分<9.2", "8.8<评分<9.0", "8.5<评分<8.8", "评分<8.5"]
    countninetwo = 0
    countninezero = 0
    counteighteight = 0
    counteightfive = 0
    counteightfour = 0
    for index in c:
        if index > 92:
            countninetwo += 1;
        elif 90 < index <= 92:
            countninezero += 1;
        elif 88 < index <= 90:
            counteighteight += 1;
        elif 85 < index <= 88:
            counteightfive += 1;
        elif index < 85:
            counteightfour += 1;

    bar = Bar("电影评分等级统计")
    bar.add("评分", atter, [countninetwo, countninezero, counteighteight, counteightfive, counteightfour], is_stack=True)
    bar.render(r'条形图.html')
    return datalist


def fanchart(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取页面信息的函数，0-9 10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码
        # 2.解析数据--逐一解析
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串，形成列表
            # print(item)      #测试：查看电影item全部信息
            data = []  # 保存一部电影的所有信息
            item = str(item)



            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)  # 添加评价人数


            datalist.append(data)  # 拔处理好的一部电影信息放入datalist

    a = np.array(datalist)
    from itertools import chain
    a_a = chain.from_iterable(a)
    b = np.array(list(a_a))
    b_b = b.astype(np.float)
    c = [elem / 100 for elem in b_b]

    countone = 0
    countnine = 0
    counteight = 0
    countseven = 0
    countsix = 0
    for index in c:
        if index > 10000:
            countone += 1;
        elif 9000 < index < 10000:
            countnine += 1;
        elif 8000 < index < 9000:
            counteight += 1;
        elif 7000 < index <= 8000:
            countseven += 1;
        elif index < 7000:
            countsix += 1;
        from pyecharts import Pie

        attr = ["10w<评价数", "9w<评价数<10w", "8w<评价数<9w", "7w<评价数<8w", "评价数<7w"]
        v1 = [countone, countnine, counteight, countseven, countsix]
        pie = Pie("电影评论数分类")
        pie.add("", attr, v1, is_label_show=True)
        pie.render(r'饼状.html')

    return datalist

def labelchart(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取页面信息的函数，0-9 10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码
        # 2.解析数据--逐一解析
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串，形成列表
            # print(item)      #测试：查看电影item全部信息
            data = []  # 保存一部电影的所有信息
            item = str(item)
            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s)?/>(\s+)?', " ", bd)  # 去掉<br/>
            bd = re.sub('/', " ", bd)  # 替换/
            data.append(bd.strip())  # 去掉前后的空格
            datalist.append(data)  # 拔处理好的一部电影信息放入datalist


    a = np.array(datalist)
    from itertools import chain
    a_a = chain.from_iterable(a)
    b = np.array(list(a_a))

    countjuqing = 0
    countaiqing = 0
    countmeiguo = 0
    countxiju = 0
    countzainan = 0
    countfanzui = 0
    countdongzuo = 0
    countxuanyi = 0
    countqihuan = 0
    countgewu = 0
    countjingsong = 0
    countkehuan = 0
    countmaoxian = 0
    countzhanzheng = 0
    countxila = 0
    countjiating = 0
    countguzhuang = 0
    countwuxia = 0
    countlishi = 0
    countzhuanji = 0
    countyinyue = 0
    for index in b:
        pattern_juqing = re.compile("剧情")
        find_juqing = re.findall(pattern_juqing, index)
        if len(find_juqing) != 0:
            countjuqing += 1

        pattern_aiqing = re.compile("爱情")
        find_aiqing = re.findall(pattern_aiqing, index)
        if len(find_aiqing) != 0:
            countaiqing += 1

        pattern_meiguo = re.compile("美国")
        find_meiguo = re.findall(pattern_meiguo, index)
        if len(find_meiguo) != 0:
            countmeiguo += 1

        pattern_xiju = re.compile("喜剧")
        find_xiju = re.findall(pattern_xiju, index)
        if len(find_xiju) != 0:
            countxiju += 1

        pattern_zainan = re.compile("灾难")
        find_zainan = re.findall(pattern_zainan, index)
        if len(find_zainan) != 0:
            countzainan += 1

        pattern_fanzui = re.compile("犯罪")
        find_fanzui = re.findall(pattern_fanzui, index)
        if len(find_fanzui) != 0:
            countfanzui += 1

        pattern_dongzuo = re.compile("动作")
        find_dongzuo = re.findall(pattern_dongzuo, index)
        if len(find_dongzuo) != 0:
            countdongzuo += 1

        pattern_xuanyi = re.compile("悬疑")
        find_xuanyi = re.findall(pattern_xuanyi, index)
        if len(find_xuanyi) != 0:
            countxuanyi += 1

        pattern_maoxian = re.compile("冒险")
        find_maoxian = re.findall(pattern_maoxian, index)
        if len(find_maoxian) != 0:
            countmaoxian += 1

        pattern_qihuan = re.compile("奇幻")
        find_qihuan = re.findall(pattern_qihuan, index)
        if len(find_qihuan) != 0:
            countqihuan += 1

        pattern_jingsong = re.compile("惊悚")
        find_jingsong = re.findall(pattern_jingsong, index)
        if len(find_jingsong) != 0:
            countjingsong += 1

        pattern_gewu = re.compile("歌舞")
        find_gewu = re.findall(pattern_gewu, index)
        if len(find_gewu) != 0:
            countgewu += 1

        pattern_kehuan = re.compile("科幻")
        find_kehuan = re.findall(pattern_kehuan, index)
        if len(find_kehuan) != 0:
            countkehuan += 1

        pattern_lishi = re.compile("历史")
        find_lishi = re.findall(pattern_lishi, index)
        if len(find_lishi) != 0:
            countlishi += 1

        pattern_zhanzheng = re.compile("战争")
        find_zhanzheng = re.findall(pattern_zhanzheng, index)
        if len(find_zhanzheng) != 0:
            countzhanzheng += 1

        pattern_zhuanji = re.compile("传记")
        find_zhuanji = re.findall(pattern_zhuanji, index)
        if len(find_zhuanji) != 0:
            countzhuanji += 1

        pattern_jiating = re.compile("家庭")
        find_jiating = re.findall(pattern_jiating, index)
        if len(find_jiating) != 0:
            countjiating += 1

        pattern_xila = re.compile("希腊")
        find_xila = re.findall(pattern_xila, index)
        if len(find_xila) != 0:
            countxila += 1

        pattern_yinyue = re.compile("音乐")
        find_yinyue = re.findall(pattern_yinyue, index)
        if len(find_yinyue) != 0:
            countyinyue += 1

        pattern_guzhuang = re.compile("古装")
        find_guzhuang = re.findall(pattern_guzhuang, index)
        if len(find_guzhuang) != 0:
            countguzhuang += 1

        pattern_wuxia = re.compile("武侠")
        find_wuxia = re.findall(pattern_wuxia, index)
        if len(find_wuxia) != 0:
            countwuxia += 1


    from pyecharts import WordCloud

    name = ["剧情", "爱情", "美国", "喜剧", "灾难","犯罪","动作","悬疑","奇幻","歌舞","惊悚","科幻","冒险","历史","战争","传记","家庭","希腊","音乐","古装","武侠"]
    value = [countjuqing, countaiqing, countmeiguo, countxiju, countzainan, countfanzui, countdongzuo, countxuanyi, countqihuan, countgewu, countjingsong, countkehuan, countmaoxian,countlishi,countzhanzheng,countzhuanji,countjiating,countxila,countyinyue,countguzhuang,countwuxia]
    wordcloud = WordCloud(width=1300, height=620)
    wordcloud.add("", name, value, word_size_range=[20, 100])
    wordcloud.render(r'biaoqian.html')

    return datalist

def worldmap(baseurl):
    datalist = []
    for i in range(0, 10):  # 调用获取页面信息的函数，0-9 10次
        url = baseurl + str(i * 25)
        html = askURL(url)  # 保存获取到的网页源码
        # 2.解析数据--逐一解析
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):  # 查找符合要求的字符串，形成列表
            # print(item)      #测试：查看电影item全部信息
            data = []  # 保存一部电影的所有信息
            item = str(item)

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s)?/>(\s+)?', " ", bd)  # 去掉<br/>
            bd = re.sub('/', " ", bd)  # 替换/
            data.append(bd.strip())  # 去掉前后的空格
            datalist.append(data)  # 拔处理好的一部电影信息放入datalist


    a = np.array(datalist)
    from itertools import chain
    a_a = chain.from_iterable(a)
    b = np.array(list(a_a))

    countmeiguo = 0
    countriben = 0
    countzhongguo = 0
    countyingguo = 0
    counthanguo = 0
    countyidali = 0
    countaodaliya = 0
    countagenting = 0

    for index in b:
        pattern_meiguo = re.compile("美国")
        find_meiguo = re.findall(pattern_meiguo, index)
        if len(find_meiguo) != 0:
            countmeiguo += 1

        pattern_riben = re.compile("日本")
        find_riben = re.findall(pattern_riben, index)
        if len(find_riben) != 0:
            countriben += 1

        pattern_zhongguo = re.compile("中国")
        find_zhongguo = re.findall(pattern_zhongguo, index)
        if len(find_zhongguo) != 0:
            countzhongguo += 1

        pattern_yingguo = re.compile("英国")
        find_yingguo = re.findall(pattern_yingguo, index)
        if len(find_yingguo) != 0:
            countyingguo += 1

        pattern_hanguo = re.compile("韩国")
        find_hanguo = re.findall(pattern_hanguo, index)
        if len(find_hanguo) != 0:
            counthanguo += 1

        pattern_yidali = re.compile("意大利")
        find_yidali = re.findall(pattern_yidali, index)
        if len(find_yidali) != 0:
            countyidali += 1

        pattern_aodaliya = re.compile("澳大利亚")
        find_aodaliya = re.findall(pattern_aodaliya, index)
        if len(find_aodaliya) != 0:
            countaodaliya += 1

        pattern_agenting = re.compile("阿根廷")
        find_agenting = re.findall(pattern_agenting, index)
        if len(find_agenting) != 0:
            countagenting += 1

        from pyecharts import Map
        value = [countmeiguo,countriben,countzhongguo,countyingguo,counthanguo,countyidali,countaodaliya,countagenting]
        attr = ["United States", "Japan", "China", "Russia","Korea","Italy","Australia","Argentina"]
        map = Map("世界地图示例", width=1200, height=600)
        map.add(
            "",
            attr,
            value,
            maptype="world",
            is_visualmap=True,
            visual_text_color="#000",
            is_map_symbol_show=False,
        )
        map.render(r'world.html')

    return datalist



# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla/5.0(Windows NT 10.0;Win64;x64) AppleWebKit/537.36(KHTML, likeGecko) Chrome / 84.0.4147.89Safari / 537.36"
    }
    # 用户代理，表示告诉豆瓣，我们是什么类型的机器，浏览器（本质上是告诉浏览器我们可以接受什么水平的东西）
    request = urllib.request.Request(url, headers=head)
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

    # 3.保存数据


def saveData(datalist, savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象
    sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True)  # 创建工作表
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外文名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheet.write(0, i, col[i])  # 列名
    for i in range(0, 250):
        # print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i + 1, j, data[j])  # 数据

    book.save('豆瓣电影Top250.xls')  # 保存


def saveDate2DB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
                insert into movie250(
                info_link,pic_link,cname,ename,score,rated,introducation,info)
                values(%s)''' % ",".join(data)

        print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close


def init_db(dbpath):
    sql = '''
         create table movie250
        (
            id integer primary key autoincrement,
            info_link test,
            pic_link text,
            cname vrchar,
            ename varchar,
            score numeric,
            rated numeric,
            introducation text,
            info text
            )

    '''  # 创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


if __name__ == "__main__":  # 当函数执行时
    main()

    print("爬取完毕！")
