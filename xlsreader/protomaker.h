#ifndef _PROTOMAKER_H_
#define _PROTOMAKER_H_

#include <iostream>

class ProtoMaker
{
public:
	bool ReadExcel(std::string file_path, std::string output_path, std::string &err);
};

#endif