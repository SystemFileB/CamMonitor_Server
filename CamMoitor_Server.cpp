#include <windows.h>
#include <iostream>
#include <fstream>
//注：这些代码大部分都是AI贡献的

using namespace std; //不用敲std::了，yay

// 定义函数指针类型
typedef void (*Py_Initialize_t)();
typedef void (*Py_Finalize_t)();
typedef int (*PyRun_SimpleString_t)(const char *);

int main(int argc,char *argv[]) {
	// 加载 python311.dll
	HMODULE hPythonDll = LoadLibrary("python311.dll");
	if (!hPythonDll) {
        std::cerr << "无法执行启动程序，可能是因为没有安装Python，尝试修复. . ." << std::endl;
        return 1;
    } else {
    // 获取函数地址
    Py_Initialize_t Py_Initialize = (Py_Initialize_t)GetProcAddress(hPythonDll, "Py_Initialize");
    Py_Finalize_t Py_Finalize = (Py_Finalize_t)GetProcAddress(hPythonDll, "Py_Finalize");
    PyRun_SimpleString_t PyRun_SimpleString = (PyRun_SimpleString_t)GetProcAddress(hPythonDll, "PyRun_SimpleString");
    if (!Py_Initialize || !Py_Finalize || !PyRun_SimpleString) {
        std::cerr << "无法获取函数位置，可能是版本有变动. . ." << std::endl;
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
    if (result != 0) {
        std::cerr << "无法执行启动命令" << std::endl;
    }

    // 终止 Python 解释器
    Py_Finalize();

    // 释放 DLL
    FreeLibrary(hPythonDll);
	}

    return 0;
}
