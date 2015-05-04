#include <iostream>
#include <windows.h>
#include <ctime>
#include <fstream>
#include <string>

#include <map>
#include <vector>
#include "server/example1.h"
#include "server/gift.h"
#include "leetcode.hpp"

#include "heap.hpp"


using namespace std;

union Key
{
	struct
	{
		int i;
		int u : 4;
		int s : 28;
	};

	long long key;
};
static long long MakeKey(int i, int s, char u)
{
	static Key mk;

	mk.i = i;
	mk.s = s;
	mk.u = u;

	return mk.key;
}

/*
[
     [2],
    [3,4],
   [6,5,7],
  [4,1,8,3]
]
*/
/*class Solution {
public:
	set<int> hehe;
    int minimumTotal(vector<vector<int> > &triangle) {
    	int size = triangle.size();
    	for(int i = 0; i< size; ++i)
    	{
    		for( int j = 0; j < i; ++j)
    		{
    			auto v = triangle[i];
    			v[j]
    		}
    	}
    }
};*/

int main()
{
	LARGE_INTEGER BegainTime ;     
	LARGE_INTEGER EndTime ;     
	LARGE_INTEGER Frequency ;     
	QueryPerformanceFrequency(&Frequency);     
	QueryPerformanceCounter(&BegainTime) ;     

	//cout<<hammingWeight(13)<<endl;	// 1
	//cout<<reverseBits(1 )<<endl;		// 2
	//cout<<Pow(0.44894, -5)<<endl;

	//cout<<a.compare(b)<<endl;
	//cout<<isPalindromes("!!!")<<endl;
	
	//Heap<int> h;
	multiset<int> h;
	int x; 
	for( int i = 0; i < 100000; ++i)
	{
		x = rand();
		h.insert(x);
	}
	for (int i =0; i < 100000; ++i)
	{
		h.erase(h.begin());
	}

	QueryPerformanceCounter(&EndTime);    
	cout << "runtime:" <<(double)( EndTime.QuadPart - BegainTime.QuadPart )/ Frequency.QuadPart<<"s"<<endl;     

//	::MessageBox(0, TEXT("hehe"), L"test", MB_OK | MB_ICONINFORMATION);
	system("pause");
}
