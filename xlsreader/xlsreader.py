#! /usr/bin/env python
#coding=utf-8

import xlrd # for read excel
import sys
import os

class LogHelp :
    """日志辅助类"""
    _logger = None
    _close_imme = True

    @staticmethod
    def set_close_flag(flag):
        LogHelp._close_imme = flag

    @staticmethod
    def _initlog():
        import logging

        LogHelp._logger = logging.getLogger()
        logfile = 'tnt_comm_deploy_tool.log'
        hdlr = logging.FileHandler(logfile)
        formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(lineno)d|%(funcName)s|%(message)s')
        hdlr.setFormatter(formatter)
        LogHelp._logger.addHandler(hdlr)
        LogHelp._logger.setLevel(logging.NOTSET)
        # LogHelp._logger.setLevel(logging.WARNING)

        LogHelp._logger.info("\n\n\n")
        LogHelp._logger.info("logger is inited!")

    @staticmethod
    def get_logger() :
        if LogHelp._logger is None :
            LogHelp._initlog()

        return LogHelp._logger

    @staticmethod
    def close() :
        if LogHelp._close_imme:
            import logging
            if LogHelp._logger is None :
                return
            logging.shutdown()

# log macro
LOG_DEBUG=LogHelp.get_logger().debug
LOG_INFO=LogHelp.get_logger().info
LOG_WARN=LogHelp.get_logger().warn
LOG_ERROR=LogHelp.get_logger().error


# 行 内容				eg
# #1 表格备注			**活动配置
# #2 自定义结构列表		Item(-){id[int],num[int]}		Reward(#){item[Item]}
# #3 备注				item(id-num) item#item#item		描述说明或内容样本
# #4 类型				Reward							int string uint 自定义结构
# #5 中文名				物品奖励						生成注释
# #6 字段名				reward							生成方法名
ROW_TABLE_DESCRIPTION 	= 0
ROW_STRUCT_DEFINE 		= 1
ROW_FIELD_COMMENT		= 2
ROW_FIELD_TYPE			= 3
ROW_FILED_CNAME			= 4
ROW_FILED_NAME			= 5

struct_name_map = { "struct":0, "int":1, "short":1, "int32":1, "uint":2, "uint32":2, "string":3, "bool":4, "float":5, "double":6 }
type_name_map = { 1:"int32", 2:"uint32", 3:"bytes", 4:"bool", 5:"float", 6:"double"}
def TypeToInt(str):
    if struct_name_map.has_key(str) == True:
        return struct_name_map[str]
    else:
        return 0 

def FormatType(type):
    type_id = TypeToInt(type)
    if type_id != 0 :
        return type_name_map[type_id]
    else : 
        return type

"""
    output type name = 1; 
    parse Item item value
"""
class FieldNode:
    def __init__(self):
        self.name = ""    #节点名
        self.type = 0     #节点类型

class StructNode:
    def __init__(self):
        self.name = ""
        self.delimiter = ""
        self.fields = {}    #node_name: FieldNode

""" message sheet_name
    {
        struct define
        filed_define
    }
"""
class SheetNode:
    def __init__(self):
        self.name = ""
        self.structs = {}   # struct_name: StructNode
        self.fields = {}    # field_name:FieldNode    避免重复

