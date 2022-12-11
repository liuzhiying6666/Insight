import threading
import time
import json
import requests
from lxml import etree
from bs4 import BeautifulSoup

class wify_org(threading.Thread):
    # wify_org网站获取news_urls、news_titles、news_contents字段
    def __init__(self):
        threading.Thread.__init__(self)
        self.filename = time.strftime("%Y-%m-%d", time.localtime(time.time())) + '_wify_org.json'
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
            'Connection': 'close'}

    def run(self):
        items = []
        for i in range(1,3):
            page_num = i
            if page_num == 0:
                url = "https://www.wi-fi.org/news-events/press-releases"
            else:
                url = "https://www.wi-fi.org/news-events/press-releases" + "?page=" + str(page_num)
            try:
                html = requests.get(url,headers=self.headers)
                html.encoding = html.apparent_encoding
                content = html.text
                tree = etree.HTML(content)
                a_list = tree.xpath('//*[@class="list-hr-lines"]/li')
                for a in a_list:
                    news_times = a.xpath('./div[2]/span//text()')  # 文章发布时间
                    url_path = a.xpath('./div[3]/a/@href')
                    url = "https://www.wi-fi.org" + url_path[0]  # 文章url
                    try:
                        news_html = requests.get(url, headers=self.headers)
                        news_html.encoding = news_html.apparent_encoding
                        news_content = news_html.text
                        news_tree = etree.HTML(news_content)
                        news_title = news_tree.xpath('//*[@class="content-main"]/div/h1//text()')  # 文章标题
                        news_titles = news_title[0].strip()
                        content = news_tree.xpath('//*[@class="content-main"]/div[1]/p/text()')
                        contents = ''
                        for i in content:
                            contents += i
                        news_contents = contents  # 文章内容
                        news_dict = str(dict((["url", url], ["date", news_times[0]], ["title", news_titles],
                                              ["content", news_contents]))) + '\n'
                        items.append(news_dict)
                    except:
                        pass
            except:
                pass
        with open('data/{}'.format(self.filename), 'w') as file_obj:
            json.dump(items, file_obj, indent=1)

class darktrace(threading.Thread):
    # darktrace网站，获取blog_title、blog_author_time、blog_content、url字段数据
    def __init__(self):
        threading.Thread.__init__(self)
        self.filename = time.strftime("%Y-%m-%d", time.localtime(time.time())) + '_darktrace.json'
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
            'Connection': 'close'}

    def run(self):
        blogs = []
        try:
            html = requests.get('https://darktrace.com/archive/blog-posts', headers=self.headers)
            html.encoding = html.apparent_encoding
            content = html.text
            tree = etree.HTML(content)
            a_list = tree.xpath('//*[@class="_3-column-grid-2-tablet-1-mobile w-dyn-items"]/div[@class="blog-post-item w-dyn-item"]/div/a/@href')
            for a in a_list[0:100]:
                url = "https://darktrace.com" + a  # 获取每篇文章的url
                try:
                    blog_html = requests.get(url, headers=self.headers)
                    blog_html.encoding = blog_html.apparent_encoding
                    blog_content1 = blog_html.text
                    blog_tree = etree.HTML(blog_content1)
                    blog_list = blog_tree.xpath('//*[@class="main-page-content-block"]')
                    for i in blog_list:
                        blog_title = i.xpath('./div[1]/div[1]/div[1]/h1//text()')[0]  # 标题
                        blog_author_time = str(
                            i.xpath('./div[1]/div[2]/div[1]/div[1]/div[2]/div[2]//text()')[0]) + ' ' + str(
                            i.xpath('./div[1]/div[2]/div[1]/div[1]/div[2]/div[1]//text()')[0])
                        blog_content = i.xpath('./div[1]/div[2]/div[1]/div[1]/div[3]//text()')  # 内容
                        blog_content_list = ""
                        for contents in blog_content:
                            blog_content_list += contents.strip()
                        blog_dict = str(dict((["url", url], ["date", blog_author_time], ["title", blog_title],
                                              ["content", blog_content_list]
                                              ))) + '\n'
                        blogs.append(blog_dict)
                except:
                    pass
        except:
            pass

        with open('data/{}'.format(self.filename), 'w') as file_obj:
            json.dump(blogs, file_obj, indent=1)

