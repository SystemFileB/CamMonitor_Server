"""
CamMoitor，但是打日志用的
"""

from colorama import Fore,Style,init,Back
import os
from . import configs
from datetime import datetime
import glob
import time
init()
set_runPath=configs.set_runPath
latestlog=""

# 初始化日志类型常量
INFO=0
WARN=1
ERROR=2
DEBUG=3

def init_logman():
    """载入日志文件并初始化一些变量"""

    global set_runPath,latestlog
    set_runPath = configs.set_runPath

    # 获取当前时间并格式化
    now = datetime.now()
    latestlog = set_runPath + "/logs/" + f"log_{now.strftime('%Y%m%d_%H%M%S')}.txt"

    # 创建新的日志文件
    with open(latestlog, "w", encoding="utf-8") as f:
        # 往日志写入时间
        f.write("==========日志时间：{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}==========\n".format(now.year, now.month, now.day, now.hour, now.minute, now.second))
        f.close()

    #让traceback写到日志里
    import sys
    sys.excepthook = log_exception

def write_log(text:str,color:str=Fore.RESET,type:int=INFO,print_no_head=False,heads=(),heads_file=()):
    """
    打日志
    
    参数：
        text:str 日志内容
        color 颜色和样式，使用logman.Fore,logman.Style和logman.Back里的定义，默认logman.Fore.WHITE
        type 日志类型，默认logman.INFO
        print_no_head 不输出时间和类型
        *args 在 [时间] [日志类型] 两个头后面加上其他的内容
    """
    global set_runPath
    now=datetime.now() #初始日志类型
    head_file="" #日志文件头
    head=""      #输出日志头

    head_file+="[{}] [".format(datetime.strftime(now,configs.logmancfg["timeformat"])) #时间头
    head+="[{}] [".format(datetime.strftime(now,configs.logmancfg["timeformat"]))

    if type==INFO:
        head+=Fore.CYAN+"INFO"+Style.RESET_ALL
        head_file+="INFO"
    elif type==WARN:
        head+=Fore.YELLOW+"WARN"+Style.RESET_ALL
        head_file="WARN"
    elif type==ERROR:
        head+=Fore.RED+"ERROR"+Style.RESET_ALL
        head_file+="ERROR"
    elif type==DEBUG:
        if configs.logman_debugout==False:
            return
        head+=Fore.LIGHTBLACK_EX+"DEBUG"+Style.RESET_ALL
        head_file+="DEBUG"
    head+="] "
    head_file+="] "
    for arg in heads:
        head+="[{}] ".format(arg)
    for arg in heads_file:
        head_file+="[{}] ".format(arg)

    with open(latestlog,"a",encoding="utf-8") as f: #输出
        f.write(head_file+text+"\n")
        f.close()
    if print_no_head:
        print(color+text+Style.RESET_ALL)
    else:
        print(head+color+text+Style.RESET_ALL)

def del_oldlog():
    """删旧日志"""
    # 获取当前日期
    from datetime import date
    import datetime as datet
    today = date.today()
    # 计算删除日期
    del_date = today - datet.timedelta(days=configs.logmancfg["deldays"])
    
    # 遍历日志文件
    log_files = glob.glob(set_runPath + "/logs/log_*.txt")
    log_dates = []
    
    for log_file in log_files:
        # 从文件名中提取日期
        file_date_str = log_file.split("_")[1].split(".")[0]
        # 使用指定的时间格式解析日期
        file_date = datet.datetime.strptime(file_date_str, '%Y%m%d').date()
        log_dates.append(file_date)
    
    # 去重
    unique_dates = set(log_dates)
    
    # 检查日志日期
    if len(unique_dates) > configs.logmancfg["deldays"]:
        oldest_date = min(unique_dates)
        for log_file, file_date in zip(log_files, log_dates):
            if file_date == oldest_date:
                write_log("已删除{}，死因：超过{}天".format(log_file, configs.logmancfg["deldays"]), type=WARN)
                os.remove(log_file)

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