class XlsReader:
    """通过excel配置生成配置的protobuf定义文件"""
    def __init__(self, xls_file_path):
        self._xls_file_path = xls_file_path
        self._tables = {}           # name:TableInfo
        try :
            self._workbook = xlrd.open_workbook(self._xls_file_path)
        except BaseException, e :
            print "open xls file(%s) failed!"%(self._xls_file_path)
            raise

        self._output = []           # 将所有的输出先写到一个list， 最后统一写到文件
        self._indentation = 0       # 排版缩进空格数

        self._pb_file_name = "ly_pb_temp.proto" #"ly_temp_pb_" + self._workbook.file_name + ".proto"        临时文件，不用管中文问题
        self._struct_list = []


    def Parse(self) :
        self._LayoutFileHeader()
        self._output.append("package pb_deploy;\n")

        for sheet in self._workbook.sheets():
            _ParseSheet(sheet)

        self._Write2File()
        LogHelp.close()
   
        try :
            command = "protoc --python_out=./ " + self._pb_file_name
            os.system(command)
        except BaseException, e :
            print "protoc failed!"
            raise

        os.remove(self._pb_file_name)   #remove temperate file

        DataParse()

    def _ParseSheet(self, sheet) :
        self._LayoutStructHead(sheet.sheet_name)
        self._IncreaseIndentation()

        col_count = len(sheet.row_values(ROW_STRUCT_DEFINE))
        LOG_INFO("struct define parse, col_count = %d", col_count)
        for col in range(0, self._col_count) :
            self._ParseStructDefine(sheet, col)

        col_count = len(sheet.row_values(ROW_FIELD_TYPE))
        LOG_INFO("field parse, col_count = %d", col_count)
        for col in range(0, self._col_count) :
            self._ParseFieldDefine(sheet, col)

        #开始输出
        self._LayoutStructDefines(sheet)
        self._LayoutFieldDefines(sheet)

        self._DecreaseIndentation()
        self._LayotuStructTail()

