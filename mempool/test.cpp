#include <stdio.h>
#include "mempool.h"
#include <iostream>

using namespace std;


class CTest
{
public:
	CTest() {data1 = data2 = 0;};
	~CTest(){};
	void*       operator new (size_t);
	void        operator delete(void* pTest);
public:
	int         data1;
	int         data2;
};

//MemPool mempool(sizeof(CTest), 126, "test");
MemoryPool mempool(sizeof(CTest));

void CTest::operator delete( void* pTest )
{  
	mempool.Free(pTest);  
}


void* CTest::operator new(size_t)
{
	return (CTest*)mempool.Alloc();
}


int main()
{
	LARGE_INTEGER BegainTime ;     
	LARGE_INTEGER EndTime ;     
	LARGE_INTEGER Frequency ;     
	QueryPerformanceFrequency(&Frequency);     
	QueryPerformanceCounter(&BegainTime) ;     
	// start


	const int n = 10000;
	CTest** ptr = new CTest*[n];
	
	cout<<"new"<<endl;
	for (int i = 0; i < n; ++i)
	{
		ptr[i] = new CTest;
	}
	cout<<"delete"<<endl;
	for (int i = 0; i < n; ++i)
	{
		delete ptr[i];
	}

	// end
	QueryPerformanceCounter(&EndTime);    
	cout << "花费时间:" <<(double)( EndTime.QuadPart - BegainTime.QuadPart )/ Frequency.QuadPart<<"s"<<endl;     

	//	::MessageBox(0, TEXT("hehe"), L"test", MB_OK | MB_ICONINFORMATION);
	system("pause");
}