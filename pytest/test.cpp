//pythonfile
#ifdef _WIN32
#define _CRT_SECURE_NO_WARNINGS
#endif
#include <cstdlib>
#include <fstream>
#include <iostream>

int main()
{
	/*std::ifstream fin("pythonfile.dat", std::ios::binary);

	long hehe;
	int size;
	char strbuf[256] = {0};

	fin.read((char*)&hehe, sizeof(long));
	fin.read((char*)&size, sizeof(long));
	fin.read(strbuf, size);
	strbuf[size] = 0;

	std::cout << "hehe = " << hehe << std::endl;
	std::cout << "str = " << strbuf << std::endl;

	fin.close();;
	*/

	FILE* fp = fopen("pythonfile.dat", "rb");
	long hehe;
	int size;
	char strbuf[256] = {0};

	fread((void*)&hehe, sizeof(long), 1, fp);
	fread((void*)&size, sizeof(int), 1, fp);
	fread((void*)&strbuf, size, 1, fp);
	strbuf[size] = 0;

	std::cout << "hehe = " << hehe << std::endl;
	std::cout << "str = " << strbuf << std::endl;

	fclose(fp);

	system("pause");

	return 0;
}