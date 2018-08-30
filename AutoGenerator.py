#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a interprocess communication code generator which use header file XX4A_if.h XX4A_type.h  '
from symbol import parameters

__author__ = 'Weiwang Sun'

import sys, re, getopt, os
import time
import codecs
import shutil


def type_to_size(type="ZOO_INT32", array=''):
    if type == "ZOO_INT32":
        return 4
    if type == "ZOO_UINT32":
        return 4
    if type == "ZOO_CHAR":
        if "[" in array:
            len = int(array.split("[")[1].split("]")[0])
            # print("len :" + str(len))
            return 8
        else:
            return 1
    if type == "ZOO_DOUBLE":
        return 8
    if type == "ZOO_INT16":
        return 4
    if type == "ZOO_UINT16":
        return
    if type == "ZOO_FLOAT":
        return 8
    if "enum" in type:
        return 4
    if "ENUM" in type:
        return 4
    if "STRUCT" in type:
        return 8
    if "struct" in type:
        return 8
    if "int" in type:
        return 4
    if "unsigned int" in type:
        return 4
    if "CALLBACK_FUNCTION" in type:
        return 4
    if "bool" in type:
        return 1
    return 4


def str_to_hex(s):
    return ''.join([hex(ord(c)).replace('0x', '') for c in s])


class ENVIRONMENT_CLASS(object):
    def __init__(self):
        self._current_path = os.getcwd()

    def get_current_path(self):
        return self._current_path


class COMMENT_CLASS(object):
    def __init__(self, comment=None):
        self._str = comment

    def get_string(self):
        return '/* ' + self._str + ' */'

    def get_comment(self, comment):
        return '/**' + '\n' + ' *@brief ' + comment + '\n' + '**/' + '\n'

    def get_comment_param(self, comment, parameters=[]):
        buffer = '/**' + '\n' + ' *@brief ' + comment + '\n'
        for s in parameters:
            p = ' *@param ' + s + '\n'
            buffer = buffer + s
        buffer = buffer + '**/' + '\n'
        return buffer


class FILE_HEADER_COMMENT_CLASS(object):
    def __init__(self, product='', component_id='', filename='', description='{Summary Description}',
                 author='Generator', context='created'):
        self._product = product
        self._component_id = component_id
        self._filename = filename
        self._description = description
        self._version = 'V1.0.0'
        self._date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self._author = author
        self._context = context

    def add_property(self, product, component_id, filename, description, author, context):
        self._product = product
        self._component_id = component_id
        self._filename = filename
        self._description = description
        self._author = author
        self._context = context

    def get_list(self):
        tmplist = []
        tmplist.append('/***********************************************************')
        tmplist.append(' * Copyright (C) 2018, shanghai NIO CO. ,LTD')
        tmplist.append(' * All rights reserved.')
        tmplist.append(' * Product        : ' + self._product)
        tmplist.append(' * Component id   : ' + self._component_id)
        tmplist.append(' * File Name      : ' + self._filename)
        tmplist.append(' * Description    : ' + self._description)
        tmplist.append(' * History        : ')
        tmplist.append(' * Version        date          auther         context ')
        tmplist.append(
            ' * ' + self._version + '         ' + self._date + '    ' + self._author + '      ' + self._context)
        tmplist.append('*************************************************************/')
        return tmplist


class FILE_INCLUDE_CLASS(object):
    def __init__(self, filelist=[]):
        self._filelist = filelist

    def add_property(self, filelist):
        self._filelist = filelist

    def get_list(self):
        tmplist = []
        if self._filelist:
            for fl in self._filelist:
                if "st" in fl or "std" in fl or "MQ" in fl or "ZOO" in fl or "MM" in fl or "CM" in fl or "BD" in fl or "EH" in fl or "TR" in fl:
                    tmplist.append('#include ' + '<' + fl + '>')
                else:
                    tmplist.append('#include ' + '"' + fl + '"')
        return tmplist


def get_ifndef(file_name):
    convert = file_name.upper().replace(".", "_")
    st = "#ifndef " + convert + "\n#define " + convert + "\n"
    return st


def get_endif(file_name):
    st = "#endif // " + file_name + "\n"
    return st


class MEMBER_CLASS:
    def __init__(self, type='', name=''):
        self._type = type
        self._name = name

    def get_type(self):
        return self._type

    def get_name(self):
        return self._name


class ENUM_CLASSS:
    def __init__(self, name='', member=[]):
        self._name = name
        self._member = member

    def get_name(self):
        return self._name

    def get_members(self):
        return self._member


class STRUCT_CLASSS:
    def __init__(self, str=''):
        self._str = str

    def get_member_list(self):
        tmp = []
        double_slash_patten = re.compile(r'//.*')
        slash_star_patten = re.compile(r'/\*.*?\*/')
        name_patten = re.compile(r"(\w\w4\w\_\w*\_STRUCT)")
        mem_patten = re.compile(r"(\w*\s+\w*;)+")
        s = re.sub(double_slash_patten, ' ', self._str)
        x = re.sub(slash_star_patten, '', s)
        m = re.sub('[\r\n\t]', '', x)
        # print(m)
        name = name_patten.findall(m)
        # print(name)
        r = mem_patten.findall(m)
        # print(r )
        for mm in r:
            tmp.append(mm)
        return tmp

    def get_member(self, member=''):
        v_patten = re.compile(r"(\w*)\s+(\w*)")
        y = v_patten.findall(member)
        # print(y)
        return MEMBER_CLASS(y[0][0], y[0][1])


# *
# @brief function parameters class define
# *
class PARAMETERS_CLASS:
    def __init__(self, direction='IN', type='888', name='xxxx'):
        self._direction = direction
        self._type = type
        self._name = name

    def get_type(self):
        return self._type

    def get_name(self):
        return self._name

    def get_direction(self):
        return self._direction

    def remove_square_brackets(self):
        result = self._name
        if '[' in self._name:
            brackets_patten = re.compile(r"[a-zA-Z0-9\_]+[^[]")
            m = brackets_patten.findall(self._name)
            print(m[0])
            result = m[0]
        return result

    def remove_variable_with_asterisk(self):
        result = self._name
        return result.strip("*")

    def check_variable_contain_square_brackets(self):
        if '[' in self._name:
            return 1
        return 0

    def get_name_without_asterisk(self):
        result = self._name
        return result.strip("*")

    def get_name_without_square_brackets(self):
        result = self._name
        if '[' in self._name:
            r = self._name.strip().split("[")
            result = r[0]
        return result

    def get_name_with_square_brackets_header_addr(self):
        result = self._name
        if '[' in self._name:
            r = self._name.strip().split("[")
            result = r[0] + "[0]"
        return result

    def get_array_length(self):
        result = ''
        length = []
        if '[' in self._name:
            brackets_patten = re.compile(r"(\[(.*?)\])")
            length = brackets_patten.findall(self._name)
            # print(length)
        if len(length) > 1:
            result = length[0][1] + " * " + length[1][1]
        else:
            result = length[0][1]
        return result


