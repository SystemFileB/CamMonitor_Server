# 🗃️ 归档
这是我 NaN 年前的陈年老项目，而且因为 pyav 库我不熟悉，AI 又写了一堆石山代码，导致我没办法写推流部分

看来，得要把 C/C++/Rust 放进来写这个项目，才能有机会把它完成

但是，我打算先把它存档，虽然这里有一些代码我可能用得上（比如 `CamMonitor_Server.cpp` 启动器还有那个较轻量的日志管理器，虽然我现在已经知道了可以用 `logging`）

我一般没有打主题（topic）的习惯，所以其它的仓库数据都很惨淡

...与其关注我的第一个仓库，为什么不去多看看我的后期之秀呢？它们明显比这个仓库完成度更高...

...如果你感兴趣的话

---

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./banner_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="./banner_light.png">
  <img alt="CamMoitor_Server Banner" src="./banner_light.png">
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
  - [ ] \_\_init__.py 主程序
  - [x] configs.py 配置文件存储
  - [ ] gui.py 托盘图标及引导进入管理页面程序
  - [x] logman.py 日志管理器
  - [ ] rtmp_push.py 古希腊掌管推流，nginx进程管理的神
- [ ] 通过mctoast库来显示通知
- [ ] 写一个网页显示管理界面
