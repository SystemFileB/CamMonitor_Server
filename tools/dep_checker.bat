@echo off&cd /d %~dp0
echo �������. . .
python -c "import PIL,colorama,numpy">nul 2>nul
if "%errorlevel%"=="9009" (
echo ��δ��װPython������ʹ�ô����п�汾��װPython
pause
goto end
)

if "%errorlevel%"=="1" (
echo ��ʼ��װ����. . .
python -m pip install -r ../config/deps.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
if "%errorlevel%"=="1" (
echo ��������һЩ���õ���. . .  ����ն�
pause
goto end
)
echo ��װ�ɹ��������Ƿ�װ�ɹ�. . .
python -c "import PIL,colorama,numpy"
if "%errorlevel%"=="1" (
echo ��װʧ��
pause
goto end
)
)

echo ���Ѿ���װ�������������ٴΰ�װ
pause

:end