# *
# @brief function class define
# *
class FUNCTION_CLASS:
    def __init__(self, function='', code_index=1):
        self._function = function
        self._input_parameters = []
        self._output_parameters = []
        self._inoutput_parameters = []
        self._interface_type = 'Sync'
        self._return_type = 'ZOO_INT32'
        self._name = ''
        self._code_index = code_index
        self._in_flag = 0
        self._out_flag = 0
        self._inout_flag = 0
        self.get_function_name()
        if function != '':
            self.get_input_parameters_list()
            self.get_output_parameters_list()
            self.get_inoutput_parameters_list()

    def get_comment(self, comment=''):
        buffer = '/**' + '\n' + ' *@brief ' + comment + '\n'

        for s in self._input_parameters:
            p = ' *@param ' + s.get_name() + '\n'
            buffer = buffer + p

        for s in self._output_parameters:
            p = ' *@param ' + s.get_name() + '\n'
            buffer = buffer + p

        for s in self._inoutput_parameters:
            p = ' *@param ' + s.get_name() + '\n'
            buffer = buffer + p

        buffer = buffer + '**/' + '\n'
        return buffer

    def get_body(self, component_id=''):
        body = "{\n" \
               "    TR4A_trace( COMPONENT_ID_" + component_id + ", __ZOO_FUNC__, \"> function entry ... \");\n" \
                "    ZOO_INT32 result = OK;\n" \
                "    " + component_id + "4I_REQUEST_STRUCT *request_message = NULL;/* 消息发送参数*/ \n" \
                "    " + component_id + "4I_REPLY_STRUCT *reply_message = NULL;	/* 接收参数*/\n" \
                "    ZOO_INT32 ZOO_timeout = 60;\n" \
                "    ZOO_INT32 request_length = 0;/*发送消息长度*/\n" \
                "    ZOO_INT32 reply_length = 0;/*应该接收消息长度*/\n" \
                "    ZOO_INT32 func_code = " + self.get_function_code_upper() + ";\n" \
                "    result = " + component_id + "4I_get_request_message_length(func_code, &request_length);\n" \
                "    if(OK == result)\n" \
                "    {\n" \
                "        request_message = (" + component_id + "4I_REQUEST_STRUCT *)MM4A_malloc(request_length);\n" \
                "    }\n\n" \
                "    if(OK == result)\n" \
                "    {\n" \
                "        if(request_message == NULL)\n" \
                "        {\n" \
                "            result = " + component_id + "4A_PARAMETER_ERR;\n" \
                "        }\n" \
                "    }\n\n" \
                "    if(OK == result)\n" \
                "    {\n" \
                "        result = " + component_id + "4I_get_reply_message_length(func_code, &reply_length);\n" \
                "    }\n\n" \
                "    if(OK == result)\n" \
                "    {\n" \
                "        reply_message = (" + component_id + "4I_REPLY_STRUCT *)MM4A_malloc(reply_length);\n" \
                "    }\n\n" \
                "    if(OK == result)\n" \
                "    {\n" \
                "        if(reply_message == NULL)\n" \
                "        {\n" \
                "            result = " + component_id + "4A_PARAMETER_ERR;\n" \
                "        }\n" \
                "    }\n\n" \
                "    if(OK == result)\n" \
                "    {\n" \
                "        request_message->request_header.function_code = func_code;\n"\
                "        reply_message->reply_header.function_code = func_code;\n"

        if "_sig" in self._function:
            body = body + "        request_message->request_header.need_reply = ZOO_FALSE;\n"
        else:
            body = body + "        request_message->request_header.need_reply = ZOO_TRUE;\n"

        for pm in self._input_parameters:
            if pm.check_variable_contain_square_brackets():
                body = body + "        memcpy((void *)(&request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + "),&" + pm.get_name_with_square_brackets_header_addr() + ",sizeof(" + pm.get_type() + ") * " + pm.get_array_length() + ");\n"
            elif "*" in pm.get_type():
                if "CHAR" in pm.get_type() or "char" in pm.get_type():
                    body = body + "        memcpy((void *)(request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name() + ")," + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + ") * " + component_id + "4I_BUFFER_LENGTH" + ");\n"
                else:
                    body = body + "        memcpy((void *)(request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name() + ")," + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + "));\n"
            else:
                body = body + "        memcpy((void *)(&request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name() + "),&" + pm.get_name() + ",sizeof(" + pm.get_type() + "));\n"

        if "_sig" in self._function:
            body = body + "    }\n\n" \
                          "    if(OK == result)\n" \
                          "    {\n" \
                          "        result = " + component_id + "4I_send_signal(" + component_id + "4A_SERVER,request_message,request_length);\n" \
                          "    }\n\n" \
                          "    if(OK == result)\n" \
                          "    {\n" \
                          "        result = reply_message->reply_header.execute_result;\n"
        else :
            body = body + "    }\n\n" \
                          "    if(OK == result)\n" \
                          "    {\n" \
                          "        result = " + component_id + "4I_send_request_and_reply(" + component_id + "4A_SERVER,request_message,reply_message,ZOO_timeout);\n" \
                                                                                                             "    }\n\n" \
                                                                                                             "    if(OK == result)\n" \
                                                                                                             "    {\n" \
                                                                                                             "        result = reply_message->reply_header.execute_result;\n"
            for pm in self._output_parameters:
                if pm.check_variable_contain_square_brackets():
                    body = body + "        memcpy(&" + pm.get_name_with_square_brackets_header_addr() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + ",sizeof(" + pm.get_type() + ") * " + pm.get_array_length() + ");\n"
                elif "*" in pm.get_type():
                    if "CHAR" in pm.get_type() or "char" in pm.get_type():
                        body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                            "const").strip().strip("*") + ") * " + component_id + "4I_BUFFER_LENGTH" + ");\n"
                    else:
                        body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                            "const").strip().strip("*") + "));\n"
                else:
                    body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type() + "));\n"

            for pm in self._inoutput_parameters:
                if pm.check_variable_contain_square_brackets():
                    body = body + "        memcpy(&" + pm.get_name_with_square_brackets_header_addr() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + ",sizeof(" + pm.get_type() + ") * " + pm.get_array_length() + ");\n"
                elif "*" in pm.get_type():
                    if "CHAR" in pm.get_type() or "char" in pm.get_type():
                        body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                            "const").strip().strip("*") + ") * " + component_id + "4I_BUFFER_LENGTH" + ");\n"
                    else:
                        body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                            "const").strip().strip("*") + "));\n"
                else:
                    body = body + "        memcpy(" + pm.get_name().strip(
                        "*") + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name().strip(
                        "*") + ",sizeof(" + pm.get_type() + "));\n"

        body = body + "    }\n\n" \
                      "    MM4A_free(request_message);\n" \
                      "    MM4A_free(reply_message);\n" \
                      "    TR4A_trace( COMPONENT_ID_" + component_id + ", __ZOO_FUNC__, \"< function exit ...\" );\n" \
                                                                       "    return result;\n}\n"
        return body

    def get_body_req(self, component_id=''):
        body = "{\n" \
               "    TR4A_trace( COMPONENT_ID_" + component_id + ", __ZOO_FUNC__, \"> function entry ... \");\n" \
            "    ZOO_INT32 result = OK;\n" \
            "    " + component_id + "4I_REQUEST_STRUCT *request_message = NULL;/* 消息发送参数*/ \n" \
            "    ZOO_INT32 req_length = 0;/*发送消息长度*/\n" \
            "    ZOO_INT32 func_code = " + self.get_function_code_upper().replace(
            "_REQ", "") + ";\n" \
            "    result = " + component_id + "4I_get_request_message_length(func_code, &req_length);\n" \
            "    if(OK == result)\n" \
            "    {\n" \
            "        request_message = (" + component_id + "4I_REQUEST_STRUCT *)MM4A_malloc(req_length);\n" \
            "    }\n\n" \
            "    if(OK == result)\n" \
            "    {\n" \
            "        if(request_message == NULL)\n" \
            "        {\n" \
            "            result = " + component_id + "4A_PARAMETER_ERR;\n" \
            "        }\n" \
            "    }\n\n" \
            "    if(OK == result)\n" \
            "    {\n" \
            "        request_message->request_header.function_code = func_code;\n" \
            "        request_message->request_header.need_reply = ZOO_TRUE;\n"

        for pm in self._input_parameters:
            if pm.check_variable_contain_square_brackets():
                body = body + "        memcpy((void *)(&request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + "),&" + pm.get_name_with_square_brackets_header_addr() + ",sizeof(" + pm.get_type() + ") * " + pm.get_array_length() + ");\n"
            elif "*" in pm.get_type():
                if "CHAR" in pm.get_type() or "char" in pm.get_type():
                    body = body + "        memcpy((void *)(request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name() + ")," + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + ") * " + component_id + "4I_BUFFER_LENGTH" + ");\n"
                else:
                    body = body + "        memcpy((void *)(request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name() + ")," + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + "));\n"
            else:
                body = body + "        memcpy((void *)(&request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name() + "),&" + pm.get_name() + ",sizeof(" + pm.get_type() + "));\n"

        body = body + "    }\n\n" \
                      "    if(OK == result)\n" \
                      "    {\n" \
                      "        result = " + component_id + "4I_send_request_message(" + component_id + "4A_SERVER,request_message);\n"

        body = body + "    }\n\n" \
                      "    MM4A_free(request_message);\n" \
                      "    TR4A_trace( COMPONENT_ID_" + component_id + ", __ZOO_FUNC__, \"< function exit ...\" );\n" \
                                                                       "    return result;\n}\n"
        return body

    def get_body_wait(self, component_id=''):
        body = "{\n" \
               "    TR4A_trace( COMPONENT_ID_" + component_id + ", __ZOO_FUNC__, \"> function entry ... \");\n" \
                                                                "    ZOO_INT32 result = OK;\n" \
                                                                "    " + component_id + "4I_REPLY_STRUCT *reply_message = NULL;	/* 接收参数*/\n" \
                                                                                        "    ZOO_INT32 ZOO_timeout = 60;\n" \
                                                                                        "    ZOO_INT32 reply_length = 0;/*应该接收消息长度*/\n" \
                                                                                        "    ZOO_INT32 func_code = " + self.get_function_code_upper().replace(
            "_WAIT", "") + ";\n" \
                           "    if(OK == result)\n" \
                           "    {\n" \
                           "        result = " + component_id + "4I_get_reply_message_length(func_code, &reply_length);\n" \
                           "    }\n\n" \
                           "    if(OK == result)\n" \
                           "    {\n" \
                           "        reply_message = (" + component_id + "4I_REPLY_STRUCT *)MM4A_malloc(reply_length);\n" \
                           "    }\n\n" \
                           "    if(OK == result)\n" \
                           "    {\n" \
                           "        if(reply_message == NULL)\n" \
                           "        {\n" \
                           "            result = " + component_id + "4A_PARAMETER_ERR;\n" \
                           "        }\n" \
                           "    }\n\n"
        body = body + "    if(OK == result)\n" \
                      "    {\n" \
                      "        result = " + component_id + "4I_receive_reply_message(" + component_id + "4A_SERVER,func_code,reply_message,ZOO_timeout);\n" \
                      "    }\n\n" \
                      "    if(OK == result)\n" \
                      "    {\n" \
                      "        result = reply_message->reply_header.execute_result;\n"

        for pm in self._output_parameters:
            if pm.check_variable_contain_square_brackets():
                body = body + "        memcpy(&" + pm.get_name_with_square_brackets_header_addr() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + ",sizeof(" + pm.get_type() + ") * " + pm.get_array_length() + ");\n"
            elif "*" in pm.get_type():
                if "CHAR" in pm.get_type() or "char" in pm.get_type():
                    body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + ") * " + component_id + "4I_BUFFER_LENGTH" + ");\n"
                else:
                    body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + "));\n"
            else:
                body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type() + "));\n"

        for pm in self._inoutput_parameters:
            if pm.check_variable_contain_square_brackets():
                body = body + "        memcpy(&" + pm.get_name_with_square_brackets_header_addr() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + ",sizeof(" + pm.get_type() + ") * " + pm.get_array_length() + ");\n"
            elif "*" in pm.get_type():
                if "CHAR" in pm.get_type() or "char" in pm.get_type():
                    body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + ") * " + component_id + "4I_BUFFER_LENGTH" + ");\n"
                else:
                    body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + "));\n"
            else:
                body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type() + "));\n"

        body = body + "    }\n\n" \
                      "    MM4A_free(reply_message);\n" \
                      "    TR4A_trace( COMPONENT_ID_" + component_id + ", __ZOO_FUNC__, \"< function exit ...\" );\n" \
                                                                       "    return result;\n}\n"
        return body

    def convert_func_name(self, new=''):
        old = self._function
        f = self._function
        x = f.replace(old, new)
        y = x.replace(';', "")
        # print(y)
        return y

    def get_func_declaration(self):

        return self._function.replace("ZOO_EXPORT","").replace(";","")

    def get_local_name(self):
        l = self._name.split("4")
        id = l[0]
        name = id + "MA_local_4" + l[1]
        return name

    # static void XXMA_local_4A_initialize(const MQ4A_SERV_ADDR server,XX4I_REQUEST_STRUCT * request,XX4I_REPLY_STRUCT * reply)
    def get_local_function_definition(self, component_id=''):
        buffer = "static void " + self.get_local_name() + "("
        buffer = buffer + "const MQ4A_SERV_ADDR server," + component_id + "4I_REQUEST_STRUCT * request," + component_id + "4I_REPLY_STRUCT * reply"
        buffer = buffer + ");\n"
        return buffer

    # const MQ4A_SERV_ADDR server,XX4I_REQUEST_STRUCT * request,XX4I_REPLY_STRUCT * reply
    def get_local_function(self, component_id=''):
        buffer = "static void " + self.get_local_name() + "("
        buffer = buffer + "const MQ4A_SERV_ADDR server," + component_id + "4I_REQUEST_STRUCT * request," + component_id + "4I_REPLY_STRUCT * reply"
        buffer = buffer + ")"
        return buffer

    def get_local_function_body(self, component_id=''):
        body = ''
        body = body + "\n{ \n"
        body = body + "    TR4A_trace( COMPONENT_ID_" + component_id + ", __ZOO_FUNC__, \"> function entry ... \");\n"
        body = body + "    ZOO_INT32 rtn = OK;\n" \
                      "    if(request == NULL)\n" \
                      "    {\n" \
                      "        EH4A_show_exception(COMPONENT_ID_" + component_id + ",__FILE__,__ZOO_FUNC__,__LINE__," + component_id + "4A_PARAMETER_ERR,\"request pointer is NULL ...ERROR\");\n" \
                                                                                                                                       "    }\n\n" \
                                                                                                                                       "    if(OK == rtn)\n" \
                                                                                                                                       "    {\n" \
                                                                                                                                       "        reply->reply_header.function_code = request->request_header.function_code;\n"
        body = body + "        rtn = " + self.get_implement_name() + "("
        for pm in self.get_input_parameters_list():
            if pm.check_variable_contain_square_brackets():
                body = body + "request->request_body." + self.get_request_struct_var() + "." + pm.get_name_without_square_brackets() + ",\n                                           "
            else:
                body = body + "request->request_body." + self.get_request_struct_var() + "." + pm.get_name_without_asterisk() + ",\n                                           "

        body = body + 'reply);\n'
        body = body + "    }\n    TR4A_trace( COMPONENT_ID_" + component_id + ", __ZOO_FUNC__, \"< function exit ... \");\n    return ;\n}\n"
        return body

    def get_implement_name(self):
        l = self._name.split("4")
        id = l[0]
        name = id + "MA_implement_4" + l[1]
        return name

    def get_implement_function_definition(self, component_id=''):
        buffer = "ZOO_EXPORT ZOO_INT32 " + self.get_implement_name() + "("
        for s in self._input_parameters:
            buffer = buffer + "IN " + s.get_type() + " " + s.get_name() + ","
        buffer = buffer + "IN " + component_id + "4I_REPLY_STRUCT * reply);\n"
        return buffer

    def get_implement_function(self, component_id=''):
        buffer = "ZOO_INT32 " + self.get_implement_name() + "("
        for s in self._input_parameters:
            buffer = buffer + "IN " + s.get_type() + " " + s.get_name() + ","
        buffer = buffer + "IN " + component_id + "4I_REPLY_STRUCT * reply)"
        return buffer

    def get_implement_function_body(self, component_id=''):
        buffer = "{\n"
        buffer = buffer + "    TR4A_trace( COMPONENT_ID_" + component_id + ", __ZOO_FUNC__, \"> function entry ... \");\n"
        buffer = buffer + "    ZOO_INT32 rtn = OK;\n"

        for pm in self._output_parameters:
            if "*" in pm.get_type():
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name() + ";\n"
            if pm.check_variable_contain_square_brackets():
                buffer = buffer + "    " + pm.get_type() + " " + pm.get_name() + ";\n"
                buffer = buffer + "    " + "memset(&" + pm.get_name_with_square_brackets_header_addr() + ",0,sizeof(" + pm.get_type() + ") * " + pm.get_array_length() + ");\n"
            if "ZOO_INT" in pm.get_name():
                buffer = buffer + "    " + pm.get_type() + " " + pm.get_name() + "  = 0;\n"
            if "_STRUCT" in pm.get_name() or "_struct" in pm.get_name():
                buffer = buffer + "    " + pm.get_type() + " " + pm.get_name() + " ;\n"
                buffer = buffer + "    " + "memset(&" + pm.get_name() + ",0,sizeof(" + pm.get_type() + "));\n"
            if "ZOO_FLOAT" in pm.get_name() or "ZOO_DOUBLE" in pm.get_name():
                buffer = buffer + "    " + pm.get_type() + " " + pm.get_name() + "  = 0.0;\n"

        for pm in self._inoutput_parameters:
            if "*" in pm.get_type():
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name() + ";\n"
            if pm.check_variable_contain_square_brackets():
                buffer = buffer + "    " + pm.get_type() + " " + pm.get_name() + ";\n"
                buffer = buffer + "    " + "memset(&" + pm.get_name_with_square_brackets_header_addr() + ",0,sizeof(" + pm.get_type() + ") * " + pm.get_array_length() + ");\n"
            if "ZOO_INT" in pm.get_name():
                buffer = buffer + "    " + pm.get_type() + " " + pm.get_name() + "  = 0;\n"
            if "_STRUCT" in pm.get_name() or "_struct" in pm.get_name():
                buffer = buffer + "    " + pm.get_type() + " " + pm.get_name() + " ;\n"
                buffer = buffer + "    " + "memset(&" + pm.get_name() + ",0,sizeof(" + pm.get_type() + "));\n"
            if "ZOO_FLOAT" in pm.get_name() or "ZOO_DOUBLE" in pm.get_name():
                buffer = buffer + "    " + pm.get_type() + " " + pm.get_name() + "  = 0.0;\n"

        buffer = buffer + "    /* usr add ... BEGIN */\n\n\n"

        if "_sig" in self._function:
            buffer = buffer + "    /* usr add ... END */\n"
            buffer = buffer + "    /* don't need reply */\n"
            buffer = buffer + "    MM4A_free(reply);\n"
        else:
            buffer = buffer + "    /* usr add ... END*/\n"
            buffer = buffer + "    " + self.get_event_name() + "(rtn,"

            for pm in self.get_output_parameters_list():
                if pm.check_variable_contain_square_brackets():
                    buffer = buffer + pm.get_name_without_square_brackets() + ","
                else:
                    buffer = buffer + pm.get_name().strip("*") + ","

            for pm in self.get_inoutput_parameters_list():
                if pm.check_variable_contain_square_brackets():
                    buffer = buffer + pm.get_name_without_square_brackets() + ","
                else:
                    buffer = buffer + pm.get_name().strip("*") + ","

            buffer = buffer + "reply);\n"

        buffer = buffer + "    TR4A_trace( COMPONENT_ID_" + component_id + ", __ZOO_FUNC__, \"< function exit ... \");\n    return rtn;\n"
        buffer = buffer + "}\n"
        return buffer

    def get_event_name(self):
        l = self._name.split("4")
        id = l[0]
        name = id + "MA_raise_4" + l[1]
        return name

    def get_event_function_definition(self, component_id=''):
        buffer = "ZOO_EXPORT ZOO_INT32 " + self.get_event_name() + "(IN ZOO_INT32 error_code,"
        for s in self._output_parameters:
            buffer = buffer + "IN " + s.get_type().strip("*") + " " + s.get_name() + ","
        for s in self._inoutput_parameters:
            buffer = buffer + "IN " + s.get_type().strip("*") + " " + s.get_name() + ","
        buffer = buffer + "IN " + component_id + "4I_REPLY_STRUCT * reply);\n"
        return buffer

    def get_event_function(self, component_id=''):
        buffer = "ZOO_INT32 " + self.get_event_name() + "(IN ZOO_INT32 error_code,"
        for s in self._output_parameters:
            buffer = buffer + "IN " + s.get_type().strip("*") + " " + s.get_name() + ","
        for s in self._inoutput_parameters:
            buffer = buffer + "IN " + s.get_type().strip("*") + " " + s.get_name() + ","
        buffer = buffer + "IN " + component_id + "4I_REPLY_STRUCT * reply)"
        return buffer

    def get_event_function_body(self, component_id=''):
        body = "{\n"
        body = body + "    ZOO_INT32 rtn = OK;\n" \
                      "    if(reply == NULL)\n" \
                      "    {\n" \
                      "        rtn = " + component_id + "4A_PARAMETER_ERR;\n" \
                                                        "    }\n\n" \
                                                        "    if(OK == rtn)\n" \
                                                        "    {\n" \
                                                        "        reply->reply_header.execute_result = error_code;\n"

        for pm in self._output_parameters:
            if pm.check_variable_contain_square_brackets():
                body = body + "        memcpy(&reply->reply_body." + self.get_reply_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + ",&" + pm.get_name_with_square_brackets_header_addr() + "," + "sizeof(" + pm.get_type() + ") * " + pm.get_array_length() + ");\n"
            elif "*" in pm.get_type():
                body = body + "        memcpy(&reply->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",&" + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                    "*") + "));\n"
            else:
                body = body + "        memcpy(&reply->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",&" + pm.get_name() + ",sizeof(" + pm.get_type() + "));\n"

        for pm in self._inoutput_parameters:
            if pm.check_variable_contain_square_brackets():
                body = body + "        memcpy(&reply->reply_body." + self.get_reply_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + ",&" + pm.get_name_with_square_brackets_header_addr() + "," + "sizeof(" + pm.get_type() + ") * " + pm.get_array_length() + ");\n"
            elif "*" in pm.get_type():
                body = body + "        memcpy(&reply->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",&" + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                    "*") + "));\n"
            else:
                body = body + "        memcpy(&reply->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",&" + pm.get_name() + ",sizeof(" + pm.get_type() + "));\n"

        body = body + "    }\n"
        body = body + "    return rtn;\n}\n"
        return body

    def get_function(self):
        return self._function

    def get_function_code(self):
        id = self._name[:2]
        code = ''
        if self._code_index < 16:
            code = "0x" + str_to_hex(id) + "ff" + str(hex(self._code_index).replace("0x", '0'))
        else:
            code = "0x" + str_to_hex(id) + "ff" + str(hex(self._code_index).replace("0x", ''))
        # print("function code:" + code)
        return code

    def generate_struct_string(self, type='', members=[PARAMETERS_CLASS()], component_id=''):
        tr = "/**\n*@brief " + type + "\n**/\n" + "typedef struct \n{\n"
        total_size = 0
        for n in members:
            total_size = total_size + type_to_size(n.get_type(), n.get_name())
        # print("total size: " + str(total_size))
        size_4_count = 0
        size_8_count = 0
        for s in members:
            if "*" in s.get_type():
                tr = tr + "    " + s.get_type().strip("const").strip("*").lstrip() + " " + s.get_name().strip(
                    "*") + "[" + component_id + "4I_BUFFER_LENGTH];\n"
            else:
                tr = tr + "    " + s.get_type() + " " + s.get_name().strip("*") + ";\n"
            if "ZOO_CHAR" in s.get_type() \
                    or "char" in s.get_type() \
                    or "ZOO_DOUBLE" in s.get_type() \
                    or "ZOO_FLOAT" in s.get_type() \
                    or "STRUCT" in s.get_type() \
                    or "struct" in s.get_type():
                size_8_count = size_8_count + 1
            else:
                size_4_count = size_4_count + 1

        if size_4_count % 2 == 1:
            tr = tr + "    ZOO_CHAR filler[4];\n"
        if len(members) == 0:
            tr = tr + "    ZOO_CHAR filler[8];\n"
        tr = tr + "}" + type + ";\n\n"
        return tr

    def generate_subscribe_struct_string(self, type=''):
        st = "/**\n*@brief " + type + "\n**/\n" + "typedef struct \n{\n"
        print("in size = " + str(self._name))
        for t in self._input_parameters:
            st = st + "    " + t.get_type() + " *callback_function;\n"
            st = st + "    void * parameter;\n"
        st = st + "}" + type + ";\n\n"
        return st

    def get_request_struct_typ(self, component_id=''):
        result = self.get_function_code_upper() + "_REQ_STRUCT"
        new = component_id + "4I_"
        old = component_id + "4A_"
        # print(old+" " + new)
        # print(result)
        if "4T_" in result:
            old = component_id + "4T_"
        return result.replace(old, new)

    def get_request_struct_var(self):
        patten = re.compile(r"(\w*4\w)_(\w*)")
        v = self._name
        var = patten.findall(v)
        result = var[0][1]
        if "_req" in result:
            result = result + "_msg"
        elif "_wait" in result:
            result = result.replace("_wait", "") + "_req_msg"
        else:
            result = result + "_req_msg"

        print("request_struct_var: " + result)
        return result

    def get_reply_struct_typ(self, component_id=''):
        result = self.get_function_code_upper() + "_REP_STRUCT"
        new = component_id + "4I_"
        old = component_id + "4A_"
        if "4T_" in result:
            old = component_id + "4T_"
        return result.replace(old, new)

    def get_reply_struct_var(self):
        patten = re.compile(r"(\w*4\w)_(\w*)")
        v = self._name
        var = patten.findall(v)
        result = var[0][1]
        if "_req" in result:
            result = result + "_msg"
        elif "_wait" in result:
            result = result.replace("_wait", "") + "_rep_msg"
        else:
            result = result + "_rep_msg"

        return result

    def get_callback_struct_typ(self, component_id=''):
        result = self.get_function_code_upper() + "_CALLBACK_STRUCT"
        new = component_id + "4I_"
        old = component_id + "4A_"
        if "4T_" in result:
            old = component_id + "4T_"
        return result.replace(old, new)

    def get_request_struct_msg(self, component_id=''):
        tp = self.get_function_code_upper() + "_REQ_STRUCT"
        old = '4A_'
        if "4T_" in tp:
            old = "4T_"
        r = tp.replace(old, "4I_")
        result = self.generate_struct_string(r, self.get_input_parameters_list(), component_id)
        return result

    def get_reply_struct_msg(self, component_id=''):
        tp = self.get_function_code_upper() + "_REP_STRUCT"
        result = ''
        mem = [PARAMETERS_CLASS("OUT", "ZOO_CHAR", "filler[8]")]
        if len(self.get_output_parameters_list()) > 0:
            if self._interface_type == "Sync":
                mem = self._output_parameters
        if len(self.get_inoutput_parameters_list()) > 0:
            mem = self._inoutput_parameters
        old = '4A_'
        if "4T_" in tp:
            old = "4T_"
        r = tp.replace(old, "4I_")
        result = self.generate_struct_string(r, mem, component_id)
        return result

    def get_callback_struct_msg(self, component_id=''):
        tp = self.get_function_code_upper() + "_CALLBACK_STRUCT"
        old = '4A_'
        if "4T_" in tp:
            old = "4T_"
        r = tp.replace(old, "4I_")
        result = self.generate_subscribe_struct_string(r)
        return result

    def check_need_generate_fc(self):
        if self._interface_type == 'Sync' or self._interface_type == "subscribe":
            return 1
        else:
            return 0

    def check_is_subscribe(self):
        if self._interface_type == "subscribe":
            return 1
        return 0

    def get_function_code_mirco(self):
        return "#define " + self._name.upper() + "_CODE" + " " + self.get_function_code()

    def get_function_code_upper(self):
        return self._name.upper() + "_CODE"

    def get_function_name(self):
        name_patten = re.compile(r"^\s*(\w+)\s+(\w+)\s*(\w+)\(", re.UNICODE | re.VERBOSE | re.MULTILINE | re.DOTALL)
        name = name_patten.findall(self._function)
        if len(name) == 0:
            return self._function
        self._return_type = name[0][1]
        self._name = name[0][2]
        if '_req' in self._name:
            self._interface_type = 'req'
        elif '_wait' in self._name:
            self._interface_type = 'wait'
        elif '_subscribe' in self._name:
            self._interface_type = 'subscribe'
        elif '_unsubscribe' in self._name:
            self._interface_type = 'unsubscribe'

        return self._name

    def get_function_code_upper(self):
        return self._name.upper() + "_CODE"

    def get_input_parameters_list(self):
        if not self._in_flag:
            self._in_flag = 1
            param_patten = re.compile(r"^\s*"
                                      "(ZOO_EXPORT)?"
                                      "\s+"
                                      "(ZOO_INT32|void|ZOO_BOOL)\s+"
                                      "(\w+)"
                                      "\s*"
                                      "\(([^)]*)\)\s*;", re.UNICODE | re.VERBOSE | re.MULTILINE | re.DOTALL)
            type_patten = re.compile(r"^\s*(\w+)\s+(\w*)\s+(\w*]+)")

            name = param_patten.findall(self._function)
            print(name)
            param = name[0][-1]
            result = re.sub('[\r\n\t]', '', param).replace(",...", "").split(',')
            print(result)
            tmp = []
            for p in result:
                print(p)
                m = p.strip()
                if "*" in m:
                    m = m.replace("*", "")
                    t = m.split(" ")
                    if t[0] == 'IN':
                        print("function: " + self._name)
                        print("parameter direction: " + t[0])
                        if len(t) == 3:
                            print("parameter type: " + t[1] + "*")
                            print("parameter name: " + t[2])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + "*", t[2].strip()))
                        if len(t) == 4:
                            print("parameter type: " + t[1] + " " + t[2] + "*")
                            print("parameter name: " + t[3])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + " " + t[2] + "*", t[3].strip()))
                        if len(t) == 5:
                            print("parameter type: " + t[1] + " " + t[2] + " " + t[3] + "*")
                            print("parameter name: " + t[4].strip("*"))
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + " " + t[2] + " " + t[3] + "*", t[4].strip()))
                else:
                    t = m.split(" ")
                    if t[0] == 'IN':
                        print("function: " + self._name)
                        print("parameter direction: " + t[0])
                        if len(t) == 3:
                            print("parameter      type: " + t[1])
                            print("parameter      name: " + t[2])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1], t[2].strip()))
                        if len(t) == 4:
                            print("parameter      type: " + t[1] + " " + t[2].strip())
                            print("parameter      name: " + t[3])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + " " + t[2], t[3].strip()))
                        if len(t) == 5:
                            print("parameter      type: " + t[1] + " " + t[2] + " " + t[3].strip())
                            print("parameter      name: " + t[4])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + " " + t[2] + " " + t[3], t[4].strip()))

            self._input_parameters = tmp
        return self._input_parameters

    def get_output_parameters_list(self):
        if not self._out_flag:
            self._out_flag = 1

            param_patten = re.compile(r"^\s*"
                                      "(ZOO_EXPORT)?"
                                      "\s+"
                                      "(ZOO_INT32|void|ZOO_BOOL)\s+"
                                      "(\w+)"
                                      "\s*"
                                      "\(([^)]*)\)\s*;", re.UNICODE | re.VERBOSE | re.MULTILINE | re.DOTALL)
            type_patten = re.compile(r"^\s*(\w+)\s+(\w*)\s+(\w*]+)")
            name = param_patten.findall(self._function)
            print(name)
            param = name[0][-1]
            result = re.sub('[\r\n\t]', '', param).replace(",...", "").split(',')
            print(result)
            tmp = []
            for p in result:
                # print(p)
                m = p.strip()
                if "*" in m:
                    m = m.replace("*", "")
                    t = m.split(" ")
                    if t[0] == 'OUT':
                        print("function: " + self._name)
                        print("parameter direction: " + t[0])
                        if len(t) == 3:
                            print("parameter type: " + t[1] + "*")
                            print("parameter name: " + t[2])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1].strip() + "*", t[2].strip()))
                        if len(t) == 4:
                            print("parameter type: " + t[1] + " " + t[2] + "*")
                            print("parameter name: " + t[3])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1].strip() + " " + t[2].strip() + "*", t[3].strip()))
                        if len(t) == 5:
                            print("parameter type: " + t[1] + " " + t[2] + " " + t[3] + "*")
                            print("parameter name: " + t[4].strip("*"))
                            tmp.append(
                                PARAMETERS_CLASS(t[0], t[1].strip() + " " + t[2].strip() + " " + t[3].strip() + "*",
                                                 t[4].strip()))
                else:
                    t = m.split(" ")
                    if t[0] == 'OUT':
                        print("function: " + self._name)
                        print("parameter direction: " + t[0])
                        if len(t) == 3:
                            print("parameter      type: " + t[1])
                            print("parameter      name: " + t[2])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1].strip(), t[2].strip()))
                        if len(t) == 4:
                            print("parameter      type: " + t[1].strip() + " " + t[2])
                            print("parameter      name: " + t[3])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1].strip() + " " + t[2], t[3].strip()))
                        if len(t) == 5:
                            print("parameter      type: " + t[1] + " " + t[2] + " " + t[3])
                            print("parameter      name: " + t[4])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1].strip() + " " + t[2].strip() + " " + t[3].strip(),
                                                        t[4].strip()))
            self._output_parameters = tmp
        return self._output_parameters

    def get_inoutput_parameters_list(self):
        if not self._inout_flag:
            self._inout_flag = 1

            param_patten = re.compile(r"^\s*"
                                      "(ZOO_EXPORT)?"
                                      "\s+"
                                      "(ZOO_INT32|void|ZOO_BOOL)\s+"
                                      "(\w+)"
                                      "\s*"
                                      "\(([^)]*)\)\s*;", re.UNICODE | re.VERBOSE | re.MULTILINE | re.DOTALL)
            type_patten = re.compile(r"^\s*(\w+)\s+(\w*)\s+(\w*]+)")
            name = param_patten.findall(self._function)
            param = name[0][-1]
            result = re.sub('[\r\n\t]', '', param).replace(",...", "").split(',')
            # print(result)
            tmp = []
            for p in result:
                # print(p)
                m = p.strip()
                if "*" in m:
                    m = m.replace("*", "")
                    t = m.split(" ")
                    if t[0] == 'INOUT':
                        print("function: " + self._name)
                        print("parameter direction: " + t[0])
                        if len(t) == 3:
                            print("parameter type: " + t[1] + "*")
                            print("parameter name: " + t[2])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + "*", t[2]))
                        if len(t) == 4:
                            print("parameter type: " + t[1] + " " + t[2] + "*")
                            print("parameter name: " + t[3])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + " " + t[2] + "*", t[3]))
                        if len(t) == 5:
                            print("parameter type: " + t[1] + " " + t[2] + " " + t[3] + "*")
                            print("parameter name: " + t[4].strip("*"))
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + " " + t[2] + " " + t[3] + "*", t[4]))
                else:
                    t = m.split(" ")
                    if t[0] == 'INOUT':
                        print("function: " + self._name)
                        print("parameter direction: " + t[0])
                        if len(t) == 3:
                            print("parameter      type: " + t[1])
                            print("parameter      name: " + t[2])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1], t[2]))
                        if len(t) == 4:
                            print("parameter      type: " + t[1] + " " + t[2])
                            print("parameter      name: " + t[3])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + t[2], t[3]))
                        if len(t) == 5:
                            print("parameter      type: " + t[1] + " " + t[2] + " " + t[3])
                            print("parameter      name: " + t[4])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + t[2] + t[3], t[4]))
            self._inoutput_parameters = tmp
        return self._inoutput_parameters

    def get_interface_type(self):
        return self._interface_type

    def get_return_type(self):
        return self._return_type