#Items[#]{item(Item)}
#Reward[,]{items(Items),exp(int)}
    def _ParseStructDefine(self, sheet, col):
        struct_form_string = str(sheet.cell_value(ROW_STRUCT_DEFINE, col)).strip()
        i1 = struct_form_string.find('[')
        i2 = struct_form_string.find(']')
        i3 = struct_form_string.find('{')
        i4 = struct_form_string.find('}')

        if i1 < 1 or i2 != i1+2 or i3 != i2+1 or i4 < i3+4 :
            print "struct parse failed at sheet:%s row:%d col:%d" %(sheet.name, ROW_STRUCT_DEFINE, col)
            sys.exit(-1)

        struct_node = StructNode()
        struct_node.name = struct_form_string[:i1]
        struct_node.delimiter = struct_form_string[i1+1:i2]

        #存入结构列表
        if sheet.structs.has_key(struct_node.name) :
            print "struct define repeated : " + struct_node.name
            sys.exit(-1)
        sheet.structs[struct_node.name] = struct_node

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
            if struct_node.fields.has_key(node.name):
                print "fields define repeated: " + node.name
                sys.exit(-1)
            struct_node.fields[node.name] = node

    def _ParseFieldDefine(self, sheet, col):
        field_type = str(sheet.cell_value(ROW_FIELD_TYPE, col)).strip()
        field_name = str(sheet.cell_value(ROW_FIELD_NAME, col)).strip()
        field_cname = unicode(sheet.cell_value(ROW_FIELD_CNAME, col))
        type_id = TypeToInt(field_type)

        if sheet.fields.has_hey(field_name) : 
            print "sheet:%s field: %s define repeated" % (sheet.file_name, field_name)
            sys.exit(-1)
        if type_id == 0 and sheet.structs.has_key(field_type) == False :
            print "sheet:%s field: %s 's type %s not defined or surported." % (sheet.file_name, field_name, field_type)
            sys.exit(-1)

        sheet.fields[field_name] = FormatType(field_type)

    def _LayoutStructDefines(self, sheet):
        for struct_name in sheet.structs :
            struct_node = sheet.structs[struct_name]
            self._LayoutStructHead(struct_node.name)    # Reward  | Items
            self._IncreaseIndentation()
            field_num = 1
            if len(struct_node.fields) == 1 :   # Items
                field_node = struct_node.fields.values()[0]
                self._output.append("\t"*self._indentation + "repeated " + field_node.type +" " + field_name + " = " + str(field_num) + ";\n")
            else :  #Reward{ items, exp }
                for field_name in struct_node.fields :
                   # optional Items items = 1; 
                   field_node = struct_node.fields[field_name]
                   self._output.append("\t"*self._indentation + "optional " + field_node.type +" " + field_name + " = " + str(field_num) + ";\n")
                   field_num += 1
            self._DecreaseIndentation()
            self._LayoutStructTail()


    def _LayoutFieldDefines(self, sheet):

    def old_fielddefine():
        field_type = str(self._sheet.cell_value(FIELD_TYPE_ROW, self._col)).strip()
        field_name = str(self._sheet.cell_value(FIELD_NAME_ROW, self._col)).strip()
        field_comment = unicode(self._sheet.cell_value(FIELD_COMMENT_ROW, self._col))

        LOG_INFO("%s|%s|%s|%s", field_rule, field_type, field_name, field_comment)

        comment = field_comment.encode("utf-8")
        self._LayoutComment(comment)

        if repeated_num >= 1:
            field_rule = "repeated"

            self._LayoutOneField(field_rule, field_type, field_name)

            actual_repeated_num = 1 if (repeated_num == 0) else repeated_num
            self._col += actual_repeated_num

        elif field_rule == "repeated" :
            # 2011-11-29 修改
            # 若repeated第二行是类型定义，则表示当前字段是repeated，并且数据在单列用分好相隔
            second_row = str(self._sheet.cell_value(FIELD_TYPE_ROW, self._col)).strip()
            LOG_DEBUG("repeated|%s", second_row);
            # exel有可能有小数点
            if second_row.isdigit() or second_row.find(".") != -1 :
                # 这里后面一般会是一个结构体
                repeated_num = int(float(second_row))
                LOG_INFO("%s|%d", field_rule, repeated_num)
                self._col += 1
                self._FieldDefine(repeated_num)
            else :
                # 一般是简单的单字段，数值用分号相隔
                field_type = second_row
                field_name = str(self._sheet.cell_value(FIELD_NAME_ROW, self._col)).strip()
                field_comment = unicode(self._sheet.cell_value(FIELD_COMMENT_ROW, self._col))
                LOG_INFO("%s|%s|%s|%s", field_rule, field_type, field_name, field_comment)

                comment = field_comment.encode("utf-8")
                self._LayoutComment(comment)

                self._LayoutOneField(field_rule, field_type, field_name)

                self._col += 1

        elif field_rule == "required_struct" or field_rule == "optional_struct":
            field_num = int(self._sheet.cell_value(FIELD_TYPE_ROW, self._col))
            struct_name = str(self._sheet.cell_value(FIELD_NAME_ROW, self._col)).strip()
            field_name = str(self._sheet.cell_value(FIELD_COMMENT_ROW, self._col)).strip()

            LOG_INFO("%s|%d|%s|%s", field_rule, field_num, struct_name, field_name)


            if (self._IsStructDefined(struct_name)) :
                self._is_layout = False
            else :
                self._struct_name_list.append(struct_name)
                self._is_layout = True

            col_begin = self._col
            self._StructDefine(struct_name, field_num)
            col_end = self._col

            self._is_layout = True

            if repeated_num >= 1:
                field_rule = "repeated"
            elif field_rule == "required_struct":
                field_rule = "required"
            else:
                field_rule = "optional"

            self._LayoutOneField(field_rule, struct_name, field_name)

            actual_repeated_num = 1 if (repeated_num == 0) else repeated_num
            self._col += (actual_repeated_num-1) * (col_end-col_begin)
        else :
            self._col += 1
            return

    def _LayoutFileHeader(self) :
        """生成PB文件的描述信息"""
        self._output.append("/**\n")
        self._output.append("* @file:   " + self._pb_file_name + "\n")
        self._output.append("* @author: SeanLiu <darkdawn@sina.com>\n")
        self._output.append("* @brief:  The file is generated by tools. Don't modify it.n")
        self._output.append("*/\n")
        self._output.append("\n")


    def _LayoutStructHead(self, struct_name) :
        """生成结构头"""
        if not self._is_layout :
            return
        self._output.append("\n")
        self._output.append("\t"*self._indentation + "message " + struct_name + "{\n")

    def _LayoutStructTail(self) :
        """生成结构尾"""
        self._output.append("\t"*self._indentation + "}\n")
        self._output.append("\n")

    def _LayoutComment(self, comment) :
        # 改用C风格的注释，防止会有分行
        if not self._is_layout :
            return
        if comment.count("\n") > 1 :
            if comment[-1] != '\n':
                comment = comment + "\n"
                comment = comment.replace("\n", "\n" + "\t" * (self._indentation + TAP_BLANK_NUM),
                        comment.count("\n")-1 )
                self._output.append("\t"*self._indentation + "/** " + comment + "\t"*self._indentation + "*/\n")
        else :
            self._output.append("\t"*self._indentation + "/** " + comment + " */\n")

    def _LayoutOneField(self, field_rule, field_type, field_name) :
        """输出一行定义"""
        if not self._is_layout :
            return
        if field_name.find('=') > 0 :
            name_and_value = field_name.split('=')
            self._output.append("\t"*self._indentation + field_rule + " " + field_type \
                    + " " + str(name_and_value[0]).strip() + " = " + self._GetAndAddFieldIndex()\
                    + " [default = " + str(name_and_value[1]).strip() + "]" + ";\n")
            return

        if (field_rule != "required" and field_rule != "optional") :
            self._output.append("\t"*self._indentation + field_rule + " " + field_type \
                    + " " + field_name + " = " + self._GetAndAddFieldIndex() + ";\n")
            return

        if field_type == "int32" or field_type == "int64"\
                or field_type == "uint32" or field_type == "uint64"\
                or field_type == "sint32" or field_type == "sint64"\
                or field_type == "fixed32" or field_type == "fixed64"\
                or field_type == "sfixed32" or field_type == "sfixed64" \
                or field_type == "double" or field_type == "float" :
                    self._output.append("\t"*self._indentation + field_rule + " " + field_type \
                            + " " + field_name + " = " + self._GetAndAddFieldIndex()\
                            + " [default = 0]" + ";\n")
        elif field_type == "string" or field_type == "bytes" :
            self._output.append("\t"*self._indentation + field_rule + " " + field_type \
                    + " " + field_name + " = " + self._GetAndAddFieldIndex()\
                    + " [default = \"\"]" + ";\n")
        else :
            self._output.append("\t"*self._indentation + field_rule + " " + field_type \
                    + " " + field_name + " = " + self._GetAndAddFieldIndex() + ";\n")
        return

    def _IncreaseIndentation(self) :
        """增加缩进"""
        self._indentation += 1

    def _DecreaseIndentation(self) :
        """减少缩进"""
        self._indentation -= 1

    def _Write2File(self) :
        """输出到文件"""
        pb_file = open(self._pb_file_name, "w+")
        pb_file.writelines(self._output)
        pb_file.close()


