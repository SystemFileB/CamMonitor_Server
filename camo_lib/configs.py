set_ffmpegPath=""
set_nginxPath=""
set_cmdinfoPath=""
set_runPath=""
set_version=""
inited=False

def init_configs():
    # 初始化配置文件
    global set_ffmpegPath,\
        set_nginxPath,\
        set_cmdinfoPath,\
        set_runPath,\
        set_version,\
        inited
    
    if not inited:
        import json
        with open(set_runPath+"/config/build_info.json","r",encoding="utf-8") as f:
            build_info=json.load(f)
            __version__=build_info["version"]
            set_cmdinfoPath=build_info["cmdinfo"]
            set_ffmpegPath=build_info["ffmpeg"]
            set_nginxPath=build_info["nginx"]
            set_version=__version__
        inited=True