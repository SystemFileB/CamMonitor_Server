set_ffmpegPath=""
set_nginxPath=""
set_nginxPathNotFull=""
set_cmdinfoPath=""
set_runPath=""
set_version=""
logman_debugout=False
logmancfg={}
rtmp_push_cfg={}
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
        logmancfg,\
        rtmp_push_cfg
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
        
        # rtmp_push配置
        try:
            with open(set_runPath+"/config/rtmp_push.json","r+",encoding="utf-8") as f:
                rtmp_push_cfg=json.load(f)
                f.close()
        except FileNotFoundError:
            with open(set_runPath+"/config/rtmp_push.json","w",encoding="utf-8") as f:
                rtmp_push_cfg={
                    "desc1": "这是rtmp_push的配置文件，你也可以使用图形界面来管理",
                    "desc2": "    timeformat    推送时的水印格式(strftime)，默认使用%Y/%m/%d %H:%M:%S %A CamMoitor",
                    "desc3": "    fps           一秒推送多少帧，默认30",
                    "desc4": "    camera        摄像头索引，默认0",
                    "desc5": "    width         推送的视频宽度，默认640",
                    "desc6": "    height        推送的视频高度，默认480",
                    "desc7": "    codec         视频编码器，默认libx264",
                    "desc8": "    audio         音频设备索引，默认-1，也就是不推送音频",
                    "desc9": "    audio_bitrate 音频码率，默认44100",
                    "timeformat": "%Y/%m/%d %H:%M:%S %A CamMoitor",
                    "fps": 30,
                    "camera": 0,
                    "width": 640,
                    "height": 480,
                    "codec": "libx264",
                    "audio": -1,
                    "audio_bitrate": 44100
                }
                json.dump(rtmp_push_cfg,f,indent=2,ensure_ascii=False)
