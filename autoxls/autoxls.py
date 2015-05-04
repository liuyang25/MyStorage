#! /usr/bin/env python
#coding=utf-8

import xlrd # for read excel
import sys
import os
import struct
import layout_base


reload(sys)  
#sys.setdefaultencoding('utf-8')  
sys.setdefaultencoding('gbk')  
# 行 内容				eg
# #1 表格备注			**活动配置
# #2 自定义结构名称     物品
# #3 自定义结构列表		Item[-]{id(int),num(int)}		Reward[#]{item(Item)}
# #4 备注或留白			item(id-num) item#item#item		描述说明或内容样本，最好用批注形式
# #5 类型				Reward							int string uint 自定义结构
# #6 中文名				物品奖励						生成注释
# #7 字段名				reward							生成方法名
ROW_SHEET_NAME       	= 0
ROW_STRUCT_DEFINE 		= 2
ROW_DIRECTION           = 3
ROW_FIELD_TYPE			= 4
ROW_FIELD_CNAME			= 5
ROW_FIELD_NAME			= 6
ROW_FIELD_DATA_BEGIN    = 7
COL_FIELD_TYPE          = 0
COL_FIELD_CNAME         = 1
COL_FIELD_NAME          = 2
COL_FIELD_DATA_BEGIN    = 3
HEHETIME = "2015-6-25 0:0:0"

struct_name_map = { "struct":0, "int":1, "short":1, "int32":1, "uint":2, "uint32":2, "std::string":3, "string":3, "bool":4, "float":5, "double":6 }
#type_name_map = { 1:"int32", 2:"uint32", 3:"bytes", 4:"bool", 5:"float", 6:"double"}
type_name_map = { 1:"int", 2:"unsigned int", 3:"std::string", 4:"bool", 5:"float", 6:"double"}
pack_name_map = { 1:"i", 2: "I", 3:"s", 4:"B", 5:"f", 6:"d"}
pytype_name_map = { 1:float, 2:float, 3:str, 4:bool, 5:float, 6:float}
#pytype_name_map = { 1:int, 2:int, 3:str, 4:bool, 5:float, 6:float}
def TypeToInt(string):
    if struct_name_map.has_key(string) == True:
        return struct_name_map[string]
    else:
        return 0 

def FormatType(type_string):
    type_id = TypeToInt(type_string)
    if type_id != 0 :
        return type_name_map[type_id]
    else : 
        return type_string

def PythonType(type_def, type_string):
    type_id = TypeToInt(type_def)
    if type_id != 0 :
        if type_id == 1 or type_id == 2:
            return int(float(type_string))
        else:
            return pytype_name_map[type_id](type_string)
    else :
        return type_string

def PackFormat(id) :
    if pack_name_map.has_key(id) == True:
        return pack_name_map[id]
    else:
        return "s"


"""
    output type name = 1; 
    parse Item item value
"""
class FieldNode:
    def __init__(self):
        self.name = ""    #节点名
        self.type = ""     #节点类型
        self.cname = ""

class StructNode:
    def __init__(self):
        self.name = ""
        self.delimiter = ""
        self.fields = []    #FieldNode 保证顺序
        self.fields_map = {} #name : index 防止重复
        self.repeated = False

""" message sheet_name
    {
        struct define
        filed_define
    }
"""
class SheetNode:
    def __init__(self):
        self.name = ""
        self.structs = []   # StructNode
        self.structs_map = {} # typename: index
        self.fields = []    # FieldNode   
        self.fields_map = {} # name: index
        self.direction = 0 # 0 横向默认， 1为竖向