class CALLBACK_FUNCTION_CLASS:
    def __init__(self, function='', code_index=1, parts=[('', '', '')]):
        self._function = function
        self._input_parameters = [PARAMETERS_CLASS()]
        self._output_parameters = [PARAMETERS_CLASS()]
        self._inoutput_parameters = [PARAMETERS_CLASS()]
        self._interface_type = 'Sync'
        self._return_type = ''
        self._name = ''
        self._code_index = code_index
        self._parts = parts
        self._struct_type = ''
        self._callback_f = ''
        self.initialize()

    def get_function_name(self):
        return  self._function

    def get_comment(self, comment=''):
        buffer = '/**' + '\n' + ' *@brief ' + comment + '\n'

        for s in self._input_parameters:
            p = ' *@param ' + s.get_name() + '\n'
            buffer = buffer + p

        for s in self._output_parameters:
            p = ' *@param ' + s.get_name() + '\n'
            buffer = buffer + p

        for s in self._inoutput_parameters:
            p = ' *@param ' + s.get_name() + '\n'
            buffer = buffer + p

        buffer = buffer + '**/' + '\n'
        return buffer

    def get_callback_struct_typ(self, component_id=''):
        result = self.get_function_code_upper() + "_CALLBACK_STRUCT"
        new = component_id + "4I_"
        old = component_id + "4A_"
        if "4T_" in result:
            old = component_id + "4T_"
        return result.replace(old, new)

    def get_function_code_upper(self):
        return self._name.upper() + "_CODE"

    def get_name(self):
        return self._name

    def get_function_difinition(self, funtion_name='', component_id='XX'):
        d = funtion_name.replace(component_id, component_id + "MA_raise_")
        f = "ZOO_EXPORT void " + d + "("
        for s in self._input_parameters:
            f = f + "IN " + s.get_type() + " " + s.get_name() + ","

        f = f + ");"
        return f.replace(",);", ");")

    def get_function_name(self, funtion_name='', component_id='XX'):
        d = funtion_name.replace(component_id, component_id + "MA_raise_")
        f = "void " + d + "("
        for s in self._input_parameters:
            f = f + "IN " + s.get_type() + " " + s.get_name() + ","

        f = f + ")"
        return f.replace(",)", ")")

    def get_sub_callback_name(self,name=''):
        return name.replace("subscribe","callback")

    def generate_sub_callback_code(self,function=FUNCTION_CLASS(),component_id='XX'):
        code = "static void " + self.get_sub_callback_name(function.get_function_name()) + "(void *context_p, MQ4A_CALLBACK_STRUCT *local_proc, void *msg)\n"
        callback_t = function.get_input_parameters_list()[0].get_type()
        code = code + "{\n" \
                      "    ZOO_INT32 result = OK;\n" \
                      "    ZOO_INT32 error_code = OK;\n" \
                      "    "+component_id+"4I_REPLY_STRUCT *reply_msg = NULL;\n" \
                      "    "+function.get_callback_struct_typ(component_id)+" * callback_struct = NULL;\n"\
                      "    ZOO_INT32 rep_length = 0;\n"\
                      "    "+component_id+"4A_STATUS_STRUCT status;\n"\
                      "    if(msg == NULL)\n"\
                      "    {\n"\
                      "        result = " + component_id + "4A_PARAMETER_ERR;\n"\
                      "        EH4A_show_exception(COMPONENT_ID_" + component_id + ", __FILE__, __ZOO_FUNC__, __LINE__,result,\"msg is NULL.\");\n" \
                      "    }\n\n"\
                      "    if(OK == result)\n"\
                      "    {\n"\
                      "        result = " + component_id + "4I_get_reply_message_length("+function.get_function_code_upper()+", &rep_length);\n"\
                      "        if(OK != result)\n"\
                      "        {\n"\
                      "            result = " + component_id + "4A_PARAMETER_ERR;\n"\
                      "            EH4A_show_exception(COMPONENT_ID_" + component_id + ", __FILE__, __ZOO_FUNC__, __LINE__,result,\"get_reply_messge_length failed.\");\n" \
                      "        }\n" \
                      "    }\n\n"\
                      "    if(OK == result)\n"\
                      "    {\n"\
                      "        reply_msg = ("+component_id+"4I_REPLY_STRUCT * )MM4A_malloc(rep_length);\n"\
                      "        if(OK != result)\n"\
                      "        {\n"\
                      "            result = " + component_id + "4A_PARAMETER_ERR;\n"\
                      "            EH4A_show_exception(COMPONENT_ID_" + component_id + ", __FILE__, __ZOO_FUNC__, __LINE__,result,\"MM4A_malloc failed.\");\n" \
                      "        }\n" \
                      "    }\n\n"\
                      "    if(OK == result)\n"\
                      "    {\n"\
                      "        memcpy(reply_msg, msg, rep_length);\n" \
                      "        if ("+function.get_function_code_upper()+" != reply_msg->reply_header.function_code)\n"\
                      "        {\n"\
                      "            result = " + component_id + "4A_PARAMETER_ERR;\n"\
                      "            EH4A_show_exception(COMPONENT_ID_" + component_id + ", __FILE__, __ZOO_FUNC__, __LINE__,result,\"function code incorrect.\");\n" \
                      "        }\n" \
                      "        error_code = reply_msg->reply_header.execute_result;\n"\
                      "        memcpy((void*)&status, &reply_msg->reply_body."+self.get_struct_var()+".status, sizeof("+component_id+"4A_STATUS_STRUCT));\n"\
                      "        callback_struct = (" + function.get_callback_struct_typ(component_id) + "*) local_proc;\n"\
                      "        (("+callback_t+")callback_struct->callback_function)(status,error_code,context_p);\n "\
                      "   }\n\n"\
                      "   if(reply_msg != NULL)\n"\
                      "   {\n"\
                      "        MM4A_free(reply_msg);\n"\
                      "   }\n"\
                      "}"
        return code



    def generate_callback(self, function=FUNCTION_CLASS(), component_id='XX'):
        f = ''
        f = f + self.generate_sub_callback_code(function,component_id) + "\n\n"
        f = f + function.get_func_declaration()+"\n"
        f = f + "{\n"
        f = f + "    ZOO_INT32 result = OK;\n"
        f = f + "    ZOO_INT32 event_id = 0;\n"
        cb = "callback"
        f = f + "    MQ4A_CALLBACK_STRUCT* callback = NULL;\n"
        f = f + "    if (NULL == callback_function)\n" \
                "    {\n" \
                "        result = " + component_id + "4A_PARAMETER_ERR;\n" \
                "        EH4A_show_exception(COMPONENT_ID_" + component_id + ", __FILE__, __ZOO_FUNC__, __LINE__,result,\"callback_function is NULL.\");\n" \
                "        return result;\n" \
                "    }\n\n" \
                "    /*function entry*/\n" \
                "    TR4A_trace(COMPONENT_ID_" + component_id + ", __ZOO_FUNC__, \"> function entry ... \");\n"

        f = f + "    /*fill callback strcut*/\n" \
                "    callback = (MQ4A_CALLBACK_STRUCT*)MM4A_malloc(sizeof(" + function.get_callback_struct_typ(component_id) + "));\n"

        f = f + "    if (NULL == callback)\n" \
                "    {\n" \
                "        result = " + component_id + "4A_PARAMETER_ERR;\n" \
                "        EH4A_show_exception(COMPONENT_ID_" + component_id + ", __FILE__, __ZOO_FUNC__, __LINE__,result,\"callback is NULL.\");\n" \
                "    }\n\n"

        f = f + "    if (OK == result)\n" \
                "    {\n" \
                "        callback->callback_function = callback_function;\n" \
                "        event_id = " + function.get_function_code_upper() + ";\n" \
                "        result = "+component_id+"4I_send_subscribe(" + component_id + "4A_SERVER,\n" \
                "                                      " + self.get_sub_callback_name(function.get_function_name()) + ",\n" \
                "                                      callback,\n" \
                "                                      event_id,\n" \
                "                                      (ZOO_HANDLE*)handle,\n" \
                "                                      context);\n" \
                "        if (OK != result)\n" \
                "        {\n" \
                "           result = " + component_id + "4A_PARAMETER_ERR;\n" \
                "           EH4A_show_exception(COMPONENT_ID_" + component_id + ", __FILE__, __ZOO_FUNC__, __LINE__,result,\"send_subscribe failed.\");\n" \
                "           MM4A_free(callback);\n" \
                "        }\n" \
                "    }\n\n" \
                "    TR4A_trace(COMPONENT_ID_" + component_id + ", __ZOO_FUNC__,\"< function exit ...\");\n" \
                "    return result;\n" \
                "}\n\n"
        f= f + self.generate_unsubscribe(function,component_id)
        return f

    def generate_unsubscribe(self,function=FUNCTION_CLASS(), component_id='XX'):
        body = "ZOO_INT32 " + function.get_function_name().replace("_subscribe","_unsubscribe") + "(IN ZOO_UINT32 handle)\n{\n"
        body = body + "    ZOO_INT32 result = OK;\n"
        body = body + "    ZOO_INT32 event_id = " + function.get_function_code_upper() + ";\n"
        body = body + "    if(OK == result)\n"
        body = body + "    {\n"
        body = body + "        result = "+component_id+"4I_send_unsubscribe("+component_id+"4A_SERVER,event_id,handle);\n" \
                      "    }\n"
        body = body + "    return result;\n}\n\n"
        return body

    def get_function_body(self, function=FUNCTION_CLASS(), component_id='XX'):
        body = "{\n"
        body = body + "    ZOO_INT32 rtn = OK;\n" \
                      "    " + component_id + "4I_REPLY_STRUCT * reply_message = NULL;\n" \
                                              "    reply_message = (" + component_id + "4I_REPLY_STRUCT * ) " + "MM4A_malloc(sizeof(" + component_id + "4I_REPLY_STRUCT));\n"
        body = body + "    if(NULL == reply_message)\n" \
                      "    {\n" \
                      "        rtn = " + component_id + "4A_PARAMETER_ERR;\n" \
                    "    }\n" \
                    "    \n" \
                    "    if(OK == rtn)\n" \
                    "    {\n" \
                    "        reply_message->reply_header.function_code = " + function.get_function_code_upper() + ";\n" \
                                                                                                                  "        reply_message->reply_header.execute_result = error_code;\n"

        for p in self._input_parameters:
            if "STRUCT" in p.get_type() or "struct" in p.get_type():
                body = body + "        memcpy(&reply_message->reply_body." + self.get_struct_var() + "." + p.get_name() + ",&status,sizeof(" + p.get_type() + "));\n"
        body = body + "    }\n\n" \
                      "    if(OK == rtn)\n" \
                      "    {\n" \
                      "        rtn = " + component_id + "4I_publish_event(" + component_id + "4A_SERVER,\n" \
                      "                                            " + function.get_function_code_upper() + ",\n" \
                      "                                            reply_message);\n"
        body = body + "    }\n\n" \
                      "    if(OK != rtn)\n"\
                      "    {\n"\
                      "        EH4A_show_exception(COMPONENT_ID_" + component_id + ", __FILE__, __ZOO_FUNC__, __LINE__,rtn,\"publish_event failed.\");\n" \
                      "    }\n"\
                      "    MM4A_free(reply_message);\n" \
                      "    return ;\n" \
                      "}"
        return body

    def initialize(self):
        for p in self._parts:
            result = re.sub('[\r\n\t]', '', p[2]).split(',')
            self._name = p[1]
            self._return_type = p[0]
            # print(result)
            in_p = []
            out_p = []
            inout_p = []
            for x in result:
                m = x.strip()
                t = m.split(" ")
                print("\n")
                print("function: " + self._name)
                if t[0] == 'IN':
                    print("parameter direction: " + t[0])
                    print("parameter      type: " + t[1])
                    print("parameter      name: " + t[2])
                    in_p.append(PARAMETERS_CLASS(t[0], t[1], t[2]))
                    self._callback_f = t[1]
                if t[0] == 'OUT':
                    print("parameter direction: " + t[0])
                    print("parameter      type: " + t[1])
                    print("parameter      name: " + t[2])
                    out_p.append(PARAMETERS_CLASS(t[0], t[1], t[2]))
                if t[0] == 'INOUT':
                    print("parameter direction: " + t[0])
                    print("parameter      type: " + t[1])
                    print("parameter      name: " + t[2])
                    inout_p.append(PARAMETERS_CLASS(t[0], t[1], t[2]))

            self._input_parameters = in_p
            self._output_parameters = out_p
            self._inoutput_parameters = inout_p

    def generate_struct_string(self, type='', members=[PARAMETERS_CLASS()]):
        tr = "/**\n*@brief " + type + "\n**/\n" + "typedef struct \n{\n"
        total_size = 0
        for n in members:
            total_size = total_size + type_to_size(n.get_type(), n.get_name())
        # print("total size: " + str(total_size))
        for s in members:
            '''if type_to_size(s.get_type(),s.get_name()) % 8 > 0 :
                fill_size = (type_to_size(s.get_type(),s.get_name()) % 8)
                tr = tr + "    ZOO_CHAR filler[" + str(fill_size) + "];\n"'''
            if "STRUCT" in s.get_type() or "struct" in s.get_type():
                tr = tr + "    " + s.get_type() + " " + s.get_name().strip("*") + ";\n"
                tr = tr + "    ZOO_CHAR filler[8];\n"

        if len(members) == 0:
            tr = tr + "    ZOO_CHAR filler[8];\n"
        tr = tr + "}" + type + ";\n\n"
        self._struct_type = type
        self.get_struct_var()
        return tr

    def get_struct_typ(self):
        return self._struct_type

    def get_struct_var(self):
        m = self._struct_type.split("_")
        m.pop(0)
        m.pop(len(m) - 1)
        v = ''
        for i in m:
            v = v + i + "_"
        x = v.rstrip("_") + "_msg"
        # print(x.lower())
        return x.lower()

    def get_input_parameters(self):
        return self._input_parameters

    def get_output_parameters(self):
        return self._output_parameters

    def get_inoutput_parameters(self):
        return self._inoutput_parameters

    def get_reply_msg(self, name):
        tp = name.upper() + "_CODE_REP_STRUCT"
        result = ''
        mem = [PARAMETERS_CLASS("OUT", "ZOO_CHAR", "filler[8]")]
        if len(self._input_parameters) > 0:
            mem = self._input_parameters
            # print(mem)
        old = '4A_'
        if "4T_" in tp:
            old = "4T_"
        r = tp.replace(old, "4I_")
        result = self.generate_struct_string(r, mem)
        # print(result)
        return result


