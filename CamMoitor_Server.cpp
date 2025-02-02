#include <windows.h>
#include <iostream>
#include <fstream>
#include <memory>
#include <array>
//注：这些代码大部分都是AI贡献的

using namespace std; //不用敲了，yay

// 定义函数指针类型
typedef void (*Py_Initialize_t)();
typedef void (*Py_Finalize_t)();
typedef int (*PyRun_SimpleString_t)(const char *);

string getPythonDllName() {
    
    array<char, 128> buffer;
    string result;
    unique_ptr<FILE, decltype(&pclose)> pipe(popen("python -V 2>&1", "r"), pclose);
    
    if (!pipe) {
        throw runtime_error("popen() failed!");
    }
    
    while (fgets(buffer.data(), buffer.size(), pipe.get()) != nullptr) {
        result += buffer.data();
    }
    
    // 查找"Python "字符串，并提取版本号
    size_t pos = result.find("Python ");
    if (pos == string::npos) {
        wchar_t command[]=L"start cmd /c tools\\cmdinfo \"无法获取Python DLL名称(你确定Python安装了吗)，请打开config/python_launcher手动修改Python DLL文件名\"";
        _wsystem(command);
        exit(1);
    }
    
    // 提取版本号的前三个字符（例如"3.9"或"3.1"）
    string version = result.substr(pos + 7, 4);
    
    // 替换版本号中的"."为""，并添加"python"前缀和".dll"后缀
    string dllName = "python" + version.replace(1, 1, "") + ".dll";
    
    return dllName;
}

string getPythonFromTxt() {
    string pythonPath;
    ifstream txtFile("config/python_launcher.txt");
    if (txtFile.is_open()) {
        getline(txtFile, pythonPath);
        txtFile.close();
    }

    if (pythonPath.empty()) {
        pythonPath = getPythonDllName();
        ofstream outFile("config/python_launcher.txt");
        if (outFile.is_open()) {
            outFile << pythonPath;
            outFile.close();
        }
    }

    return pythonPath;
}

int main(int argc, char *argv[]) {
    // 重定向标准输出到控制台
    if (AttachConsole(ATTACH_PARENT_PROCESS)) {
        freopen("CONOUT$", "w", stdout);
        freopen("CONOUT$", "w", stderr);
    }

    // 获得python3*.dll文件名
    string pythonPath = getPythonFromTxt();
    // 加载 python311.dll
    HMODULE hPythonDll=LoadLibrary(pythonPath.c_str());
	if (!hPythonDll) {
        wchar_t command[]=L"start cmd /c tools\\cmdinfo \"无法执行启动程序，可能是因为没有安装Python. . .\"";
        _wsystem(command);
        return 1;
    }
    // 获取函数地址
    Py_Initialize_t Py_Initialize = (Py_Initialize_t)GetProcAddress(hPythonDll, "Py_Initialize");
    Py_Finalize_t Py_Finalize = (Py_Finalize_t)GetProcAddress(hPythonDll, "Py_Finalize");
    PyRun_SimpleString_t PyRun_SimpleString = (PyRun_SimpleString_t)GetProcAddress(hPythonDll, "PyRun_SimpleString");
    if (!Py_Initialize || !Py_Finalize || !PyRun_SimpleString) {
        wchar_t command[]=L"start cmd /c tools\\cmdinfo.bat \"无法获取函数位置，可能是版本有变动. . .\"";
        _wsystem(command);
        FreeLibrary(hPythonDll);

        return 1;
    }

    // 初始化 Python 解释器
    Py_Initialize();

    // 执行 Python 代码
	string pythonCode="import launcher;launcher.main(";
	for(int i=1;i<argc;i++) {
		pythonCode+='"';
		pythonCode+=argv[i];
		pythonCode+='"';
		pythonCode+=",";
	}
	pythonCode+=")";
    int result = PyRun_SimpleString(pythonCode.c_str());

    // 终止 Python 解释器
    Py_Finalize();

    // 释放 DLL
    FreeLibrary(hPythonDll);

    return 0;
}
