// xlscpp.cpp : 定义控制台应用程序的入口点。
//

#include "ExcelFormat.h"

using namespace ExcelFormat;


#ifdef _WIN32

#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <shellapi.h>
#include <crtdbg.h>

#else // _WIN32

#define	FW_NORMAL	400
#define	FW_BOLD		700

#endif // _WIN32


static void example1(const char* path)
{
	BasicExcel xls;

	// create sheet 1 and get the associated BasicExcelWorksheet pointer
	xls.New(1);
	BasicExcelWorksheet* sheet = xls.GetWorksheet(0);

	XLSFormatManager fmt_mgr(xls);


	// Create a table containing an header row in bold and four rows below.

	ExcelFont font_bold;
	font_bold._weight = FW_BOLD; // 700

	CellFormat fmt_bold(fmt_mgr);
	fmt_bold.set_font(font_bold);

	int col, row = 0;

	for(col=0; col<10; ++col) {
		BasicExcelCell* cell = sheet->Cell(row, col);

		cell->Set("TITLE");
		cell->SetFormat(fmt_bold);
	}

	while(++row < 4) {
		for(int col=0; col<10; ++col)
			sheet->Cell(row, col)->Set("text");
	}


	++row;

	ExcelFont font_red_bold;
	font_red_bold._weight = FW_BOLD;
	font_red_bold._color_index = EGA_RED;

	CellFormat fmt_red_bold(fmt_mgr, font_red_bold);
	fmt_red_bold.set_color1(COLOR1_PAT_SOLID);			// solid background
	fmt_red_bold.set_color2(MAKE_COLOR2(EGA_BLUE,0));	// blue background

	CellFormat fmt_green(fmt_mgr, ExcelFont().set_color_index(EGA_GREEN));

	for(col=0; col<10; ++col) {
		BasicExcelCell* cell = sheet->Cell(row, col);

		cell->Set("xxx");
		cell->SetFormat(fmt_red_bold);

		cell = sheet->Cell(row, ++col);
		cell->Set("yyy");
		cell->SetFormat(fmt_green);
	}


	xls.SaveAs(path);
}


int main(int argc, char* argv[])
{
	BasicExcel e;

	// Load a workbook with one sheet, display its contents and save into another file.
	e.Load("f:/example1.xls");	
	BasicExcelWorksheet* sheet1 = e.GetWorksheet("Sheet1");
	if (sheet1)
	{
		size_t maxRows = sheet1->GetTotalRows();
		size_t maxCols = sheet1->GetTotalCols();
		cout << "Dimension of " << sheet1->GetAnsiSheetName() << " (" << maxRows << ", " << maxCols << ")" << endl;

		printf("          ");
		for (size_t c=0; c<maxCols; ++c) printf("%10d", c+1);
		cout << endl;

		for (size_t r=0; r<maxRows; ++r)
		{
			printf("%10d", r+1);
			for (size_t c=0; c<maxCols; ++c)
			{
				BasicExcelCell* cell = sheet1->Cell(r,c);
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
	cout << endl;
	return 0;
}

