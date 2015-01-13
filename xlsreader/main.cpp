#include "libxl/libxl.h"
#include "iostream"

using namespace libxl;
using namespace std;

int main() 
{
	Book* book = xlCreateBook();
	if(book)
	{
		if(book->load(L"f:/example1.xls"))
		{
			Sheet* sheet = book->getSheet(0);
			if(sheet)
			{
				size_t max_rows = sheet->lastRow();
				size_t max_cols = sheet->lastCol();

				cout<< "r:" <<max_rows<< "c: "<< max_cols << endl;
				for (size_t r=0; r<max_rows; ++r)
				{

					for( int c=0; c<max_cols; ++c)
					{
						const wchar_t* s = sheet->readStr(r, c);
						if(s) 
							wcout << s << endl;
						else
						{
							int n = sheet->readNum(r, c);
							if( n > 0 )
								wcout<< n << endl;
						}
					}
				}
			}
		}
	}

	getchar();
	book->release();
}