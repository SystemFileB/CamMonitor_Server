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

    #正式运行
    print("")
    logman.write_log("CamMoitor {} https://github.com/SystemFileB/CamMonitor_Server".format(__version__),type=logman.INFO,print_no_head=True)
    logman.write_log("By SystemFileB 和所有贡献者们",print_no_head=True)
    print("")
    logman.write_log("运行于：{}".format(configs.set_runPath),print_no_head=True)
    print("")
    logman.write_log("启动nginx. . .",color=logman.Fore.LIGHTGREEN_EX)