class cita(threading.Thread):
    # cita网站，获取article_date、article_title、article_url、article_content字段数据
    def __init__(self):
        threading.Thread.__init__(self)
        self.filename = time.strftime("%Y-%m-%d", time.localtime(time.time())) + '_ctia.json'
        self.base_url = "https://www.ctia.org/api/wordpress/posts/?categories=blog"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.13 Safari/537.36",
            'Connection': 'close'
        }

    def get_url(self):
        # 获取每篇文章的url
        urls = []
        for i in range(1, 43):
            if i == 1:
                url = self.base_url + "&limit=12"
            else:
                url = self.base_url + "&page=" + str(i) + "&limit=12"
            try:
                response = requests.get(url, headers=self.headers)  # 每页有12个文章
                json_source = json.loads(response.text)
                items = json_source['items']  # 拿到items键的值
                for j in items:
                    # 遍历items，每个items有12个值
                    slug = j['slug']
                    blog_url = "https://www.ctia.org/api/wordpress/posts/" + str(slug)
                    urls.append(blog_url)
            except:
                pass
        return urls[0:100]

    def run(self):
        # 遍历每篇文章，获取所需字段article_date、article_title、article_url、article_content字段数据
        urls = self.get_url()
        data = []
        for i in urls:
            try:
                article = requests.get(i, headers=self.headers)  # 获取文章的内容
                json_source = json.loads(article.text)
                items = json_source['items'][0]  # 拿到items键的值
                article_date = items['date']  # 文章发布日期
                article_title = items['title']  # 文章标题
                article_url = str(i).replace("https://www.ctia.org/api/wordpress/posts/",
                                             "https://www.ctia.org/news/")  # 文章地址
                aiticle_paragraph = len(items['fields']['components'])  # 获取文章段落数
                article_content = ''  # 获取文章内容
                for i in range(aiticle_paragraph):
                    paragraph = items['fields']['components'][i]['text']
                    article_content += paragraph
            except:
                pass
            temp = str(dict((["url", article_url], ["date", article_date], ["title", article_title],
                             ["content", article_content]))) + '\n'
            data.append(temp)
        with open('data/{}'.format(self.filename), 'w') as file_obj:
            json.dump(data, file_obj, indent=1)

class ansi(threading.Thread):
    # 获取ansi标准网站的ansi_url、ansi_title、ansi_content、ansi_time字段数据
    def __init__(self):
        threading.Thread.__init__(self)
        self.base_url = "http://www.msckobe.com/links/safety_code/"
        self.htm = ['ansi.htm', 'bs.htm', 'din.htm', 'en.htm', 'gb.htm', 'iec.htm', 'iso.htm', 'jis.htm', 'nf.htm']
        self.filename = time.strftime("%Y-%m-%d", time.localtime(time.time())) + '_ansi.json'
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
            'Connection': 'close'
        }

    def get_url(self):
        urls = []
        for htm in self.htm:
            url = self.base_url + htm
            urls.append(url)
        return urls

    def run(self):
        urls = self.get_url()
        items = []
        for i in urls:
            try:
                response = requests.get(i, headers=self.headers)
                response.encoding = 'utf8'
                res = response.text
                ansi_tree = etree.HTML(res)
                for j in range(2, 15):
                    ansi_url = i
                    if ansi_tree.xpath('//tr[{}]/td[2]/text()'.format(j)) != []:
                        ansi_title = ansi_tree.xpath('//tr[{}]/td[2]/text()'.format(j))[0]
                    else:
                        continue
                    ansi_content = ansi_tree.xpath('//tr[{}]/td[1]/text()'.format(j))[-1]
                    ansi_time = ansi_content[-5:]
                    ansi_dict = str(
                        dict((["url", ansi_url], ["date", ansi_time.strip('\n')], ["title", ansi_title.strip('\n')],
                              ["content", ansi_content.strip('\n')]))) + '\n'
                    items.append(ansi_dict)
            except:
                pass
        with open('data/{}'.format(self.filename), 'w', encoding = "utf-8") as file_obj:
            json.dump(items, file_obj, indent=1, ensure_ascii=False)

class CVE(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.filename = time.strftime("%Y-%m-%d", time.localtime(time.time())) + '_CVE.json'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'close'
        }
        self.url = "https://cassandra.cerias.purdue.edu/CVE_changes/today.html"

    def get_cve_urls(self):
        '''获取最新的cve漏洞url地址'''
        start_content = 'New entries'  # 起始字符串
        end_content = 'Graduations'
        try:
            response = requests.get(self.url, headers=self.headers, timeout=60)
            response = str(response.text)
            start_index = response.index(start_content)
            if start_index >= 0:
                start_index += len(start_content)
                end_index = response.index(end_content)
                cve_urls_content = response[start_index:end_index]  # 获取网页的指定范围
                soup = BeautifulSoup(cve_urls_content, "html.parser")
                cve_url_lists = []  # 存放获取到的cve url
                for u in soup.find_all('a'):
                    cve_url = u["href"]
                    cve_url_lists.append(cve_url)
                return cve_url_lists[0:100]
        except:
            pass

    def run(self):
        '''获取最新cve漏洞信息'''
        CVE_ListS = []
        cve_urls = self.get_cve_urls()
        for cve_url in cve_urls:
            try:
                response = requests.get(cve_url, headers=self.headers, timeout=60)
                response = response.text
                soup = BeautifulSoup(response, "html.parser")
                table = soup.find("div", id="GeneratedTable").find("table")  # 获取table标签内容
                cve_id = table.find_all("tr")[1].find("td", nowrap="nowrap").find("h2").string  # cve id
                cve_data = cve_id.split('-')[-2]
                cve_description = table.find_all("tr")[3].find("td").string  # cve 介绍
                try:
                    CVE_List = str(dict((["url", str(cve_url)], ["date", str(cve_data)], ["title", str(cve_id)],
                                         ["content", str(cve_description)])))
                    CVE_ListS.append(CVE_List)
                except:
                    CVE_List = str(dict((["url", str(cve_url)], ["date", str(cve_data)], ["title", str(cve_id)],
                                         ["content", cve_description])))
                    CVE_ListS.append(CVE_List)
            except:
                pass
        with open('data/{}'.format(self.filename), 'w') as file_obj:
            json.dump(CVE_ListS, file_obj, indent=1)

