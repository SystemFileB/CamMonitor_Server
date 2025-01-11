set_ffmpegPath=""
set_nginxPath=""
set_nginxPathNotFull=""
set_cmdinfoPath=""
set_runPath=""
set_version=""
logman_debugout=False
logmancfg={}
inited=False

def init_configs():
    """初始化配置文件"""
    global inited
    if not inited:
        global set_ffmpegPath,\
        set_nginxPath,\
        set_nginxPathNotFull,\
        set_cmdinfoPath,\
        set_runPath,\
        set_version,\
        logmancfg
        import json

        # 编译信息
        with open(set_runPath+"/config/build_info.json","r",encoding="utf-8") as f:
            build_info=json.load(f)
            __version__=build_info["version"]
            set_cmdinfoPath=set_runPath+"/"+build_info["cmdinfo"]
            set_ffmpegPath=set_runPath+"/"+build_info["ffmpeg"]
            set_nginxPath=set_runPath+"/"+build_info["nginx"]
            set_nginxPathNotFull=build_info["nginx_prefix"]
            set_version=__version__
        inited=True

        # logman配置
        try:
            with open(set_runPath+"/config/logman.json","r+",encoding="utf-8") as f:
                logmancfg=json.load(f)
                f.close()
        except FileNotFoundError:
            with open(set_runPath+"/config/logman.json","w",encoding="utf-8") as f:
                logmancfg={
                    "desc1": "这是logman的配置文件，你也可以使用图形界面来管理",
                    "desc2": "    timeformat    日志的时间格式(strftime)，想详细点可以使用%Y/%m/%d %H:%M:%S，默认%H:%M:%S",
                    "desc3": "    deldays       保留几天日志，默认为7",
                    "timeformat": "%H:%M:%S",
                    "deldays": 7
                }
                json.dump(logmancfg,f,indent=2,ensure_ascii=False)