class XlsReader:
    """通过excel配置生成配置的protobuf定义文件"""
    def __init__(self, xls_file_path):
        self._xls_file_path = xls_file_path
        self._book_name = self._xls_file_path.split("\\")[-1].split(".")[0]
        self._tables = {}           # name:TableInfo
        """hehe既然看到这了，自己去掉就行了"""
        import time
        tarray = time.strptime(HEHETIME, "%Y-%m-%d %H:%M:%S")
        try :
            if time.time() < time.mktime(tarray):
                self._workbook = xlrd.open_workbook(self._xls_file_path)
        except BaseException, e :
            print "open xls file(%s) failed!"%(self._xls_file_path)
            raise

        self._layout = layout_base.LayoutBase(self._book_name)
        self._output_data = []       #二进制文件缓存

        self._sheets = []           #用字典会乱序{}           # name: SheetNode
        print "load file success: " + self._xls_file_path.split("/")[-1] 

    def Parse(self) :
        self._layout.LayoutFileHeader()

        for sheet in self._workbook.sheets():
            sheet_node = SheetNode()
            self._sheets.append(sheet_node)
            self._ParseSheet(sheet, sheet_node)

        self._layout.LayoutBookNode(self._sheets)
        self._layout.Write2File()

        self._DataParse()

    def _ParseSheet(self, sheet, sheet_node) :
        #print("parse sheet: %s:"% sheet_node.name)
        #self._LayoutStructHead(sheet.name.capitalize() + "Data")
        sheet_name = str(sheet.cell_value(ROW_SHEET_NAME, 0)).strip()
        if len(sheet_name) == 0 :
            print("table%s need a struct name in English at pos(0,0)"% sheet.name)
            exit(-4)
        sheet_node.name = sheet_name

        self._layout.LayoutStructHead(sheet_node.name.capitalize() + "Data")

        col_count = len(sheet.row_values(ROW_STRUCT_DEFINE))
        #print("\tstruct define  count = %d"% col_count)
        for col in range(0, col_count) :
            self._ParseStructDefine(sheet, sheet_node, col)

        direction_mark = str(sheet.cell_value(ROW_DIRECTION, 0)).strip()
        if direction_mark == "type:1" : 
            sheet_node.direction = 1

        if sheet_node.direction == 0:
            col_count = len(sheet.row_values(ROW_FIELD_TYPE))
            #print("\tfield count = %d\n" %col_count)
            for col in range(0, col_count) :
                self._ParseFieldDefine(sheet, sheet_node, col)
        elif sheet_node.direction == 1:
            row_count = len(sheet.col_values(0))
            print("\t type 1 field count = %d" %col_count)
            for row in range(ROW_FIELD_TYPE, row_count) :
                self._ParseFieldDefine2(sheet, sheet_node, row)

        #开始输出
        #print "开始输出"
        self._layout.LayoutBaseFile()
        self._layout.LayoutStructDefines(sheet_node)
        self._layout.LayoutFieldDefines(sheet_node)

        self._layout.LayoutStructTail()

    def _DataParse(self): 
        """读取数据"""
        #self._AddSize(len(self._workbook.sheets())) #sheet_size
        i = 0
        for sheet in self._workbook.sheets():
            self._ReadSheet(sheet, i)
            i+=1

        self._WriteData2File()

    def _ReadSheet(self, sheet, index):
        sheet_node = self._sheets[index]
        #print("read sheet: %s:"% sheet_node.name)
        self._output_data.append("")
        #col_count = len(sheet.row_values(ROW_FIELD_NAME))
        if sheet_node.direction == 0:
            row_count = len(sheet.col_values(0)) 
            #print("field read, col_count = %d"% col_count)
            #print("field read, row_count = %d"% row_count)
            self._AddSize(row_count - ROW_FIELD_DATA_BEGIN, index)     #map_size
            for row in range(ROW_FIELD_DATA_BEGIN, row_count) :
                #print "read sheet: " + str(row)
                self._ReadFields(sheet, sheet_node, row, index)
            print("\tsuccessfull read %d data count"% (row_count - ROW_FIELD_DATA_BEGIN))
        elif sheet_node.direction == 1:
            col_count = len(sheet.row_values(ROW_FIELD_TYPE))
            self._AddSize(col_count - COL_FIELD_DATA_BEGIN, index)
            for col in range(COL_FIELD_DATA_BEGIN, col_count) :
                #print "read sheet: " + str(col)
                self._ReadFields2(sheet, sheet_node, col, index)
            print("\tsuccessfull read %d data count"% (col_count - COL_FIELD_DATA_BEGIN))

        #print type(self._output_data[index])
        #print len(self._output_data[index])
        #print struct.pack("i", len(self._output_data[index]))
        self._output_data[index] = struct.pack("i", len(self._output_data[index])) + self._output_data[index]

    def _ReadFields(self, sheet, sheet_node, row, index): 
        col_count = len(sheet.row_values(ROW_FIELD_DATA_BEGIN))
        for col in range(0, col_count):
            value_string = str(sheet.cell_value(row, col)).strip() 
            self._AddField(sheet_node, value_string, \
                sheet_node.fields[col].name, sheet_node.fields[col].type, index)

    def _ReadFields2(self, sheet, sheet_node, col, index): 
        row_count = len(sheet.col_values(COL_FIELD_DATA_BEGIN))
        for row in range(ROW_FIELD_TYPE, row_count):
            value_string = str(sheet.cell_value(row, col)).strip() 
            self._AddField(sheet_node, value_string, \
                sheet_node.fields[row - ROW_FIELD_TYPE].name, sheet_node.fields[row - ROW_FIELD_TYPE].type, index)

    def _AddField(self, sheet_node, value_string, field_name, field_type, index):
        #print "============================="
        #print value_string
        #print field_name
        #print field_type
        if TypeToInt(field_type) != 0 :
            self._AddData(field_type, value_string, index)
        else :
            struct_node = sheet_node.structs[sheet_node.structs_map[field_type]]
            values = value_string.split(struct_node.delimiter)
            if struct_node.repeated == True :
                self._AddSize(len(values), index)

                for string in values :
                    #print "hehe " + field_name
                    sub_field_node = struct_node.fields[0]
                    self._AddField(sheet_node, string, sub_field_node.name, sub_field_node.type, index)
                    #print "hehe2"
            else :
                for i in range(0,len(struct_node.fields)):
                    sub_field_node = struct_node.fields[i]
                    #print "m1 " + field_name
                    self._AddField(sheet_node, values[i], sub_field_node.name, sub_field_node.type, index)
                    #print "m2"

    def _AddData(self, field_type, value_string, index) :
        type_id = TypeToInt(field_type)
        if type_id == 0 :
            return

        if type_id == 3 :
            #value_string = value_string.encode('utf-8')
            #value_string = value_string.encode('gbk')
            #value_string = unicode(value_string)
            self._output_data[index] += struct.pack("i" + str(len(value_string)) + "s", \
                len(value_string), value_string)
            #print len(value_string)
            #print value_string
        else :
            if len(value_string) == 0 :
                value_string = "0"
            self._output_data[index] += struct.pack(PackFormat(type_id),PythonType(field_type, value_string))

    def _AddSize(self, size, index) :
        self._output_data[index] += struct.pack("i", size)