class DataReader:
    """解析excel的数据"""
    def __init__(self, xls_file_path, sheet_name):
        self._xls_file_path = xls_file_path
        self._sheet_name = sheet_name

        try :
            self._workbook = xlrd.open_workbook(self._xls_file_path)
        except BaseException, e :
            print "open xls file(%s) failed!"%(self._xls_file_path)
            raise

        try :
            self._sheet =self._workbook.sheet_by_name(self._sheet_name)
        except BaseException, e :
            print "open sheet(%s) failed!"%(self._sheet_name)
            raise

        self._row_count = len(self._sheet.col_values(0))
        self._col_count = len(self._sheet.row_values(0))

        self._row = 0
        self._col = 0

        try:
            self._module_name = "tnt_deploy_" + self._sheet_name.lower() + "_pb2"
            sys.path.append(os.getcwd())
            exec('from '+self._module_name + ' import *');
            self._module = sys.modules[self._module_name]
        except BaseException, e :
            print "load module(%s) failed"%(self._module_name)
            raise

    def Read(self) :
        """对外的接口:解析数据"""
        LOG_INFO("begin parse, row_count = %d, col_count = %d", self._row_count, self._col_count)

        item_array = getattr(self._module, self._sheet_name+'_ARRAY')()

        # 先找到定义ID的列
        id_col = 0
        for id_col in range(0, self._col_count) :
            info_id = str(self._sheet.cell_value(self._row, id_col)).strip()
            if info_id == "" :
                continue
            else :
                break

        for self._row in range(4, self._row_count) :
            # 如果 id 是 空 直接跳过改行
            info_id = str(self._sheet.cell_value(self._row, id_col)).strip()
            if info_id == "" :
                LOG_WARN("%d is None", self._row)
                continue
            item = item_array.items.add()
            self._ParseLine(item)

        LOG_INFO("parse result:\n%s", item_array)

        self._WriteReadableData2File(str(item_array))

        data = item_array.SerializeToString()
        self._WriteData2File(data)


        #comment this line for test .by kevin at 2013年1月12日 17:23:35
        LogHelp.close()

    def _ParseLine(self, item) :
        LOG_INFO("%d", self._row)

        self._col = 0
        while self._col < self._col_count :
            self._ParseField(0, 0, item)

    def _ParseField(self, max_repeated_num, repeated_num, item) :
        field_rule = str(self._sheet.cell_value(0, self._col)).strip()

        if field_rule == "required" or field_rule == "optional" :
            field_name = str(self._sheet.cell_value(2, self._col)).strip()
            if field_name.find('=') > 0 :
                name_and_value = field_name.split('=')
                field_name = str(name_and_value[0]).strip()
            field_type = str(self._sheet.cell_value(1, self._col)).strip()

            LOG_INFO("%d|%d", self._row, self._col)
            LOG_INFO("%s|%s|%s", field_rule, field_type, field_name)

            if max_repeated_num == 0 :
                field_value = self._GetFieldValue(field_type, self._row, self._col)
                # 有value才设值
                if field_value != None :
                    item.__setattr__(field_name, field_value)
                self._col += 1
            else :
                if repeated_num == 0 :
                    if field_rule == "required" :
                        print "required but repeated_num = 0"
                        raise
                else :
                    for col in range(self._col, self._col + repeated_num):
                        field_value = self._GetFieldValue(field_type, self._row, col)
                        # 有value才设值
                        if field_value != None :
                            item.__getattribute__(field_name).append(field_value)
                self._col += max_repeated_num

        elif field_rule == "repeated" :
            # 2011-11-29 修改
            # 若repeated第二行是类型定义，则表示当前字段是repeated，并且数据在单列用分好相隔
            second_row = str(self._sheet.cell_value(FIELD_TYPE_ROW, self._col)).strip()
            LOG_DEBUG("repeated|%s", second_row);
            # exel有可能有小数点
            if second_row.isdigit() or second_row.find(".") != -1 :
                # 这里后面一般会是一个结构体
                max_repeated_num = int(float(second_row))
                read = self._sheet.cell_value(self._row, self._col)
                repeated_num = 0 if read == "" else int(self._sheet.cell_value(self._row, self._col))

                LOG_INFO("%s|%d|%d", field_rule, max_repeated_num, repeated_num)

                if max_repeated_num == 0 :
                    print "max repeated num shouldn't be 0"
                    raise

                if repeated_num > max_repeated_num :
                    repeated_num = max_repeated_num

                self._col += 1
                self._ParseField(max_repeated_num, repeated_num, item)

            else :
                # 一般是简单的单字段，数值用分号相隔
                # 一般也只能是数字类型
                field_type = second_row
                field_name = str(self._sheet.cell_value(FIELD_NAME_ROW, self._col)).strip()
                field_value_str = unicode(self._sheet.cell_value(self._row, self._col))
                #field_value_str = unicode(self._sheet.cell_value(self._row, self._col)).strip()

                # LOG_INFO("%d|%d|%s|%s|%s",
                #         self._row, self._col, field_rule, field_type, field_name, field_value_str)

                #2013-01-24 jamey
                #增加长度判断
                if len(field_value_str) > 0:
                    if field_value_str.find(";\n") > 0 :
                        field_value_list = field_value_str.split(";\n")
                    else :
                        field_value_list = field_value_str.split(";")

                    for field_value in field_value_list :
                        if field_type == "bytes":
                            item.__getattribute__(field_name).append(field_value.encode("utf8"))
                        else:
                            item.__getattribute__(field_name).append(int(float(field_value)))

                self._col += 1

        elif field_rule == "required_struct" or field_rule == "optional_struct":
            field_num = int(self._sheet.cell_value(FIELD_TYPE_ROW, self._col))
            struct_name = str(self._sheet.cell_value(FIELD_NAME_ROW, self._col)).strip()
            field_name = str(self._sheet.cell_value(FIELD_COMMENT_ROW, self._col)).strip()

            LOG_INFO("%s|%d|%s|%s", field_rule, field_num, struct_name, field_name)


            col_begin = self._col

            # 至少循环一次
            if max_repeated_num == 0 :
                struct_item = item.__getattribute__(field_name)
                self._ParseStruct(field_num, struct_item)

            else :
                if repeated_num == 0 :
                    if field_rule == "required_struct" :
                        print "required but repeated_num = 0"
                        raise
                    # 先读取再删除掉
                    struct_item = item.__getattribute__(field_name).add()
                    self._ParseStruct(field_num, struct_item)
                    item.__getattribute__(field_name).__delitem__(-1)

                else :
                    for num in range(0, repeated_num):
                        struct_item = item.__getattribute__(field_name).add()
                        self._ParseStruct(field_num, struct_item)

            col_end = self._col

            max_repeated_num = 1 if (max_repeated_num == 0) else max_repeated_num
            actual_repeated_num = 1 if (repeated_num==0) else repeated_num
            self._col += (max_repeated_num - actual_repeated_num) * ((col_end-col_begin)/actual_repeated_num)

        else :
            self._col += 1
            return

    def _ParseStruct(self, field_num, struct_item) :
        """嵌套结构数据读取"""

        # 跳过结构体定义
        self._col += 1
        while field_num > 0 :
            self._ParseField(0, 0, struct_item)
            field_num -= 1

    def _GetFieldValue(self, field_type, row, col) :
        """将pb类型转换为python类型"""

        field_value = self._sheet.cell_value(row, col)
        LOG_INFO("%d|%d|%s", row, col, field_value)

        try:
            if field_type == "int32" or field_type == "int64"\
                    or  field_type == "uint32" or field_type == "uint64"\
                    or field_type == "sint32" or field_type == "sint64"\
                    or field_type == "fixed32" or field_type == "fixed64"\
                    or field_type == "sfixed32" or field_type == "sfixed64" :
                        if len(str(field_value).strip()) <=0 :
                            return None
                        else :
                            return int(field_value)
            elif field_type == "double" or field_type == "float" :
                    if len(str(field_value).strip()) <=0 :
                        return None
                    else :
                        return float(field_value)
            elif field_type == "string" :
                field_value = unicode(field_value)
                if len(field_value) <= 0 :
                    return None
                else :
                    return field_value
            elif field_type == "bytes" :
                field_value = unicode(field_value).encode('utf-8')
                if len(field_value) <= 0 :
                    return None
                else :
                    return field_value
            else :
                return None
        except BaseException, e :
            print "parse cell(%u, %u) error, please check it, maybe type is wrong."%(row, col)
            raise

    def _WriteData2File(self, data) :
        file_name = "tnt_deploy_" + self._sheet_name.lower() + ".data"
        file = open(file_name, 'wb+')
        file.write(data)
        file.close()

    def _WriteReadableData2File(self, data) :
        file_name = "tnt_deploy_" + self._sheet_name.lower() + ".txt"
        file = open(file_name, 'wb+')
        file.write(data)
        file.close()



if __name__ == '__main__' :
    """入口"""
    if len(sys.argv) < 3 :
        print "Usage: %s xls_file" %(sys.argv[0])
        sys.exit(-1)

    xls_file = sys.argv[1]

    try :
        parser = XlsReader(xls_file)
        parser.Parse()
    except BaseException, e :
        print "parse xls file failed!!!"
        print e
        sys.exit(-3)

    print "parse xls file success!!!"


