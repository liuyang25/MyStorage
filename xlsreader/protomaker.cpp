#include "protomaker.h"
#include <list>
#include "ExcelFormat.h"


using namespace ExcelFormat;
struct Node
{
	std::string name;
	int			type;
	std::string str;
};

typedef std::list<Node*> NodeList;

inline bool ReadStructDefine();
inline bool ReadNameDefine();
inline bool ReadData();

bool ProtoMaker::ReadExcel(std::string file_path, std::string output_path, std::string &err)
{
	BasicExcel e;

	// Load a workbook with one sheet, display its contents and save into another file.
	if( !e.Load(file_path.c_str()) )
	{
		err = "open file error. file_path:";
		err.append(file_path);
		return false;
	}

	int sheet_count = e.GetTotalWorkSheets();
	if (sheet_count == 0)
	{
		err = "no sheet to read";
		return false;
	}

	for( int i = 0; i < sheet_count; ++i )
	{
		BasicExcelWorksheet* sheet = e.GetWorksheet(i);

		size_t max_rows = sheet->GetTotalRows();
		size_t max_cols = sheet->GetTotalCols();

		for (size_t r=0; r<max_rows; ++r)
		{
			for (size_t c=0; c<max_cols; ++c)
			{
				BasicExcelCell* cell = sheet->Cell(r,c);
				switch (cell->Type())
				{
				case BasicExcelCell::UNDEFINED:
					printf("          ");
					break;

				case BasicExcelCell::INT:
					printf("%10d", cell->GetInteger());
					break;

				case BasicExcelCell::DOUBLE:
					printf("%10.6lf", cell->GetDouble());
					break;

				case BasicExcelCell::STRING:
					printf("%10s", cell->GetString());
					break;

				case BasicExcelCell::WSTRING:
					wprintf(L"%10s", cell->GetWString());
					break;
				}
			}
			cout << endl;
		}
	}

	return true;
}


bool ReadStructDefine()
{

	return true;
}

bool ReadNameDefine()
{

	return true;
}

bool ReadData()
{

	return true;
}
