#Insight
项目介绍：
定时爬取安全网站咨询，目前写了7个（wifi联盟，darktrace，cita，ansi，CVE，huawei，中伦咨询，）
部署步骤：
1、将镜像python_lzy.tar还原为docker镜像：docker import python_lzy.tar python_lzy
2、data文件夹（保存数据）
   其中docker.sh保存执行脚本语句
   threading_spider.py为爬虫脚本
3、运行./docker.sh
4、新建crontab定时任务：0 12 * * * sh /home/lzy/lzy/docker.sh