# *
# @brief interface header file
# *
class XX4A_IF_HEADER_CLASS:
    def __init__(self, file_name=''):
        self._file_name = file_name
        self._function_list = []
        self._callback_list = []
        self.initialize()
        print("if.h: " + file_name)

    def get_product(self):
        product = ['XX']
        with open(self._file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.find('Product:') > -1:
                    product = line.split('Product:')
                    break
        return product[-1]

    def get_author(self):
        return 'Code Generator'

    def get_file_name(self):
        return self._file_name

    def initialize(self):
        callback_entity = re.compile(r"^\s*"
                                     "typedef\s+"
                                     "(?P<FUNCTION_POINTER_RETRUN_TYPE>\w+)"
                                     "\s*\(\s*\*"
                                     "(?P<FUNCTION_POINTER_TYPE>\w*)"
                                     "\s*\)\s*\("
                                     "(?P<PARAMETERS>[^)]*)",
                                     re.UNICODE | re.VERBOSE | re.MULTILINE | re.DOTALL)

        tmp = []
        with open(self._file_name, 'r+', encoding='utf-8') as f:
            text = f.read()
            entity = callback_entity.findall(text)
            # print("callback: *************************************BEGIN")
            # print(entity)
            # print("callback: *************************************END")
            fc = 0
            for result in entity:
                fp = "ZOO_EXPORT " + result[0] + " " + result[1] + "(" + result[2] + ")"
                #print("//////////////////////////////////////////////////////")
                #print(fp)
                tmp.append(CALLBACK_FUNCTION_CLASS(fp, fc, entity))
                fc = fc + 1
        self._callback_list = tmp

    def get_callback_list(self):
        return self._callback_list

    def get_function_list(self):
        function_entity = re.compile(r"^\s*"
                                     "ZOO_EXPORT?"
                                     "\s+"
                                     "\w+\s+"
                                     "\w+"
                                     "\s*"
                                     "\([^)]*\)\s*;", re.UNICODE | re.VERBOSE | re.MULTILINE | re.DOTALL)
        tmp = []
        with open(self._file_name, 'r+', encoding='utf-8') as f:
            text = f.read()
            entity = function_entity.findall(text)
            # print(entity)
            fc = 0
            for result in entity:
                tmp.append(FUNCTION_CLASS(result, fc))
                # print(result)
                fc = fc + 1
        self._function_list = tmp
        return tmp


# *
# @brief interface header file
# *
class XX4A_TYPE_HEADER_CLASS:
    def __init__(self, file=''):
        self._file = file

    def get_enum_list(self):
        enum_patten = re.compile(r"typedef\s+enum\s*{[^}]*}[^;]+")
        e = []
        print(self._file)
        with open(self._file, 'r+', encoding='utf-8') as f:
            text = f.read()
            entity = enum_patten.findall(text)
            print(entity)
            for result in entity:
                tmp = []
                double_slash_patten = re.compile(r'//.*')
                slash_star_patten = re.compile(r'/\*.*?\*/')
                name_patten = re.compile(r"(\w\w4\w\_\w*\_ENUM)")
                mem_patten = re.compile(r"\s*(\w\w4\w\_\w*)+")
                s = re.sub(double_slash_patten, ' ', result)
                x = re.sub(slash_star_patten, '', s)
                m = re.sub('[\r\n\t]', '', x)
                print(m)
                name = name_patten.findall(m)
                print(name)
                r = mem_patten.findall(m)
                print(r)
                for mm in r:
                    tmp.append(mm)
                e.append(ENUM_CLASSS(name, tmp))
        return e

    def get_struct_list(self):
        enum_patten = re.compile(
            r"typedef\s+struct\s*{[^}]*}[^;]+")  # re.compile(r"typedef\s+struct\s*{[^{}]*}\s*([a-zA-Z0-9_]+)\s*;")
        e = []
        print(self._file)
        with open(self._file, 'r+', encoding='utf-8') as f:
            text = f.read()
            e = enum_patten.findall(text)
            print(e)
        return e

    def get_mirco_list(self):
        return


# *
# create directory for XX component
# *
class XX_DIR_GENERATOR(object):
    def __init__(self, component_id='XX'):
        self._current_path = os.getcwd()
        self._inc_dir = self._current_path + '/' + component_id + '/' + 'inc'
        self._com_dir = self._current_path + '/' + component_id + '/' + 'com'
        self._lib_dir = self._current_path + '/' + component_id + '/' + 'lib'
        self._bin_dir = self._current_path + '/' + component_id + '/' + 'bin'
        self._bin_tst = self._current_path + '/' + component_id + '/' + 'test'
        if not os.path.exists(self._inc_dir):
            os.makedirs(self._inc_dir)
        if not os.path.exists(self._com_dir):
            os.makedirs(self._com_dir)
        if not os.path.exists(self._lib_dir):
            os.makedirs(self._lib_dir)
        if not os.path.exists(self._bin_dir):
            os.makedirs(self._bin_dir)
        if not os.path.exists(self._bin_tst):
            os.makedirs(self._bin_tst)

    def get_inc_path(self):
        return self._inc_dir

    def get_com_path(self):
        return self._com_dir

    def get_lib_path(self):
        return self._lib_dir

    def get_bin_path(self):
        return self._bin_dir


# *
# create XX4I_type.h
# *
class XX4I_type_h(object):
    def __init__(self, component_id='', function_list=[], callback_lsit=[CALLBACK_FUNCTION_CLASS()], path=''):
        self._component_id = component_id
        self._function_list = function_list
        self._file_name = path + '/' + component_id + '4I_type.h'
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', component_id + '4I_type.h')
        self._callback_list = callback_lsit

    def generate_header_comment(self):
        with open(self._file_name, 'w') as f:
            for header in self._header_comment.get_list():
                f.write(header)
                f.write('\n')
        return

    def generate_include(self):
        with open(self._file_name, 'a+') as f:
            f.write('#ifndef ' + self._component_id + '4I_TYPE_H')
            f.write('\n')
            f.write('#define ' + self._component_id + '4I_TYPE_H')
            f.write('\n')
            f.write('#include <MQ4A_type.h>')
            f.write('\n')
            f.write('#include "' + self._component_id + '4A_type.h"')
            f.write('\n')
            f.write('#include "' + self._component_id + '4A_if.h"')
            f.write('\n')
            f.write('\n')
        return

    def get_server_address(self):
        return self._component_id + '4A_SERVER'

    def generate_mirco_defintion(self):
        with open(self._file_name, 'a+') as f:
            f.write(COMMENT_CLASS().get_comment('Mirco Defnition'))
            f.write('#define COMPONENT_ID_' + self._component_id + ' "' + self._component_id + "\"")
            f.write('\n')
            f.write('#define ' + self._component_id + '4A_SERVER     "' + self._component_id + '4A_SERVER"')
            f.write('\n')
            f.write('#define ' + self._component_id + '4I_BUFFER_LENGTH    256')
            f.write('\n')
            f.write('#define ' + self._component_id + '4I_RETRY_INTERVAL   3')
            f.write('\n')
            f.write('\n')
            f.write(COMMENT_CLASS().get_comment('Function Code Definitions'))
            for func in self._function_list:
                if func.check_need_generate_fc() == 1:
                    func_code_define = func.get_function_code_mirco()
                    f.write(func_code_define)
                    f.write('\n')
            f.write("\n")
        return

    def generate_header_struct(self):
        with open(self._file_name, 'a+') as f:
            f.write("/*Request and reply header struct*/\n"
                    "typedef struct\n"
                    "{\n"
                    "    MQ4A_SERV_ADDR repl_addr;\n"
                    "    ZOO_INT32 msg_id;\n"
                    "    ZOO_BOOL reply_wanted;\n"
                    "    ZOO_INT32 func_id;\n"
                    "}" + self._component_id + "4I_REPLY_HANDLER_STRUCT;")
            f.write("\n\n")
            f.write("/*Request message header struct*/\n"
                    "typedef struct\n"
                    "{\n"
                    "    ZOO_INT32 function_code;\n"
                    "    ZOO_BOOL need_reply;\n"
                    "}" + self._component_id + "4I_REQUEST_HEADER_STRUCT;")
            f.write("\n\n")
            f.write("/*Reply message header struct*/\n"
                    "typedef struct\n"
                    "{\n"
                    "    ZOO_INT32 function_code;\n"
                    "    ZOO_BOOL execute_result;\n"
                    "}" + self._component_id + "4I_REPLY_HEADER_STRUCT;")
            f.write("\n\n")
        return

    def generate_request_message(self):
        with open(self._file_name, 'a+') as f:
            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write(func.get_request_struct_msg(self._component_id))
        return

    def generate_reply_message(self):
        with open(self._file_name, 'a+') as f:
            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write(func.get_reply_struct_msg(self._component_id))
                if func.get_interface_type() == "subscribe":
                    for cb in self._callback_list:
                        f.write(cb.get_reply_msg(func.get_function_name()))
        return

    def generate_subsribe_message(self):
        with open(self._file_name, 'a+') as f:
            for func in self._function_list:
                if func.check_is_subscribe():
                    print(func.get_function_name())
                    f.write(func.get_callback_struct_msg())
        return

    def generate_request_messages(self):
        with open(self._file_name, 'a+') as f:
            f.write("typedef struct\n")
            f.write("{\n")
            f.write("    " + self._component_id + "4I_REQUEST_HEADER_STRUCT request_header;\n")
            f.write("    union\n")
            f.write("    {\n")
            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write("        " + func.get_request_struct_typ(
                        self._component_id) + " " + func.get_request_struct_var() + ";\n")
            f.write("     }request_body;\n")
            f.write("}" + self._component_id + "4I_" + "REQUEST_STRUCT;\n")
            f.write("\n\n")
        return

    def generate_reply_messages(self):
        with open(self._file_name, 'a+') as f:
            f.write("typedef struct\n")
            f.write("{\n")
            f.write("    " + self._component_id + "4I_REPLY_HEADER_STRUCT reply_header;\n")
            f.write("    union\n")
            f.write("    {\n")
            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write("        " + func.get_reply_struct_typ(
                        self._component_id) + " " + func.get_reply_struct_var() + ";\n")
            for cb in self._callback_list:
                f.write("        " + cb.get_struct_typ() + " " + cb.get_struct_var() + ";\n")

            f.write("    }reply_body;\n")
            f.write("}" + self._component_id + "4I_" + "REPLY_STRUCT;\n")
            f.write("\n\n")
        return

    def end_file(self):
        with open(self._file_name, 'a+') as f:
            f.write("#endif //" + self._component_id + '4I_type.h' + "\n")

    def generate(self):
        self.generate_header_comment()
        self.generate_include()
        self.generate_mirco_defintion()
        self.generate_header_struct()
        self.generate_request_message()
        self.generate_reply_message()
        self.generate_request_messages()
        self.generate_reply_messages()
        self.generate_subsribe_message()
        self.end_file()
        return


# *
# create XX4I_if.c
# *
class XX4A_c(object):
    def __init__(self, component_id='', function_list=[], callback_lsit=[CALLBACK_FUNCTION_CLASS()], path=''):
        self._component_id = component_id
        self._function_list = function_list
        self._callback_list = callback_lsit
        self._path = path
        self._file_name = self._component_id + "4A.c"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', component_id + '4A.c')

    def generate(self):
        with open(self._path + '/' + self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")
            for incld in FILE_INCLUDE_CLASS(["ZOO.h", "stdio.h", "stdlib.h", "string.h",
                                             "MQ4A_if.h",
                                             "MQ4A_type.h",
                                             "MM4A_if.h", "EH4A_if.h", "TR4A_if.h",
                                             self._component_id + "4I_type.h",
                                             self._component_id + "4A_type.h",
                                             self._component_id + "4I_if.h",
                                             ]).get_list():
                f.write(incld)
                f.write("\n")
            i = 0
            for fc in self._function_list:
                if fc.get_interface_type() == "Sync":
                    f.write(fc.get_comment(fc.get_function_name()))
                    f.write(fc.get_function().replace("ZOO_EXPORT ", "").rstrip(";"))
                    f.write("\n")
                    f.write(fc.get_body(self._component_id))
                    f.write("\n")

                if fc.get_interface_type() == "req":
                    f.write(fc.get_comment(fc.get_function_name()))
                    f.write(fc.get_function().replace("ZOO_EXPORT ", "").rstrip(";"))
                    f.write("\n")
                    f.write(fc.get_body_req(self._component_id))
                    f.write("\n")

                if fc.get_interface_type() == "wait":
                    f.write(fc.get_comment(fc.get_function_name()))
                    f.write(fc.get_function().replace("ZOO_EXPORT ", "").rstrip(";"))
                    f.write("\n")
                    f.write(fc.get_body_wait(self._component_id))
                    f.write("\n")

                if fc.get_interface_type() == "subscribe":
                    cb = self._callback_list[i]
                    f.write(cb.generate_callback(fc, self._component_id))
                    i = i+1
        return


class XX4I_if_h(object):
    def __init__(self, component_id='', function_list=[], path=''):
        self._component_id = component_id
        self._function_list = function_list
        self._path = path
        self._file_name = self._component_id + "4I_if.h"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', component_id + '4I_if.h')

    def get_request_message_length_function_difinition(self):
        fd = "/*\n" \
             "@brief 获取请求消息长度【字节】\n" \
             "*@param function_code   函数码\n" \
             "*@param *message_length 字节长度 \n" \
             "*@precondition:\n" \
             "*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._component_id + "4I_get_request_message_length(IN ZOO_INT32 function_code,\n" \
                                                                 "													INOUT ZOO_INT32 *message_length );"
        return fd

    def get_reply_message_length_function_difinition(self):
        fd = "/*" \
             "\n@brief 获取回答消息长度【字节】\n" \
             "*@param function_code   函数码\n" \
             "*@param *message_length 字节长度 \n" \
             "*@precondition:\n*@postcondition:\n" \
             "*/" \
             "\n" \
             "ZOO_EXPORT ZOO_INT32 " + self._component_id + "4I_get_reply_message_length(IN ZOO_INT32 function_code,\n" \
                                                            "													INOUT ZOO_INT32 *message_length );"
        return fd

    def get_send_request_and_reply_function_difinition(self):
        fd = "/*\n" \
             "*@brief 向目标地址发送消息，并获得返回消息，同步接口，会阻塞调用方\n" \
             "*@param MQ4A_SERV_ADDR   服务器地址\n" \
             "*@param *request_message 请求消息\n" \
             "*@param *reply_message   回复消息\n" \
             "*@param timeout          请求消息最长等待超时时间 \n" \
             "*@precondition:\n" \
             "*@postcondition: \n" \
             "*/\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._component_id + "4I_send_request_and_reply(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "													IN " + self._component_id + "4I_REQUEST_STRUCT  *request_message,\n" \
                                                                                                                                                  "													INOUT " + self._component_id + "4I_REPLY_STRUCT *reply_message,\n" \
                                                                                                                                                                                                                                      "													IN ZOO_INT32 timeout);"
        return fd

    def get_send_request_message_difinition(self):
        fd = "/*\n" \
             "*@brief 向目标地址发送消息，异步接口，非阻塞，配合" + self._component_id + "4I_receive_reply_message\n" \
                                                                    "*@param MQ4A_SERV_ADDR   服务器地址\n" \
                                                                    "*@param *request_message 请求消息 \n" \
                                                                    "*@precondition:\n*@postcondition:\n" \
                                                                    "*/\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._component_id + "4I_send_request_message(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "													IN " + self._component_id + "4I_REQUEST_STRUCT *request_message);"
        return fd

    def get_receive_reply_message_difinition(self):
        fd = "/*\n" \
             "*@brief 接收目标消息\n	" \
             "*@param server         服务器地址\n" \
             "*@param function_code  函数码\n" \
             "*@param *reply_message 返回消息\n" \
             "*@param timeout        超时时间\n" \
             "*@description:         异步接口，配合XX4I_send_request_message一起使用\n" \
             "*@precondition:\n" \
             "*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._component_id + "4I_receive_reply_message(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "													IN ZOO_INT32 function_code,\n" \
                                                                 "													INOUT " + self._component_id + "4I_REPLY_STRUCT *reply_message,\n" \
                                                                                                                                                     "													IN ZOO_INT32 timeout);"
        return fd

    def get_publish_event_difinition(self):
        fd = "/*\n" \
             "*@brief 向目标地址发布消息，订阅的用户可以收到消息\n" \
             "*@param event_id       消息的编号，一般指函数码\n" \
             "*@param *reply_message 消息结构体，函数参数组合\n" \
             "*@description:         需要先订阅，才能收到 \n" \
             "*@precondition:\n*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._component_id + "4I_publish_event(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "													IN ZOO_INT32 event_id,\n" \
                                                                 "													INOUT " + self._component_id + "4I_REPLY_STRUCT *reply_message);"
        return fd

    def get_send_subscribe_difinition(self):
        fd = "/*\n" \
             "*@brief 发送订阅消息\n*@param server            服务器地址\n" \
             "*@param callback_function 本地回调处理函数\n" \
             "*@param callback_struct   接口回调结构体\n" \
             "*@param event_id          请求消息\n" \
             "*@param *handle           订阅输出句柄\n" \
             "*@param *context          上下文标识\n " \
             "*@precondition:\n*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._component_id + "4I_send_subscribe(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "													IN MQ4A_EVENT_CALLBACK_FUNCTION callback_function,\n" \
                                                                 "													IN MQ4A_CALLBACK_STRUCT *callback_struct,\n" \
                                                                 "													IN ZOO_INT32 event_id,\n" \
                                                                 "													INOUT ZOO_HANDLE *handle,\n" \
                                                                 "													INOUT void *context);"
        return fd

    def get_send_unsubscribe_difinition(self):
        fd = "/*\n" \
             "*@brief 取消订阅\n" \
             "*@param server   服务器地址\n" \
             "*@param event_id 请求消息\n" \
             "*@param handle   订阅输出句柄 \n" \
             "*@precondition:\n" \
             "*@postcondition:\n" \
             "*/\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._component_id + "4I_send_unsubscribe(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "													IN ZOO_INT32 event_id,\n" \
                                                                 "													IN ZOO_HANDLE handle);"
        return fd

    def get_send_signal_difinition(self):
        fd = "/*\n" \
             "*@brief 发送信号消息\n" \
             "*@param server  服务器地址\n" \
             "*@param message 请求消息\n" \
             "*@param message_length   请求消息长度\n" \
             "*@precondition:\n*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._component_id + "4I_send_signal(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "													IN void * message,\n" \
                                                                 "													IN ZOO_INT32 message_length);"
        return fd

    def generate(self):
        with open(self._path + '/' + self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            for incld in FILE_INCLUDE_CLASS(["ZOO.h", "stdio.h", "stdlib.h", "EH4A_if.h", "TR4A_if.h",
                                             "MQ4A_if.h",
                                             "MQ4A_type.h",
                                             "MM4A_if.h",
                                             self._component_id + "4I_type.h",
                                             self._component_id + "4A_type.h",
                                             ]).get_list():
                f.write(incld)
                f.write("\n")
            f.write(self.get_request_message_length_function_difinition())
            f.write("\n\n")
            f.write(self.get_reply_message_length_function_difinition())
            f.write("\n\n")
            f.write(self.get_send_request_and_reply_function_difinition())
            f.write("\n\n")
            f.write(self.get_send_request_message_difinition())
            f.write("\n\n")
            f.write(self.get_receive_reply_message_difinition())
            f.write("\n\n")
            f.write(self.get_publish_event_difinition())
            f.write("\n\n")
            f.write(self.get_send_subscribe_difinition())
            f.write("\n\n")
            f.write(self.get_send_unsubscribe_difinition())
            f.write("\n\n")
            f.write(self.get_send_signal_difinition())
            f.write("\n\n")
            f.write(get_endif(self._file_name))
            f.write("\n")
        return


class XX4I_c(object):
    def __init__(self, component_id='', function_list=[], path=''):
        self._component_id = component_id
        self._function_list = function_list
        self._path = path
        self._file_name = self._component_id + "4I.c"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', component_id + '4I.c')

    def get_request_message_length_function_difinition(self):
        fd = "/*\n" \
             "@brief 获取请求消息长度【字节】\n" \
             "*@param function_code   函数码\n" \
             "*@param *message_length 字节长度 \n" \
             "*@precondition:\n" \
             "*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_INT32 " + self._component_id + "4I_get_request_message_length(IN ZOO_INT32 function_code,\n" \
                                                      "													INOUT ZOO_INT32 *message_length )\n"
        fd = fd + "{" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    /* 检查输入参数指针是否?*/\n" \
                  "    if ( NULL == message_length )\n" \
                  "    {\n" \
                  "        result = " + self._component_id + "4A_PARAMETER_ERR;\n" \
                  "        EH4A_show_exception(COMPONENT_ID_" + self._component_id + ", __FILE__, __ZOO_FUNC__, __LINE__,result,\"request msg length is NULL.\");\n" \
                  "    }\n" \
                  "    else\n" \
                  "    {\n" \
                  "        *message_length = 0;\n" \
                    "    }\n" \
                    "    /*查询发送请求消息的长度*/\n" \
                    "    if ( OK == result )\n" \
                    "    {\n" \
                    "        switch( function_code )\n" \
                    "        {\n"
        for fn in self._function_list:
            if fn.get_interface_type() == "Sync":
                fd = fd + "        case " + fn.get_function_code_upper() + ":\n"
                fd = fd + "            *message_length = sizeof(" + self._component_id + "4I_REQUEST_HEADER_STRUCT)+sizeof(" + fn.get_request_struct_typ(
                    self._component_id) + ");\n"
                fd = fd + "            break;\n"
        fd = fd + "        default:\n" \
                  "               result = " + self._component_id + "4A_PARAMETER_ERR;\n" \
                "               EH4A_show_exception(COMPONENT_ID_" + self._component_id + ", __FILE__, __ZOO_FUNC__,__LINE__,result,\" Error in " + self._component_id + "4I_get_request_message_length.\");\n" \
                "               break;\n" \
                "        }\n" \
                "    }\n" \
                "    return result;\n"
        fd = fd + "}\n"
        return fd

    def get_reply_message_length_function_difinition(self):
        fd = "/*" \
             "\n@brief 获取回答消息长度【字节】\n" \
             "*@param function_code   函数码\n" \
             "*@param *message_length 字节长度 \n" \
             "*@precondition:\n*@postcondition:\n" \
             "*/" \
             "\n" \
             "ZOO_INT32 " + self._component_id + "4I_get_reply_message_length(IN ZOO_INT32 function_code,\n" \
                                                 "													INOUT ZOO_INT32 *message_length )\n"
        fd = fd + "{" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    /* 检查输入参数指针是否?*/\n" \
                  "    if ( NULL == message_length )\n" \
                  "    {\n" \
                  "        result = " + self._component_id + "4A_PARAMETER_ERR;\n" \
                                                             "        EH4A_show_exception(COMPONENT_ID_" + self._component_id + ", __FILE__,__ZOO_FUNC__,__LINE__,result,\"request msg length is NULL.\");\n" \
                                                                                                                                "    }\n" \
                                                                                                                                "    else\n" \
                                                                                                                                "    {\n" \
                                                                                                                                "        *message_length = 0;\n" \
                                                                                                                                "    }\n" \
                                                                                                                                "    /*查询发送请求消息的长度*/\n" \
                                                                                                                                "    if ( OK == result )\n" \
                                                                                                                                "    {\n" \
                                                                                                                                "        switch( function_code )\n" \
                                                                                                                                "        {\n"
        for fn in self._function_list:
            if fn.get_interface_type() == "Sync":
                fd = fd + "        case " + fn.get_function_code_upper() + ":\n"
                fd = fd + "            *message_length = sizeof(" + self._component_id + "4I_REPLY_HEADER_STRUCT)+sizeof(" + fn.get_reply_struct_typ(
                    self._component_id) + ");\n"
                fd = fd + "            break;\n"
            if fn.get_interface_type() == "subscribe":
                fd = fd + "        case " + fn.get_function_code_upper() + ":\n"
                fd = fd + "            *message_length = sizeof(" + self._component_id + "4I_REPLY_HEADER_STRUCT)+sizeof(" + fn.get_reply_struct_typ(
                    self._component_id) + ");\n"
                fd = fd + "            break;\n"
        fd = fd + "        default:\n" \
                  "               result = " + self._component_id + "4A_PARAMETER_ERR;\n" \
                                                                    "               EH4A_show_exception(COMPONENT_ID_" + self._component_id + ", __FILE__,__ZOO_FUNC__, __LINE__,result,\" Error in " + self._component_id + "4I_get_request_message_length.\");\n" \
                                                                                                                                                                                                                             "               break;\n" \
                                                                                                                                                                                                                             "        }\n" \
                                                                                                                                                                                                                             "    }\n" \
                                                                                                                                                                                                                             "    return result;\n"
        fd = fd + "}\n"
        return fd

    def get_send_request_and_reply_function_difinition(self):
        fd = "/*\n" \
             "*@brief 向目标地址发送消息，并获得返回消息，同步接口，会阻塞调用方\n" \
             "*@param MQ4A_SERV_ADDR   服务器地址\n" \
             "*@param *request_message 请求消息\n" \
             "*@param *reply_message   回复消息\n" \
             "*@param timeout          请求消息最长等待超时时间 \n" \
             "*@precondition:\n" \
             "*@postcondition: \n" \
             "*/\n"
        fd = fd + "ZOO_INT32 " + self._component_id + "4I_send_request_and_reply(IN const MQ4A_SERV_ADDR server,\n" \
                                                      "													IN " + self._component_id + "4I_REQUEST_STRUCT  *request_message,\n" \
                                                                                                                                       "													INOUT " + self._component_id + "4I_REPLY_STRUCT *reply_message,\n" \
                                                                                                                                                                                                                           "													IN ZOO_INT32 timeout)\n"
        fd = fd + "{\n" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    ZOO_INT32 request_length = 0;/*发送消息长*/\n" \
                  "    ZOO_INT32 reply_length = 0;/*应该接收消息长度*/\n" \
                  "    ZOO_INT32 actual_reply_length = 0;/*实际接收数据长度*/\n\n" \
                  "    if(request_message == NULL)\n" \
                  "    {\n" \
                  "        result = " + self._component_id + "4A_PARAMETER_ERR;\n" \
                                                             "    }\n\n" \
                                                             "    if(result == OK)\n" \
                                                             "    {\n" \
                                                             "        result = " + self._component_id + "4I_get_request_message_length(request_message->request_header.function_code, &request_length);\n" \
                                                                                                        "    }\n\n" \
                                                                                                        "    if(result == OK)\n" \
                                                                                                        "    {\n" \
                                                                                                        "        result = " + self._component_id + "4I_get_reply_message_length(reply_message->reply_header.function_code, &reply_length);\n" \
                                                                                                                                                   "    }\n\n" \
                                                                                                                                                   "    if(result == OK)\n" \
                                                                                                                                                   "    {\n" \
                                                                                                                                                   "        result = MQ4A_send_request_and_reply(server,\n" \
                                                                                                                                                   "												request_message,\n" \
                                                                                                                                                   "												request_length,\n" \
                                                                                                                                                   "												reply_message,\n" \
                                                                                                                                                   "												reply_length,\n" \
                                                                                                                                                   "												&actual_reply_length,\n	" \
                                                                                                                                                   "											    " + self._component_id + "4I_RETRY_INTERVAL,\n" \
                                                                                                                                                                                                                             "												timeout);\n    }\n\n" \
                                                                                                                                                                                                                             " 	return result;\n" \
                                                                                                                                                                                                                             "}"
        return fd

    def get_send_request_message_difinition(self):
        fd = "/*\n" \
             "*@brief 向目标地址发送消息，异步接口，非阻塞，配合XX4I_receive_reply_message\n" \
             "*@param MQ4A_SERV_ADDR   服务器地址\n" \
             "*@param *request_message 请求消息 \n" \
             "*@precondition:\n*@postcondition:\n" \
             "*/\n"
        fd = fd + "ZOO_INT32 " + self._component_id + "4I_send_request_message(IN const MQ4A_SERV_ADDR server,\n" \
                                                      "													IN " + self._component_id + "4I_REQUEST_STRUCT *request_message)\n"
        fd = fd + "\n{\n" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    ZOO_INT32 request_length = 0;/* 发送的消息长度 */\n" \
                  "    /*查询发送请求消息的长度*/\n" \
                  "    if ( OK == result )\n" \
                  "    {\n" \
                  "        result = " + self._component_id + "4I_get_request_message_length(request_message->request_header.function_code, &request_length );\n\n" \
                                                             "    }\n\n" \
                                                             "    /*发送消息*/\n" \
                                                             "    if ( OK == result )\n" \
                                                             "    {\n" \
                                                             "        result = MQ4A_send_request( server,				 /*发送目标服务器地址*/\n" \
                                                             "                                    request_message,					 /*发送消息体*/\n" \
                                                             "                                    request_length,						 /*发送消息长*/\n" \
                                                             "                                    " + self._component_id + "4I_RETRY_INTERVAL );           /*发送间隔时*/\n" \
                                                                                                                           "    }\n\n" \
                                                                                                                           "    return result;\n" \
                                                                                                                           "}"
        return fd

    def get_receive_reply_message_difinition(self):
        fd = "/*\n" \
             "*@brief 接收目标消息\n	" \
             "*@param server         服务器地址\n" \
             "*@param function_code  函数码\n" \
             "*@param *reply_message 返回消息\n" \
             "*@param timeout        超时时间\n" \
             "*@description:         异步接口，配合XX4I_send_request_message一起使用\n" \
             "*@precondition:\n" \
             "*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_INT32 " + self._component_id + "4I_receive_reply_message(IN const MQ4A_SERV_ADDR server,\n" \
                                                      "													IN ZOO_INT32 function_code,\n" \
                                                      "													INOUT " + self._component_id + "4I_REPLY_STRUCT *reply_message,\n" \
                                                                                                                                          "													IN ZOO_INT32 timeout)\n"

        fd = fd + "{\n" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    ZOO_INT32 actual_replay_length = 0;    /*实际接收数据长度*/\n" \
                  "    ZOO_INT32 reply_length = 0; /*应该接收长度*/\n" \
                  "    result = " + self._component_id + "4I_get_reply_message_length( function_code, &reply_length );\n" \
                                                         "    /*接收返回消息*/\n" \
                                                         "    if ( OK == result )\n" \
                                                         "    {\n" \
                                                         "        result = MQ4A_get_reply( server, \n" \
                                                         "                  					reply_message,\n" \
                                                         "                       				reply_length,\n" \
                                                         "										&actual_replay_length,\n" \
                                                         "								        timeout );\n" \
                                                         "     }\n\n" \
                                                         "    return result;\n" \
                                                         "}"
        return fd

    def get_publish_event_difinition(self):
        fd = "/*\n" \
             "*@brief 向目标地址发布消息，订阅的用户可以收到消息\n" \
             "*@param event_id       消息的编号，一般指函数码\n" \
             "*@param *reply_message 消息结构体，函数参数组合\n" \
             "*@description:         需要先订阅，才能收到 \n" \
             "*@precondition:\n*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_INT32 " + self._component_id + "4I_publish_event(IN const MQ4A_SERV_ADDR server,\n" \
                "													IN ZOO_INT32 event_id,\n" \
                "													INOUT " + self._component_id + "4I_REPLY_STRUCT *reply_message)\n"
        fd = fd + "{\n" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    ZOO_INT32 reply_length = 0;\n" \
                  "    result = " + self._component_id + "4I_get_reply_message_length(reply_message->reply_header.function_code, &reply_length);\n" \
                  "    if (OK == result)\n" \
                  "    {\n" \
                  "         result = MQ4A_publish( server,\n" \
                  "								    event_id,\n" \
                  " 								reply_message,\n" \
                  "								    reply_length );\n" \
                  "    }\n\n" \
                  "    return result;\n" \
                  "}"
        return fd

    def get_send_subscribe_difinition(self):
        fd = "/*\n" \
             "*@brief 发送订阅消息\n*@param server            服务器地址\n" \
             "*@param callback_function 本地回调处理函数\n" \
             "*@param callback_struct   接口回调结构体\n" \
             "*@param event_id          请求消息\n" \
             "*@param *handle           订阅输出句柄\n" \
             "*@param *context          上下文标识\n " \
             "*@precondition:\n*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_INT32 " + self._component_id + "4I_send_subscribe(IN const MQ4A_SERV_ADDR server,\n" \
                                                      "													IN MQ4A_EVENT_CALLBACK_FUNCTION callback_function,\n" \
                                                      "													IN MQ4A_CALLBACK_STRUCT *callback_struct,\n" \
                                                      "													IN ZOO_INT32 event_id,\n" \
                                                      "													INOUT ZOO_HANDLE *handle,\n" \
                                                      "													INOUT void *context)\n"
        fd = fd + "{\n" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    //ZOO_INT32 reply_length = 0;\n" \
                  "    //result = " + self._component_id + "4I_get_reply_message_length(event_id, &reply_length);\n" \
                                                         "    if(OK == result)\n" \
                                                         "    {\n" \
                                                         "        result = MQ4A_subscribe( server,\n" \
                                                         "										    callback_function,\n" \
                                                         "											callback_struct,\n" \
                                                         "											event_id,\n" \
                                                         "											handle,\n" \
                                                         "											context);\n" \
                                                         "    }\n" \
                                                         "    return result;\n" \
                                                         "}"
        return fd

    def get_send_unsubscribe_difinition(self):
        fd = "/*\n" \
             "*@brief 取消订阅\n" \
             "*@param server   服务器地址\n" \
             "*@param event_id 请求消息\n" \
             "*@param handle   订阅输出句柄 \n" \
             "*@precondition:\n" \
             "*@postcondition:\n" \
             "*/\n"
        fd = fd + "ZOO_INT32 " + self._component_id + "4I_send_unsubscribe(IN const MQ4A_SERV_ADDR server,\n" \
                                                      "													IN ZOO_INT32 event_id,\n" \
                                                      "													IN ZOO_HANDLE handle)\n"
        fd = fd + "{\n" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    result = MQ4A_unsubscribe( server,\n" \
                  "									 event_id,\n" \
                  "								   	 handle );\n" \
                  "    return result;\n" \
                  "}"
        return fd

    def get_send_signal_difinition(self):
        fd = "/*\n" \
             "*@brief 发送信号消息\n" \
             "*@param server  服务器地址\n" \
             "*@param message 请求消息\n" \
             "*@param message_length   请求消息长度\n" \
             "*@precondition:\n*@postcondition:\n" \
             "*/" \
             "\n"

        fd = fd + "ZOO_INT32 " + self._component_id + "4I_send_signal(IN const MQ4A_SERV_ADDR server,\n" \
                                                      "													IN void * message,\n" \
                                                      "													IN ZOO_INT32 message_length)\n"
        fd = fd + "{\n" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    if (OK == result)\n" \
                  "    {\n" \
                  "         result = MQ4A_push( server,\n" \
                  "								    message,\n" \
                  "								    message_length);\n" \
                  "    }\n\n" \
                  "    return result;\n" \
                  "}"
        return fd


    def generate(self):
        with open(self._path + '/' + self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")
            for incld in FILE_INCLUDE_CLASS([self._component_id + "4I_if.h"]).get_list():
                f.write(incld)
                f.write("\n")
            f.write(self.get_request_message_length_function_difinition())
            f.write("\n\n")
            f.write(self.get_reply_message_length_function_difinition())
            f.write("\n\n")
            f.write(self.get_send_request_and_reply_function_difinition())
            f.write("\n\n")
            f.write(self.get_send_request_message_difinition())
            f.write("\n\n")
            f.write(self.get_receive_reply_message_difinition())
            f.write("\n\n")
            f.write(self.get_publish_event_difinition())
            f.write("\n\n")
            f.write(self.get_send_subscribe_difinition())
            f.write("\n\n")
            f.write(self.get_send_unsubscribe_difinition())
            f.write("\n\n")
            f.write(self.get_send_signal_difinition())
            f.write("\n\n")

        return


class XX4A_main_c(object):
    def __init__(self, component_id='', function_list=[], path=''):
        self._component_id = component_id
        self._function_list = function_list
        self._path = path
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', component_id + 'MA_main.c')
        self._file_name = path + '/' + self._component_id + "MA_main.c"
        self._server = component_id + "4A_SERVER"
        self._callback_handler = component_id + "MA_callback_handler"

    def generate(self):
        with open(self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")

            f.write("\n")
            for c in FILE_INCLUDE_CLASS(
                    ["string.h", "ZOO.h", "MQ4A_if.h", "MQ4A_type.h", "MM4A_if.h", self._component_id + "4I_type.h",self._component_id + "4A_implement.h",
                     self._component_id + "MA_dispatch.h"]).get_list():
                f.write(c)
                f.write("\n")

            f.write("\n\n")
            f.write("ZOO_INT32 main(int argc,char *argv[])")
            f.write("\n")
            f.write("{")
            f.write("\n")
            f.write("    ZOO_INT32 rtn = OK;\n"
                    "    /* 服务器地址 */\n"
                    "    MQ4A_SERV_ADDR server_addr = {0};\n"
                    "    MQ4A_SERVER_MODE_ENUM server_mode = MQ4A_SERVER_MODE_SYNC;/* 同步模式 */\n"
                    "    if(argc >= 2 )\n"
                    "    {\n"
                    "        strncpy(server_addr, argv[1], strlen(argv[1]));\n"
                    "        server_addr[31]= '\\0';\n"
                    "    }\n"
                    "    else\n"
                    "    {\n"
                    "        strncpy(server_addr," + self._server + ",strlen(" + self._server + "));\n"
                    "    }\n"                    
                    "    /* 初始化XX模块，用于创建实例*/\n"
                    "    " + self._component_id +"4A_startup();\n"     
                    "    /* 初始化内存池 */\n"
                    "    MM4A_initialize();\n"                                                 
                    "    if(OK == rtn)\n"
                    "    {\n"
                    "        /* 初始化服务器 */\n "
                    "        rtn = MQ4A_server_initialize(server_addr,server_mode);/* 初始化服务端 */\n"
                    "    }\n"
                    "    if(OK == rtn)\n"
                    "    {\n"
                    "        /* 注册服务端处理消息回调函数，用于接收客户端消息并转发到服务端内部接口 */\n"
                    "        rtn = MQ4A_register_event_handler(server_addr," + self._callback_handler + ");\n"
                    "    }\n"
                    "    if(OK == rtn)\n"
                    "    {\n"
                    "        /* 服务端进入事件监听状态 */\n"
                    "        rtn = MQ4A_enter_event_loop(server_addr);\n"
                    "    }\n"
                    "    /* 终止服务端 */\n"
                    "    MQ4A_server_terminate(server_addr);\n"
                    "    MM4A_terminate();\n"
                    "    " + self._component_id +"4A_shutdown();\n"                                                                                                        
                    "    return rtn;\n")
            f.write("}")
            f.write("\n")
        return


class XX4A_dispatch_h(object):
    def __init__(self, component_id='', function_list=[], path=''):
        self._component_id = component_id
        self._function_list = function_list
        self._path = path
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', component_id + 'MA_dispatch.h')
        self._file_name = path + '/' + component_id + "MA_dispatch.h"
        self._callback_handler = component_id + "MA_callback_handler"

    def generate(self):
        with open(self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")

            f.write("\n")
            file_name = self._component_id + "MA_dispatch.h"
            f.write(get_ifndef(file_name))
            for c in FILE_INCLUDE_CLASS(["ZOO.h",
                                         "MQ4A_if.h",
                                         "MQ4A_type.h",
                                         "MM4A_if.h",
                                         self._component_id + "4I_type.h",
                                         self._component_id + "4A_type.h",
                                         self._component_id + "MA_implement.h",
                                         ]).get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")
            f.write("/**\n")
            f.write("*@brief " + "dispatch message from client to server internal interface\n")
            f.write("*@param context       " + " \n")
            f.write("*@param server        " + "address\n")
            f.write("*@param msg           " + "request message to server\n")
            f.write("*@param len           " + "request message length\n")
            f.write("*@param reply_msg     " + "reply message length to caller\n")
            f.write("*@param reply_msg_len " + "reply message length\n")
            f.write("**/\n")
            f.write(
                "ZOO_EXPORT void " + self._callback_handler + "(void * context,const MQ4A_SERV_ADDR server,void * msg,ZOO_INT32 len,void ** reply_msg,ZOO_INT32 * reply_msg_len);")
            f.write("\n\n")
            f.write(get_endif(file_name))
        return


class XX4A_dispatch_c(object):
    def __init__(self, component_id='', function_list=[], path=''):
        self._component_id = component_id
        self._function_list = function_list
        self._path = path
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', component_id + 'MA_dispatch.c')
        self._file_name = path + '/' + component_id + "MA_dispatch.c"
        self._callback_handler = component_id + "MA_callback_handler"

    def generate(self):
        with open(self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")

            f.write("\n")
            for c in FILE_INCLUDE_CLASS(["EH4A_if.h",
                                         "TR4A_if.h",
                                         self._component_id + "MA_dispatch.h",
                                         self._component_id + "MA_implement.h"]).get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")

            for func in self._function_list:
                if func.get_interface_type() == 'Sync':
                    f.write(func.get_comment(func.get_local_name()))
                    f.write(func.get_local_function(self._component_id))
                    f.write(func.get_local_function_body(self._component_id))
                    f.write("\n")

            f.write("/**\n")
            f.write("*@brief " + "dispatch message from client to server internal interface\n")
            f.write("*@param context       " + " \n")
            f.write("*@param server        " + "address\n")
            f.write("*@param msg           " + "request message to server\n")
            f.write("*@param len           " + "request message length\n")
            f.write("*@param reply_msg     " + "reply message length to caller\n")
            f.write("*@param reply_msg_len " + "reply message length\n")
            f.write("**/\n")
            f.write(
                "void " + self._callback_handler + "(void * context,const MQ4A_SERV_ADDR server,void * msg,ZOO_INT32 len,void ** reply_msg,ZOO_INT32 * reply_msg_len)")
            f.write("\n")
            f.write("{\n")
            f.write(
                "    " + self._component_id + "4I_REQUEST_STRUCT *request = (" + self._component_id + "4I_REQUEST_STRUCT*)msg;\n"
                "    *reply_msg_len = sizeof(" + self._component_id + "4I_REPLY_STRUCT);\n"
                "    " + self._component_id + "4I_REPLY_STRUCT * reply = (" + self._component_id + "4I_REPLY_STRUCT *) MM4A_malloc(sizeof(" + self._component_id + "4I_REPLY_STRUCT));\n"
                "    *reply_msg = reply;\n    if(request == NULL)\n"
                "    {\n"
                "        EH4A_show_exception(COMPONENT_ID_" + self._component_id + ",__FILE__,__ZOO_FUNC__,__LINE__," + self._component_id + "4A_PARAMETER_ERR,\"request_message pointer is NULL ...ERROR\");\n"
                "        return;\n"
                "    }\n\n"
                "    if(reply_msg == NULL)\n"
                "    {\n"
                "        EH4A_show_exception(COMPONENT_ID_" + self._component_id + ",__FILE__,__ZOO_FUNC__,__LINE__," + self._component_id + "4A_PARAMETER_ERR,\"reply_message pointer is NULL ...ERROR\");\n"
                "        return;\n"
                "    }\n\n")
            f.write("    switch(request->request_header.function_code)")
            f.write("\n    {\n")
            for func in self._function_list:
                if func.get_interface_type() == 'Sync':
                    f.write("        " + "case " + func.get_function_code_upper() + ":\n")
                    f.write("            " + func.get_local_name() + "(server,request,reply);" + "\n")
                    f.write("            break;\n")
            f.write("        default:\n")
            f.write(
                "            EH4A_show_exception(COMPONENT_ID_" + self._component_id + ",__FILE__,__ZOO_FUNC__,__LINE__," + self._component_id + "4A_PARAMETER_ERR,\"invalid function code ...ERROR\");\n")
            f.write("            break;\n")
            f.write("     }\n")
            f.write("}\n\n")
        return


class XX4A_event_h(object):
    def __init__(self, component_id='', function_list=[], path='', callback_list=[]):
        self._component_id = component_id
        self._function_list = function_list
        self._callback_list = callback_list
        self._path = path
        self._file_name = self._component_id + "MA_event.h"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', component_id + 'MA_event.h')

    def generate(self):
        with open(self._path + '/' + self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            for c in FILE_INCLUDE_CLASS(["string.h", "stdio.h", "stdlib.h", "ZOO.h",
                                         "MQ4A_if.h",
                                         "MQ4A_type.h",
                                         "MM4A_if.h",
                                         "EH4A_if.h",
                                         "TR4A_if.h",
                                         self._component_id + "4I_type.h",
                                         self._component_id + "4A_type.h",
                                         ]).get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")

            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write(func.get_comment(func.get_event_name()))
                    f.write(func.get_event_function_definition(self._component_id))
                    f.write("\n")
                if func.get_interface_type() == "subscribe":
                    for callback in self._callback_list:
                        callback_type = callback.get_name()
                        # print("callback_type                   -------------------:" + callback_type)
                        func_call = ''
                        for pm in func.get_input_parameters_list():
                            func_call = pm
                            # print("func_call                   -------------------:" + pm.get_type())
                            if pm.get_type() in callback_type:
                                f.write(callback.get_comment(func.get_function_name()))
                                f.write(callback.get_function_difinition(func.get_function_name(), self._component_id))
                                f.write("\n")
                            break
                f.write("\n")
            f.write("\n")
            f.write(get_endif(self._file_name))
        return


class XX4A_event_c(object):
    def __init__(self, component_id='', function_list=[], path='', callback_list=[]):
        self._component_id = component_id
        self._function_list = function_list
        self._callback_list = callback_list
        self._path = path
        self._file_name = self._component_id + "MA_event.c"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', component_id + 'MA_event.c')

    def generate(self):
        with open(self._path + '/' + self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")

            for c in FILE_INCLUDE_CLASS([self._component_id + 'MA_event.h']).get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")

            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write(func.get_comment(func.get_event_name()))
                    f.write(func.get_event_function(self._component_id))
                    f.write("\n")
                    f.write(func.get_event_function_body(self._component_id))
                    f.write("\n")
                if func.get_interface_type() == "subscribe":
                    for callback in self._callback_list:
                        callback_type = callback.get_name()
                        # print("callback_type                   -------------------:" + callback_type)
                        func_call = ''
                        for pm in func.get_input_parameters_list():
                            func_call = pm
                            # print("func_call                   -------------------:" + pm.get_type())
                            if pm.get_type() in callback_type:
                                f.write(callback.get_comment(func.get_function_name()))
                                f.write(callback.get_function_name(func.get_function_name()))
                                f.write("\n")
                                f.write(callback.get_function_body(func, self._component_id))
                                f.write("\n")
                            break
            f.write("\n")
        return


class XX4A_implement_h(object):
    def __init__(self, component_id='', function_list=[], path=''):
        self._component_id = component_id
        self._function_list = function_list
        self._path = path
        self._file_name = self._component_id + "MA_implement.h"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', component_id + 'MA_implement.h')

    def generate(self):
        with open(self._path + '/' + self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            for c in FILE_INCLUDE_CLASS(["string.h", "stdlib.h", "stdio.h", "ZOO.h",
                                         "MQ4A_if.h",
                                         "MQ4A_type.h",
                                         "MM4A_if.h",
                                         "EH4A_if.h",
                                         "TR4A_if.h",
                                         self._component_id + "MA_event.h",
                                         self._component_id + "4I_type.h",
                                         self._component_id + "4A_type.h",
                                         ]).get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")
            f.write("\n")
            f.write("/**\n *@brief startup system \n**/\n")
            f.write("ZOO_EXPORT void " + self._component_id + "4A_startup(void);\n\n")
            f.write("/**\n *@brief shutdown system \n**/\n")
            f.write("ZOO_EXPORT void " + self._component_id + "4A_shutdown(void);\n\n")
            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write(func.get_comment(func.get_implement_name()))
                    f.write(func.get_implement_function_definition(self._component_id))
                    f.write("\n")
            f.write("\n")
            f.write(get_endif(self._file_name))
        return


class XX4A_implement_c(object):
    def __init__(self, component_id='', function_list=[], path=''):
        self._component_id = component_id
        self._function_list = function_list
        self._path = path
        self._file_name = self._component_id + "MA_implement.c"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', component_id + 'MA_implement.c')

    def generate(self):
        with open(self._path + '/' + self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")

            for c in FILE_INCLUDE_CLASS([self._component_id + 'MA_implement.h']).get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")

            f.write("/**\n *@brief startup system \n**/ \nvoid " + self._component_id + "4A_startup(void)\n{\n"
                                                   "    /** usr add */\n}\n\n")

            f.write("/**\n *@brief shutdown system \n**/ \nvoid " + self._component_id + "4A_shutdown(void)\n{\n"
                                                                                        "    /** usr add */\n}\n\n")
            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write(func.get_comment(func.get_implement_name()))
                    f.write(func.get_implement_function(self._component_id))
                    f.write("\n")
                    f.write(func.get_implement_function_body(self._component_id))
                    f.write("\n")
            f.write("\n")
        return


class Makefile(object):
    def __init__(self, component_id='', path=''):
        self._component_id = component_id
        self._path = path
        self._bin_makefile_name = component_id + "MA.mk"
        self._lib_makefile_name = "lib" + component_id + "4A.mk"

    def generate_makefile(self):

        if not os.path.exists(self._path + '/' + self._bin_makefile_name):
            with open(self._path + '/' + self._bin_makefile_name, 'w+') as f:
                f.write("include ../Makefile_tpl_cov\n\n" \
                        "TARGET   := " + self._component_id + "MA\n" \
                          "SRCEXTS  := .c\n" \
                          "INCDIRS  := ./inc ./com\n" \
                          "SOURCES  := \n" \
                          "SRCDIRS  := ./bin ./lib\n" \
                          "CFLAGS   := \n" \
                          "CXXFLAGS := -std=c++11\n" \
                          "CPPFLAGS := \n" \
                          "LDFPATH  := \n" \
                          "LDFLAGS  := $(GCOV_LINK) $(LDFPATH) -lTR4A -lEH4A -lMM4A -lMQ4A -lCOMMON\n\n" \
                          "include ../Project_config\n" \
                          "include ../Makefile_tpl_zoo")

        if not os.path.exists(self._path + '/' + self._lib_makefile_name):
            with open(self._path + '/' + self._lib_makefile_name, 'w+') as f:
                f.write("include ../Makefile_tpl_cov\n" \
                        "TARGET   := lib" + self._component_id + "4A.so\n" \
                        "SRCEXTS  := .cpp\n" \
                        "INCDIRS  := ./inc ./com\n" \
                        "SOURCES  := ./lib/"+self._component_id+"4A.cpp ./lib/"+self._component_id+"4I.cpp\n" \
                        "SRCDIRS  :=\n" \
                        "CFLAGS   :=\n" \
                        "CXXFLAGS := -std=c++11\n" \
                        "CPPFLAGS := $(GCOV_FLAGS)  -fPIC\n" \
                        "LDFLAGS  := $(GCOV_LINK)  -lnsl -shared\n\n" \
                        "include ../Project_config\n" \
                        "include ../Makefile_tpl_zoo")
        return



def search_header_file(dir=''):
    list = os.listdir(dir)
    path = os.listdir(dir)
    print("current dir :" + dir)
    file_list = []
    for p in path:
        if os.path.isfile(p):
            print("file: " + p)
            file_list.append(p)
    return file_list


# **
# @ search interface header file
# @ return 1 found else fail
# **
def check_is_interface_header_file(file_name=''):
    # print("intput fileName = " + file_name)
    result = file_name.find("4A_if.h")
    if result > -1:
        # print("find XX4A_if file: true")
        return 1  # find = true
    else:
        # print("find XX4A_if file: false")
        return 0  # find = true


def parse_component_id(file=''):
    print("intput fileName = " + file)
    patten = re.compile(r'(\w*)4A_[^.]')
    id = patten.findall(file)
    print(id)
    return id[0]


# **
# @ search interface header file
# @ return 1 found else fail
# **
def check_is_type_header_file(file_name=''):
    print("intput fileName = " + file_name)
    result = file_name.find("4A_type.h")
    # print(result)
    if result > -1:
        # print("find XX4A_type.h file: true")
        return 1  # find = true
    else:
        # print("find XX4A_type.h file: failed")
        return 0  # find = true


def CopyFile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print(srcfile)
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件


def CopyHeaderFile(file):
    component_id = parse_component_id(file)
    print("component_id: " + component_id)
    XX_DIR_GENERATOR(component_id)
    src_dir = os.getcwd() + "/" + file
    dst_dir = os.getcwd() + "/" + component_id + '/inc/' + file
    print("src file: " + src_dir)
    print("dst file: " + dst_dir)
    CopyFile(src_dir, dst_dir)


def FileGenenrator(XX4A_if='', XX4A_type=''):
    component_id = parse_component_id(XX4A_if)
    xx_dir = XX_DIR_GENERATOR(component_id)
    inc_dir = xx_dir.get_inc_path()
    lib_dir = xx_dir.get_lib_path()
    com_dir = xx_dir.get_com_path()
    bin_dir = xx_dir.get_bin_path()
    xx4a_if_h = XX4A_IF_HEADER_CLASS(os.getcwd() + "/" + XX4A_if)
    xx4a_type_h = XX4A_TYPE_HEADER_CLASS(os.getcwd() + "/" + XX4A_type)
    product = xx4a_if_h.get_product()
    function_list = xx4a_if_h.get_function_list()
    callback_list = xx4a_if_h.get_callback_list()
    XX4I_type_h(component_id, function_list, callback_list, inc_dir).generate()
    XX4A_c(component_id, function_list, callback_list, lib_dir).generate()
    XX4I_if_h(component_id, function_list, inc_dir).generate()
    XX4I_c(component_id, function_list, lib_dir).generate()
    XX4A_event_h(component_id, function_list, com_dir, callback_list).generate()
    XX4A_event_c(component_id, function_list, bin_dir, callback_list).generate()
    XX4A_implement_h(component_id, function_list, com_dir).generate()
    XX4A_implement_c(component_id, function_list, bin_dir).generate()
    XX4A_dispatch_h(component_id, function_list, com_dir).generate()
    XX4A_dispatch_c(component_id, function_list, bin_dir).generate()
    XX4A_main_c(component_id, function_list, bin_dir).generate()
    CopyHeaderFile(XX4A_if)
    CopyHeaderFile(XX4A_type)
    Makefile(component_id, os.getcwd() + "/" + component_id).generate_makefile()
    return


def ComponentGenerator():
    root_dir = os.getcwd()
    print(root_dir)
    header_file_list = search_header_file(root_dir)
    type_file = ''
    if_file_list = []
    for file in header_file_list:
        if check_is_interface_header_file(file):
            if_file_list.append(file)
            print(file)

    for file in header_file_list:
        if check_is_type_header_file(file):
            type_file = file
            break

    for if_h in if_file_list:
        FileGenenrator(if_h, type_file)
    return


if __name__ == '__main__':
    ComponentGenerator()
