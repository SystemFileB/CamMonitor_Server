from . import logman,configs
import subprocess as sp
import os
import _thread as thread
import av
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from datetime import datetime
path=configs.set_runPath
nginx_isItRuned=False

class Nginx:
    def start_nginx(self):
        """启动nginx"""
        logman.write_log("检查nginx配置. . .",logman.Fore.LIGHTGREEN_EX,logman.INFO)
        logman.write_log("nginx执行目录: "+configs.set_nginxPathNotFull,type=logman.DEBUG)
        result=sp.run([configs.set_nginxPath,"-t","-p",configs.set_nginxPathNotFull],stderr=sp.PIPE).stderr.decode("gbk")
        logman.write_log("nginx配置检查结果："+result,type=logman.DEBUG)
        logman.write_log("启动nginx. . .",logman.Fore.LIGHTGREEN_EX,logman.INFO)
        thread.start_new_thread(self.nginx_runner,())

    def stop_nginx(self):
        """停止nginx"""
        logman.write_log("停止nginx...",logman.Fore.LIGHTGREEN_EX,logman.INFO)
        if nginx_isItRuned:
            sp.run([configs.set_nginxPath,"-s","stop","-p",configs.set_nginxPathNotFull])

    def nginx_runner(self):
        """nginx线程"""
        nginx_isItRuned=True
        ret=sp.run([configs.set_nginxPath,"-p",configs.set_nginxPathNotFull])
        if ret.returncode!=0:
            logman.write_log("nginx退出：{}".format(ret.returncode),logman.Fore.LIGHTRED_EX,logman.ERROR)
        nginx_isItRuned=False
nginx=Nginx()

class FFMpeg:
    def __init__(self, rtmp_url, camera_index=0, audio_device=-1):
        self.rtmp_url = rtmp_url
        self.camera_index = camera_index
        self.audio_device = audio_device
        self.capture = None
        self.output = None
        self.audio_capture = None

    def start(self):
        """启动摄像头捕获和RTMP推流"""
        logman.write_log("启动摄像头捕获和RTMP推流...", logman.Fore.LIGHTGREEN_EX, logman.INFO)
        self.capture = av.open(self.camera_index, format='dshow')  # 打开摄像头

        # 设置视频流参数
        stream = self.output.add_stream('flv', rate=30)
        stream.width = 640
        stream.height = 480

        # 启动视频推流线程
        thread.start_new_thread(self._capture_and_push, (stream,))

        # 如果指定了音频设备，则启动音频推流线程
        if self.audio_device>-1:
            self.audio_capture = av.open(self.audio_device, format='dshow')  # 打开音频设备
            thread.start_new_thread(self._capture_and_push_audio, ())

    def stop(self):
        """停止摄像头捕获和RTMP推流"""
        logman.write_log("停止摄像头捕获和RTMP推流...", logman.Fore.LIGHTGREEN_EX, logman.INFO)
        if self.capture:
            self.capture.close()
        if self.output:
            self.output.close()
        if self.audio_capture:
            self.audio_capture.close()

    def _capture_and_push(self, stream):
        """在新线程中执行视频捕获和推流操作"""
        self.output = av.open(self.rtmp_url, 'w')  # 打开RTMP输出流
        for packet in self.capture.demux():
            for frame in packet.decode():
                # 在帧上加水印
                frame = self.add_watermark(frame)
                # 推流
                self.push_frame(frame, stream)

    def _capture_and_push_audio(self):
        """在新线程中执行音频捕获和推流操作"""
        audio_stream = self.output.add_stream('aac', rate=44100)  # 设置音频流参数
        for packet in self.audio_capture.demux():
            for frame in packet.decode():
                # 推流
                self.push_frame(frame, audio_stream)

    def add_watermark(self, frame):
        """在帧上加水印"""
        img = frame.to_ndarray(format='bgr24')
        # 使用指定路径的字体文件添加水印
        watermark_text = datetime.now().strftime("%Y/%m/%d %H:%M:%S %A CamMoitor")
        watermark_font_path = os.path.join(configs.runPath, "assets/camo_serv/fonts/unifont.otf")
        watermark_font = ImageFont.truetype(watermark_font_path, 36)
        watermark_color = (255, 255, 255)
        watermark_image = Image.fromarray(img)
        draw = ImageDraw.Draw(watermark_image)
        draw.text((10, 10), watermark_text, font=watermark_font, fill=watermark_color)
        img = np.array(watermark_image)
        return av.VideoFrame.from_ndarray(img, format='bgr24')
    
    def getCameras(self):
        """获取摄像头设备名元组"""
        devices = []
        for device in av.device.DeviceInfo.list():
            if device.name.startswith("video"):
                devices.append(device.name)
        return tuple(devices)
    
    def getMics(self):
        """获取音频设备名元组"""
        devices = []
        for device in av.device.DeviceInfo.list():
            if device.name.startswith("audio"):
                devices.append(device.name)
        return tuple(devices)

    def push_frame(self, frame, stream):
        """推流一帧数据"""
        for packet in stream.encode(frame):
            self.output.mux(packet)

    def switch_camera(self, camera_index):
        """切换摄像头"""
        logman.write_log("切换摄像头...", logman.Fore.LIGHTGREEN_EX, logman.INFO)
        if self.capture:
            self.capture.close()
        self.camera_index = camera_index
        self.capture = av.open(self.camera_index, format='dshow')
    
    def switch_audio(self, audio_device):
        """切换音频设备"""
        logman.write_log("切换音频设备...", logman.Fore.LIGHTGREEN_EX, logman.INFO)
        if self.audio_capture:
            self.audio_capture.close()
        self.audio_device = audio_device

    def get_supported_decoders(self):
        """获取所有支持的解码器名"""
        decoders = []
        for codec in av.codec.codecs:
            if codec.type == 'decoder':
                decoders.append(codec.name)
        return decoders

ffmpeg = FFMpeg()
