import os
def launch(run_path,*args):
    #读取设置
    from . import configs
    configs.set_runPath=run_path
    configs.init_configs()
    __version__=configs.set_version
    from . import gui
    from . import logman
    from . import rtmp_push

    # 初始化各个组件
    logman.init_logman()

    # 正式运行
    os.chdir(configs.set_runPath)
    print("")
    if "--debug" in args:
        configs.logman_debugout=True
        logman.write_log("CamMoitor {} (DEBUG) https://github.com/SystemFileB/CamMonitor_Server".format(__version__),type=logman.INFO,print_no_head=True)
    else:
        logman.write_log("CamMoitor {} https://github.com/SystemFileB/CamMonitor_Server".format(__version__),type=logman.INFO,print_no_head=True)
    logman.write_log("By SystemFileB 和所有贡献者们",print_no_head=True)
    print("")
    logman.write_log("运行于：{}".format(configs.set_runPath),print_no_head=True)
    print("")
    logman.del_oldlog()
    
    # 启动nginx
    for codec in rtmp_push.ffmpeg.get_encoders():
        logman.write_log("支持的编码器：{}".format(codec),type=logman.DEBUG)
    
    for camera in rtmp_push.ffmpeg.getCameras():
        logman.write_log("支持的摄像头：{}".format(camera),type=logman.DEBUG)

    for mic in rtmp_push.ffmpeg.getMics():
        logman.write_log("支持的麦克风：{}".format(mic),type=logman.DEBUG)