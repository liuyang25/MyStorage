#include "protomaker.h"
#include <list>
#include "libxl/libxl.h"


using namespace libxl;
struct Node
{
	std::string name;
	int			type;
	std::string str;

};

typedef std::list<Node*> NodeList;

inline bool ReadStructDefine(Sheet* sheet, NodeList& node_list, std::string &err);
inline bool ReadNameDefine(Sheet* sheet, NodeList& node_list, std::string &err);
inline bool ReadData(Sheet* sheet, NodeList& node_list, std::string &err);

bool ProtoMaker::ReadExcel(std::string file_path, std::string output_path, std::string &err)
{
	Book* book = xlCreateBook();
	bool ret = true;
	if (!book)
	{
		err = "lib err";
		return false;
	}
		

	if (!book->load(file_path.c_str()))
	{
		err = "load file failed. path: ";
		err.append(file_path);
		book->release();
		return false;
	}

	int sheet_index = 0;
	Sheet* sheet = book->getSheet(sheet_index);
	NodeList node_list;
	while (sheet != nullptr)
	{
		if (!ReadStructDefine(sheet, node_list, err)) 
		{
			book->release();
			return false;
		}

		if (!ReadNameDefine(sheet, node_list, err))
		{
			book->release();
			return false;
		}

		sheet = book->getSheet(++sheet_index);
	}
	if(sheet)
	{
		size_t max_rows = sheet->lastRow();
		size_t max_cols = sheet->lastCol();

		for (size_t r=0; r<max_rows; ++r)
		{

			for( int c=0; c<max_cols; ++c)
			{
				//const wchar_t* s = sheet->readStr(r, c);
				//int n = sheet->readNum(r, c);
			}
		}
	}

	book->release();
	return true;
}


bool ReadStructDefine(Sheet* sheet, NodeList& node_list, std::string &err);
{

	return true;
}

bool ReadNameDefine(Sheet* sheet, NodeList& node_list, std::string &err);
{

	return true;
}

bool ReadData(Sheet* sheet, NodeList& node_list, std::string &err);
{

	return true;
}
