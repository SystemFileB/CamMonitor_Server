"""
CamMoitor，但是打日志用的
"""

from colorama import Fore,Style,init,Back
import os
from . import configs
from datetime import datetime
init()
set_runPath=configs.set_runPath

# 初始化日志类型常量
INFO=0
WARN=1
ERROR=2

def init_logman():
    """载入日志文件并初始化一些变量"""
    global set_runPath
    set_runPath=configs.set_runPath
    if os.path.exists(set_runPath+"/logs/latestlog.txt"):
        for i in range(1,11):
            oldlogdel=True
            if not os.path.exists(set_runPath+"/logs/oldlog_{}.txt".format(i)):
                oldlogdel=False
                break

        if oldlogdel:
            os.remove(set_runPath+"/logs/oldlog_10.txt")
        os.rename(set_runPath+"/logs/latestlog.txt",set_runPath+"/logs/oldlog_{}.txt".format(i))

    with open(set_runPath+"/logs/latestlog.txt","w",encoding="utf-8") as f:
        # 往日志写入时间
        now=datetime.now()
        f.write("==========日志时间：{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}==========\n".format(now.year,now.month,now.day,now.hour,now.minute,now.second))
        f.close()

    #让traceback写到日志里
    import sys
    sys.excepthook = log_exception

def write_log(text:str,color:str=Fore.WHITE,type:int=INFO,print_no_head=False):
    """
    打日志
    
    参数：
        text:str 日志内容
        color 颜色和样式，使用logman.Fore,logman.Style和logman.Back里的定义，默认logman.Fore.WHITE
        type 日志类型，默认logman.INFO
        print_no_head 不输出时间和类型
    """
    global set_runPath
    now=datetime.now() #初始日志类型
    if type==INFO:
        type_t=Fore.CYAN+"INFO"+Style.RESET_ALL
        type_l="INFO"
    elif type==WARN:
        type_t=Fore.YELLOW+"WARN"+Style.RESET_ALL
        type_l="WARN"
    elif type==ERROR:
        type_t=Fore.RED+"ERROR"+Style.RESET_ALL
        type_l="ERROR"

    head="[{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}] ".format(now.year,now.month,now.day,now.hour,now.minute,now.second) #初始头

    with open(set_runPath+"/logs/latestlog.txt","a",encoding="utf-8") as f: #输出
        f.write(head+"[{}] ".format(type_l)+text+"\n")
        f.close()
    if print_no_head:
        print(color+text+Style.RESET_ALL)
    else:
        print(head+"[{}]".format(str(type_t)),color+text+Style.RESET_ALL)

def log_exception(exc_type, exc_value, exc_traceback):
    """
    炸了把输出记到日志里
    """
    import traceback
    #获取报错信息
    tbdata="".join(traceback.format_exception_only(exc_type,exc_value))
    tbdata += "".join(traceback.format_tb(exc_traceback))
    if tbdata.endswith('\n'):
        tbdata = tbdata[:-1]

    write_log(tbdata,type=ERROR) #输出