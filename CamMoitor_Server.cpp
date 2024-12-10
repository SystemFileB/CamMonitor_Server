#include <windows.h>
#include <iostream>
#include <fstream>
//ע����Щ����󲿷ֶ���AI���׵�

using namespace std; //������std::�ˣ�yay

// ���庯��ָ������
typedef void (*Py_Initialize_t)();
typedef void (*Py_Finalize_t)();
typedef int (*PyRun_SimpleString_t)(const char *);

int main(int argc,char *argv[]) {
	// ���� python311.dll
	HMODULE hPythonDll = LoadLibrary("python311.dll");
	if (!hPythonDll) {
        std::cerr << "�޷�ִ���������򣬿�������Ϊû�а�װPython�������޸�. . ." << std::endl;
        return 1;
    } else {
    // ��ȡ������ַ
    Py_Initialize_t Py_Initialize = (Py_Initialize_t)GetProcAddress(hPythonDll, "Py_Initialize");
    Py_Finalize_t Py_Finalize = (Py_Finalize_t)GetProcAddress(hPythonDll, "Py_Finalize");
    PyRun_SimpleString_t PyRun_SimpleString = (PyRun_SimpleString_t)GetProcAddress(hPythonDll, "PyRun_SimpleString");
    if (!Py_Initialize || !Py_Finalize || !PyRun_SimpleString) {
        std::cerr << "�޷���ȡ����λ�ã������ǰ汾�б䶯. . ." << std::endl;
        FreeLibrary(hPythonDll);

        return 1;
    }

    // ��ʼ�� Python ������
    Py_Initialize();

    // ִ�� Python ����
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
        std::cerr << "�޷�ִ����������" << std::endl;
    }

    // ��ֹ Python ������
    Py_Finalize();

    // �ͷ� DLL
    FreeLibrary(hPythonDll);
	}

    return 0;
}
