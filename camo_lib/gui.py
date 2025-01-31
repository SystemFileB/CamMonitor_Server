import pystray
from PIL import Image
from . import configs,rtmp_push,logman
import pystray
import tkinter as tk
import time
class Tray:
    def write_log(self,text,type=logman.INFO,color=logman.Fore.RESET):
        logman.write_log(text,type=type,color=color,heads=(logman.Fore.LIGHTBLUE_EX+"TRAY"+logman.Style.RESET_ALL,),heads_file=("TRAY",))
    def init(self):
        self.icon = pystray.Icon("CamMoitor_Server",
                                 Image.open(configs.set_runPath + "/assets/camo_serv/icon16.png"),
                                 "CamMoitor_Server",
                                 menu=pystray.Menu(
                                     pystray.MenuItem("重启Nginx", self.restart_nginx, visible=lambda item: not rtmp_push.nginx_isItRuned),
                                     pystray.Menu.SEPARATOR,
                                     pystray.MenuItem("设置", self.settings, default=True),
                                     pystray.MenuItem("退出", self.quit)
                                 ))
        self.write_log("OK! ")

    def mainloop(self):
        self.write_log("启动")
        self.icon.run()

    def restart_nginx(self):
        rtmp_push.nginx.start_nginx()
        self.icon.update_menu()

    def settings(self):
        # 在这里实现设置的逻辑
        self.write_log("设置：启动")

    def quit(self):
        # 在这里实现退出的逻辑
        self.icon.stop()
        rtmp_push.nginx.stop_nginx()
        while rtmp_push.nginx_isItRuned:
            time.sleep(0.05)

        self.write_log("退出")
tray=Tray()