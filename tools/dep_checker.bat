@echo off&cd /d %~dp0
echo 检查依赖. . .
python -c "import PIL,colorama,numpy">nul 2>nul
if "%errorlevel%"=="9009" (
echo 你未安装Python，请你使用带运行库版本或安装Python
pause
goto end
)

if "%errorlevel%"=="1" (
echo 开始安装依赖. . .
python -m pip install -r ../config/deps.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
if "%errorlevel%"=="1" (
echo 好像发生了一些不好的事. . .  检查终端
pause
goto end
)
echo 安装成功，测试是否安装成功. . .
python -c "import PIL,colorama,numpy"
if "%errorlevel%"=="1" (
echo 安装失败
pause
goto end
)
)

echo 你已经安装了依赖，无需再次安装
pause

:end