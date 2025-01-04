<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./banner_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="./banner_light.png">
  <source srcset="./banner_light.png">
  <img alt="CamMoitor_Server Banner">
</picture>

#     
一个项目，可以把摄像头当作监控来使用

由于还是WIP阶段，所以介绍信息并不多

# 📕 使用的其他开源项目
[Nginx](https://github.com/nginx/nginx) & [Nginx-RTMP-Module](https://github.com/arut/nginx-rtmp-module): 提供rtmp服务器

[FFMpeg](https://ffmpeg.org): 推流和拉流RTMP服务器里的内容

# ✅ 开发进度
- [x] 准备相关工具
- [x] 使用C++写一个启动程序
- [ ] 完成基本服务端
- [ ] 通过mctoast库来显示通知
- [ ] 写一个网页显示管理界面