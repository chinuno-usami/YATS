# YATS
Yet Another Tieba Sign  
python 实现的贴吧签到脚本
参考[kk签到](https://github.com/kookxiang/Tieba_Sign)编写  
不需要数据库纯命令行工具，适合树莓派使用  

# Python2.x  

# 使用方式
1. 获取源码到任意目录
2. yats目录中新建bduss文件存放bduss,每条一行
3. 设置计划任务，建议1点之后签到`10 01 * * * /usr/bin/python2 /path/to/yats/sign_main.py >> /path/to/yats/sign.log`