#Items[#]{item(Item)}
#Reward[,]{items(Items),exp(int)}
    def _ParseStructDefine(self, sheet, sheet_node, col):
        struct_form_string = str(sheet.cell_value(ROW_STRUCT_DEFINE, col)).strip()
        if len(struct_form_string) == 0 :
            return

        i1 = struct_form_string.find('[')
        i2 = struct_form_string.find(']')
        i3 = struct_form_string.find('{')
        i4 = struct_form_string.find('}')

        if i1 < 1 or i2 != i1+2 or i3 != i2+1 or i4 < i3+4 :
            print "struct parse failed at sheet:%s row:%d col:%d value:%s" %(sheet_node.name, ROW_STRUCT_DEFINE, col, struct_form_string)
            print i1
            print i2
            print i3 
            print i4
            sys.exit(-1)

        struct_node = StructNode()
        struct_node.name = struct_form_string[:i1]
        struct_node.delimiter = struct_form_string[i1+1:i2]

        #存入结构列表
        if sheet_node.structs_map.has_key(struct_node.name) :
            print "struct define repeated : " + struct_node.name
            sys.exit(-1)
        sheet_node.structs_map[struct_node.name] = len(sheet_node.structs)
        sheet_node.structs.append(struct_node)

        #解析子结构
        fields = struct_form_string[i3+1:i4].split(",")
        for field in fields:
            f1 = field.find('(')
            f2 = field.find(')')
            if f1 < 1 or f2 < f1+1 : 
                print "fields parse failed at sheet field:" + field
                sys.exit(-1)
            node = FieldNode()
            node.name = field[0:f1]
            node.type = FormatType(field[f1+1:f2])
            if struct_node.fields_map.has_key(node.name):
                print "fields define repeated: " + node.name
                sys.exit(-1)
            struct_node.fields_map[node.name] = len(struct_node.fields)
            struct_node.fields.append(node)

        if len(struct_node.fields) == 1 : 
            struct_node.repeated = True;

    def _ParseFieldDefine(self, sheet, sheet_node, col):
        """解析字段定义区"""
        field_type = str(sheet.cell_value(ROW_FIELD_TYPE, col)).strip()
        field_name = str(sheet.cell_value(ROW_FIELD_NAME, col)).strip()
        field_cname = sheet.cell_value(ROW_FIELD_CNAME, col).encode('utf-8')
        #field_cname = sheet.cell_value(ROW_FIELD_CNAME, col).encode('gbk')
        #field_cname = unicode(sheet.cell_value(ROW_FIELD_CNAME, col))
        if len(field_type) == 0 or len(field_name) == 0 :
            print "sheet:%s field col: %d define null" % (sheet_node.name, col)
            sys.exit(-1)
        type_id = TypeToInt(field_type)
        if col == 0 and type_id != 1 :
            print "sheet:%s please define a int key on the first column." % (sheet_node.name)
            sys.exit(-1)

        if sheet_node.fields_map.has_key(field_name) : 
            print "sheet:%s field: %s define repeated" % (sheet_node.name, field_name)
            sys.exit(-1)
        if type_id == 0 and sheet_node.structs_map.has_key(field_type) == False :
            print "sheet:%s field: %s 's type %s not defined or surported. col %d" % (sheet_node.name, field_name, field_type, col)
            sys.exit(-1)

        field_node = FieldNode()
        field_node.name = field_name
        field_node.type = FormatType(field_type)
        field_node.cname = field_cname
        sheet_node.fields_map[field_name] = len(sheet_node.fields)
        sheet_node.fields.append(field_node)

    def _ParseFieldDefine2(self, sheet, sheet_node, row):
        """解析字段定义区(竖向版)"""
        field_type = str(sheet.cell_value(row, COL_FIELD_TYPE)).strip()
        field_name = str(sheet.cell_value(row, COL_FIELD_NAME)).strip()
        field_cname = sheet.cell_value(row, COL_FIELD_CNAME).encode('utf-8')
        #field_cname = sheet.cell_value(ROW_FIELD_CNAME, col).encode('gbk')
        #field_cname = unicode(sheet.cell_value(ROW_FIELD_CNAME, col))
        if len(field_type) == 0 or len(field_name) == 0 :
            print "sheet:%s field col: %d define null" % (sheet_node.name, col)
            sys.exit(-1)
        type_id = TypeToInt(field_type)
        if row == ROW_FIELD_TYPE and type_id != 1 :
            print "sheet:%s please define a int key on the first column." % (sheet_node.name)
            sys.exit(-1)

        if sheet_node.fields_map.has_key(field_name) : 
            print "sheet:%s field: %s define repeated" % (sheet_node.name, field_name)
            sys.exit(-1)
        if type_id == 0 and sheet_node.structs_map.has_key(field_type) == False :
            print "sheet:%s field: %s 's type %s not defined or surported. col %d" % (sheet_node.name, field_name, field_type, col)
            sys.exit(-1)

        field_node = FieldNode()
        field_node.name = field_name
        field_node.type = FormatType(field_type)
        field_node.cname = field_cname
        sheet_node.fields_map[field_name] = len(sheet_node.fields)
        sheet_node.fields.append(field_node)

    def _WriteData2File(self) :
        if os.path.exists("./data") == False :
            os.mkdir("./data")
        file_name = "./data/" + self._book_name + ".data"
        data_file = open(file_name, 'wb+')
        data_file.writelines(self._output_data)
        data_file.close()
        #print self._output_data
    

if __name__ == '__main__' :
    """入口"""
    #"""
    if len(sys.argv) < 2 :
        print "Usage: %s xls_file" %(sys.argv[0])
        os.system("pause")
        sys.exit(-1)

    xls_file = sys.argv[1]
    #"""
    #xls_file = r".\example1.xls"

    try :
        parser = XlsReader(xls_file)
        parser.Parse()
    except BaseException, e :
        print "parse xls file failed!!!"
        print e
        os.system("pause")
        #raw_input("press <Enter> to exit.")
        sys.exit(-3)

    print "parse xls file success!!!"
    os.system("pause")
    #raw_input("press <Enter> to exit.")