class huawei(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.filename = time.strftime("%Y-%m-%d", time.localtime(time.time())) + '_huawei.json'

    def get_url(self):
        urls = []
        base_url = "https://www.huawei.com/cn/psirt/all-bulletins"
        try:
            html = requests.get(url=base_url)
            html.encoding = html.apparent_encoding
            content = html.text
            tree = etree.HTML(content)
            report = tree.xpath('//*[@id="tbContent"]/li')
            for a in report:
                report_url = a.xpath('./a/@href')[0]
                url = "https://www.huawei.com" + report_url
                urls.append(url)
        except:
            pass
        return urls

    def run(self):
        reports = []
        urls = self.get_url()
        for url in urls:
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent':'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
                'Connection': 'close'
            }
            try:
                html = requests.post(url=url, headers=headers)
                html.encoding = html.apparent_encoding
                content = html.text
                tree = etree.HTML(content)
                report_title = tree.xpath('//*[@class="col-sm-9 psiet-detail"]/h1/text()')[0].strip()
                report_time = tree.xpath('//*[@id="indexmain_0_liInieialReleaseDate"]/text()')[0].replace("初始发布时间：","").strip()
                report_content1 = tree.xpath('//*[@class="moreinfo active "]/text()')[0].strip()
                report_content2 = tree.xpath('//*[@class="moreinfo active "]/p/text()')[0].strip()
                if report_content1 != '':
                    report_content = report_content1 + report_content2
                else:
                    report_content = report_content2
                report_url = url
                report_dict = str(dict((["url", report_url], ["date", report_time], ["title", report_title],
                                        ["content", report_content]))) + '\n'

                reports.append(report_dict)
            except:
                pass
        with open('data/{}'.format(self.filename), mode = 'w', encoding = "utf-8") as file_obj:
            json.dump(reports, file_obj, indent=1, ensure_ascii=False)

class zhonglun(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.filename = time.strftime("%Y-%m-%d", time.localtime(time.time())) + '_zhonglun.json'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'close'
        }
        self.url = "https://www.zhonglun.com/zx/zlgd.html"
    def run(self):
        html = requests.get(url = self.url, headers = self.headers)
        html.encoding = html.apparent_encoding
        content = html.text
        tree = etree.HTML(content)
        items = []
        for i in range(1, 21):
            final_url = "https://www.zhonglun.com" + tree.xpath('//*[@class="zx_list"]//li[%s]/a/@href' % i)[0]
            article_time = tree.xpath('//*[@class="zx_list"]//li[%s]/span/text()' % i)[0]

            try:
                news_html = requests.get(final_url, headers= self.headers)
                news_html.encoding = news_html.apparent_encoding
                news_content = news_html.text
                news_tree = etree.HTML(news_content)
                article_url = final_url
                article_times = article_time
                article_title = news_tree.xpath('//*[@class="news_main"]/div[1]/span/text()')[0]
                content = ''
                atticle_content = news_tree.xpath('//*[@id="myDiv"]//p/text()')
                for atticle in atticle_content:
                    content += str(atticle).replace("\n", "").replace("\t", "").replace("\xa0", "")
                news_dict = str(dict((["url", article_url], ["date", article_time], ["title", article_title],
                                      ["content", content]))) + '\n'
                items.append(news_dict)
            except:
                pass
        with open('data/{}'.format(self.filename), 'w', encoding = "utf-8") as file_obj:
            json.dump(items, file_obj, indent=1, ensure_ascii=False)

def multi_thread():
    t1 = wify_org()
    t2 = darktrace()
    t3 = cita()
    t4 = ansi()
    t5 = CVE()
    t6 = huawei()
    t7 = zhonglun()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
if __name__ == '__main__':
    multi_thread()
