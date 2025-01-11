from . import logman,configs
import subprocess as sp
import os
path=configs.set_runPath

def start_nginx():
    """启动nginx"""
    logman.write_log("检查nginx配置. . .",logman.Fore.LIGHTGREEN_EX,logman.INFO)
    logman.write_log("nginx执行目录: "+configs.set_nginxPathNotFull,type=logman.DEBUG)
    result=sp.run([configs.set_nginxPath,"-t","-p",configs.set_nginxPathNotFull],stderr=sp.PIPE).stderr.decode("gbk")
    logman.write_log("nginx配置检查结果："+result,type=logman.DEBUG)
    logman.write_log("启动nginx. . .",logman.Fore.LIGHTGREEN_EX,logman.INFO)