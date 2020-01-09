#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a interprocess communication code generator which use header file XX4A_if.h XX4A_type.h  '
import codecs
import getopt
import os
import re
import shutil
import sys
import time
from symbol import parameters
__author__ = 'Weiwang Sun'



def type_to_size(type="ZOO_INT32", array=''):
    type = type.strip("const").strip().strip("*")
    if type == "ZOO_INT32":
        if "[" in array:
            return 8
        else:
            return 4
    if type == "ZOO_UINT32":
        if "[" in array:
            return 8
        else:
            return 4
    if type == "ZOO_LONG":
        if "[" in array:
            return 8
        else:
            return 4
    if type == "ZOO_CHAR" or type in "char" :
        if "[" in array:
            return 8
        else:
            return 1
    if type == "ZOO_DOUBLE":
        return 8
    if type == "ZOO_INT16":
        return 4
    if type == "ZOO_UINT16":
        if "[" in array:
            return 8
        else:
            return 4
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
        if "[" in array:
            return 8
        else:
            return 4
    if "unsigned int" in type:
        if "[" in array:
            return 8
        else:
            return 4
    if "CALLBACK_FUNCTION" in type:
        return 4
    if "bool" in type:
        return 1
    if "char" in type:
        return 1
    return 4

def is_char_type(s):
    if "ZOO_CHAR" in s or "char" in s:
        return 1
    else:
        return 0

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
    def __init__(self, product='', compoent_id='', filename='', description='{Summary Description}',
                 author='Generator', context='created'):
        self._product = product
        self._compoent_id = compoent_id
        self._filename = filename
        self._description = description
        self._version = 'V1.0.0'
        self._date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        self._author = author
        self._context = context

    def add_property(self, product, compoent_id, filename, description, author, context):
        self._product = product
        self._compoent_id = compoent_id
        self._filename = filename
        self._description = description
        self._author = author
        self._context = context

    def get_list(self):
        tmplist = []
        tmplist.append('/***********************************************************')
        tmplist.append(' * Copyright (C) 2018, Shanghai NIO VEHICLE CO., LTD')
        tmplist.append(' * All rights reserved.')
        tmplist.append(' * Product        : ' + self._product)
        tmplist.append(' * Component id   : ' + self._compoent_id)
        tmplist.append(' * File Name      : ' + self._filename)
        tmplist.append(' * Description    : ' + self._description)
        tmplist.append(' * History        : ')
        tmplist.append(' * Version        date          author         context ')
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
                if "st" in fl or "std" in fl or "MQ" in fl or "ZOO_COMMON_MACRO_DEFINE" in fl or "ZOO" in fl or "MM" in fl or "CM" in fl or "BD" in fl or "EH" in fl or "TR" in fl:
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
            #print(m[0])
            result = m[0]
        return result

    def remove_variable_with_asterisk(self):
        result = self._name
        return result.strip("*")

    def check_variable_contain_square_brackets(self):
        if '[' in self._name:
            return 1
        return 0

    def check_variable_contain_asterisk(self):
        if '*' in self._type:
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

    def get_pure_name(self):
        result = self._name
        if "[" in self._name:
            m = re.match(r"(.*)(\[)",self._name)
            print(m)
            result = m[1]
        elif "*" in result:
            result = result.strip("*")
        return result

# *
# @brief function class define
# *
class FUNCTION_CLASS:
    def __init__(self, function='', code_index = 0):
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
        if function != '':
            self.get_function_name()
            self.get_input_parameters_list()
            self.get_output_parameters_list()
            self.get_inoutput_parameters_list()

    def get_comment(self, comment='',retract_num = 0):
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
    def get_wrapper_name(self):
        items = self._name.split("_")
        wrap_name = ''
        items[0] = ''
        for i in items:
            wrap_name = wrap_name + i + "_"
        wrap_name = wrap_name.strip('_') + "("
        print("wrap name : " + wrap_name)
        f = ''
        print("------------------------------------------------------------------------------")
        for i in self.get_input_parameters_list(): 
            f = f + i.get_pure_name() + ","

        for i in self.get_inoutput_parameters_list():
            if "*" in i.get_type() or "[" in i.get_name():
                f = f + i.get_pure_name() + ","
            else:
                f = f + "&" + i.get_name() + ","

        for i in self.get_output_parameters_list():
            if "*" in i.get_type() or "[" in i.get_name():
                f = f + i.get_pure_name() + ","
            else:
                f = f + "&" + i.get_name() + ","
        f = f.rstrip(",")
        wrap_name = wrap_name + f + ")"
        return wrap_name

    def get_wrapper_name_implement(self):
        items = self._name.split("_")
        wrap_name = ''
        items[0] = ''
        for i in items:
            wrap_name = wrap_name + i + "_"
        wrap_name = wrap_name.strip('_') + "("
        print("wrap name : " + wrap_name)
        f = ''
        for i in self.get_input_parameters_list():
            f = f + i.get_pure_name() + ","
        for i in self.get_inoutput_parameters_list():
            f = f + "&" + i.get_pure_name() + ","
        for i in self.get_output_parameters_list():
            f = f + "&" + i.get_pure_name() + ","
        f = f.rstrip(",")
        wrap_name = wrap_name + f + ")"
        return wrap_name

    def get_body(self, compoent_id=''):
        body = "{\n" \
                "    ZOO_INT32 result = OK;\n" \
                "    " + compoent_id + "4I_REQUEST_STRUCT *request_message = NULL; \n"
        if "_sig" in self._function:
            body =  body + ""
        else:
            body = body + "    " + compoent_id + "4I_REPLY_STRUCT *reply_message = NULL;	\n"
            body = body + "    ZOO_INT32 reply_length = 0;\n"
            body = body + "    ZOO_INT32 ZOO_timeout = 60000;\n"
        body = body + "    ZOO_INT32 request_length = 0;\n" \
                "    ZOO_INT32 func_code = " + self.get_function_code_upper() + ";\n" \
                "    result = " + compoent_id + "4I_get_request_message_length(func_code, &request_length);\n" \
                "    if(OK == result)\n" \
                "    {\n" \
                "        request_message = (" + compoent_id + "4I_REQUEST_STRUCT *)MM4A_malloc(request_length);\n" \
                "    }\n\n" \
                "    if(OK == result)\n" \
                "    {\n" \
                "        if(request_message == NULL)\n" \
                "        {\n" \
                "            result = " + compoent_id + "4A_PARAMETER_ERR;\n" \
                "        }\n" \
                "    }\n\n"
        if "_sig" in self._function:
            body =  body + ""
        else:
            body = body + "    if(OK == result)\n"
            body = body + "    {\n"
            body = body + "        result = " + compoent_id + "4I_get_reply_message_length(func_code, &reply_length);\n"
            body = body + "    }\n\n"
            body = body + "    if(OK == result)\n"
            body = body + "    {\n"
            body = body + "        reply_message = (" + compoent_id + "4I_REPLY_STRUCT *)MM4A_malloc(reply_length);\n"
            body = body + "    }\n\n"
            body = body + "    if(OK == result)\n"
            body = body + "    {\n"
            body = body + "        if(reply_message == NULL)\n"
            body = body + "        {\n"
            body = body + "            result = " + compoent_id + "4A_PARAMETER_ERR;\n"
            body = body + "        }\n"
            body = body + "    }\n\n"

        body = body +  "    if(OK == result)\n"
        body = body +  "    {\n"
        body = body +  "        request_message->request_header.function_code = func_code;\n"
        if "_sig" in self._function:
            body = body + ""
        else:
            body = body +  "        reply_message->reply_header.function_code = func_code;\n"

        if "_sig" in self._function:
            body = body + "        request_message->request_header.need_reply = ZOO_FALSE;\n"
        else:
            body = body + "        request_message->request_header.need_reply = ZOO_TRUE;\n"

        for pm in self._input_parameters:
            if pm.check_variable_contain_square_brackets():
                body = body + "        memcpy((void *)(&request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + "),&" + pm.get_name_with_square_brackets_header_addr() + ",sizeof(" + pm.get_type().replace("const","").strip() + ") * " + pm.get_array_length() + ");\n"

            elif "*" in pm.get_type():
                if "CHAR" in pm.get_type() or "char" in pm.get_type():
                    body = body + "        memcpy((void *)(&request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name() + "[0])," + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + ") * " + compoent_id + "4I_BUFFER_LENGTH" + ");\n"
                else:
                    body = body + "        memcpy((void *)(&request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name() + ")," + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + "));\n"

            else:
                body = body + "        memcpy((void *)(&request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name() + "),&" + pm.get_name() + ",sizeof(" + pm.get_type().replace("const","").strip() + "));\n"

        if "_sig" in self._function:
            body = body + "    }\n\n" \
                          "    if(OK == result)\n" \
                          "    {\n" \
                          "        result = " + compoent_id + "4I_send_request_message(" + compoent_id + "4A_SERVER,request_message);\n" \
                          "    }\n\n"
        else :
            body = body + "    }\n\n" \
                          "    if(OK == result)\n" \
                          "    {\n" \
                          "        result = " + compoent_id + "4I_send_request_and_reply(" + compoent_id + "4A_SERVER,request_message,reply_message,ZOO_timeout);\n" \
                          "    }\n\n"
        if "_sig" in self._function:
            body = body
        else:
            body = body + "    if(OK == result)\n" \
                          "    {\n" \
                          "        result = reply_message->reply_header.execute_result;\n"
        for pm in self._output_parameters:
            if pm.check_variable_contain_square_brackets():
                body = body + "        memcpy(&" + pm.get_name_with_square_brackets_header_addr() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + ",sizeof(" + pm.get_type().replace("const","").strip() + ") * " + pm.get_array_length() + ");\n"
            elif "*" in pm.get_type():
                if "CHAR" in pm.get_type() or "char" in pm.get_type():
                    body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + ") * " + compoent_id + "4I_BUFFER_LENGTH" + ");\n"
                else:
                    body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + "));\n"
            else:
                body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type() + "));\n"

        for pm in self._inoutput_parameters:
            if pm.check_variable_contain_square_brackets():
                body = body + "        memcpy(&" + pm.get_name_with_square_brackets_header_addr() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + ",sizeof(" + pm.get_type().replace("const","").strip() + ") * " + pm.get_array_length() + ");\n"
            elif "*" in pm.get_type():
                if "CHAR" in pm.get_type() or "char" in pm.get_type():
                    body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + ") * " + compoent_id + "4I_BUFFER_LENGTH" + ");\n"
                else:
                    body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + "));\n"
            else:
                body = body + "        memcpy(" + pm.get_name().strip(
                    "*") + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name().strip(
                    "*") + ",sizeof(" + pm.get_type().replace("const","").strip() + "));\n"
        if "_sig" in self._function:
            body = body
        else:
            body = body + "    }\n\n"
        body = body + "    if(request_message != NULL)\n" \
                      "    {\n" \
                      "        MM4A_free(request_message);\n" \
                      "    }\n\n"
        if "_sig" in self._function:
            body = body
        else:
            body = body + "    if(reply_message != NULL)\n" \
                      "    {\n" \
                      "        MM4A_free(reply_message);\n" \
                      "    }\n"
        body = body + "    return result;\n}\n"
        return body

    def get_body_req(self, compoent_id=''):
        body = "{\n" \
            "    ZOO_INT32 result = OK;\n" \
            "    " + compoent_id + "4I_REQUEST_STRUCT *request_message = NULL; \n" \
            "    ZOO_INT32 req_length = 0;\n" \
            "    ZOO_INT32 func_code = " + self.get_function_code_upper().replace(
            "_REQ", "") + ";\n" \
            "    result = " + compoent_id + "4I_get_request_message_length(func_code, &req_length);\n" \
            "    if(OK == result)\n" \
            "    {\n" \
            "        request_message = (" + compoent_id + "4I_REQUEST_STRUCT *)MM4A_malloc(req_length);\n" \
            "    }\n\n" \
            "    if(OK == result)\n" \
            "    {\n" \
            "        if(request_message == NULL)\n" \
            "        {\n" \
            "            result = " + compoent_id + "4A_PARAMETER_ERR;\n" \
            "        }\n" \
            "    }\n\n" \
            "    if(OK == result)\n" \
            "    {\n" \
            "        request_message->request_header.function_code = func_code;\n" \
            "        request_message->request_header.need_reply = ZOO_TRUE;\n"

        for pm in self._input_parameters:
            if pm.check_variable_contain_square_brackets():
                body = body + "        memcpy((void *)(&request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + "),&" + pm.get_name_with_square_brackets_header_addr() + ",sizeof(" + pm.get_type().replace("const","").strip() + ") * " + pm.get_array_length() + ");\n"
            elif "*" in pm.get_type():
                if "CHAR" in pm.get_type() or "char" in pm.get_type():
                    body = body + "        memcpy((void *)(&request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name() + "[0])," + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + ") * " + compoent_id + "4I_BUFFER_LENGTH" + ");\n"
                else:
                    body = body + "        memcpy((void *)(&request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name() + "[0])," + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + "));\n"
            else:
                body = body + "        memcpy((void *)(&request_message->request_body." + self.get_request_struct_var() + "." + pm.get_name() + "),&" + pm.get_name() + ",sizeof(" + pm.get_type().replace("const","").strip() + "));\n"

        body = body + "    }\n\n" \
                      "    if(OK == result)\n" \
                      "    {\n" \
                      "        result = " + compoent_id + "4I_send_request_message(" + compoent_id + "4A_SERVER,request_message);\n"

        body = body + "    }\n\n" \
                      "    if(request_message != NULL)\n        MM4A_free(request_message);\n" \
                      "    return result;\n}\n"
        return body

    def get_body_wait(self, compoent_id=''):
        body = "{\n" \
               "    ZOO_INT32 result = OK;\n" \
               "    " + compoent_id + "4I_REPLY_STRUCT *reply_message = NULL;	\n" \
               "    ZOO_INT32 ZOO_timeout = 60000;\n" \
               "    ZOO_INT32 reply_length = 0;\n" \
               "    ZOO_INT32 func_code = " + self.get_function_code_upper().replace("_WAIT", "") + ";\n" \
                           "    if(OK == result)\n" \
                           "    {\n" \
                           "        result = " + compoent_id + "4I_get_reply_message_length(func_code, &reply_length);\n" \
                           "    }\n\n" \
                           "    if(OK == result)\n" \
                           "    {\n" \
                           "        reply_message = (" + compoent_id + "4I_REPLY_STRUCT *)MM4A_malloc(reply_length);\n" \
                           "    }\n\n" \
                           "    if(OK == result)\n" \
                           "    {\n" \
                           "        if(reply_message == NULL)\n" \
                           "        {\n" \
                           "            result = " + compoent_id + "4A_PARAMETER_ERR;\n" \
                           "        }\n" \
                           "    }\n\n"
        body = body + "    if(OK == result)\n" \
                      "    {\n" \
                      "        result = " + compoent_id + "4I_receive_reply_message(" + compoent_id + "4A_SERVER,func_code,reply_message,ZOO_timeout);\n" \
                      "    }\n\n" \
                      "    if(OK == result)\n" \
                      "    {\n" \
                      "        result = reply_message->reply_header.execute_result;\n"

        for pm in self._output_parameters:
            if pm.check_variable_contain_square_brackets():
                body = body + "        memcpy(&" + pm.get_name_with_square_brackets_header_addr() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + ",sizeof(" + pm.get_type().replace("const","").strip() + ") * " + pm.get_array_length() + ");\n"
            elif "*" in pm.get_type():
                if "CHAR" in pm.get_type() or "char" in pm.get_type():
                    body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip("const").strip().strip("*") + ") * " + compoent_id + "4I_BUFFER_LENGTH" + ");\n"
                else:
                    body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip("const").strip().strip("*") + "));\n"
            else:
                body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type() + "));\n"

        for pm in self._inoutput_parameters:
            if pm.check_variable_contain_square_brackets():
                body = body + "        memcpy(&" + pm.get_name_with_square_brackets_header_addr() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + ",sizeof(" + pm.get_type().replace("const","").strip() + ") * " + pm.get_array_length() + ");\n"
            elif "*" in pm.get_type():
                if "CHAR" in pm.get_type() or "char" in pm.get_type():
                    body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + ") * " + compoent_id + "4I_BUFFER_LENGTH" + ");\n"
                else:
                    body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().strip(
                        "const").strip().strip("*") + "));\n"
            else:
                body = body + "        memcpy(" + pm.get_name() + ",&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",sizeof(" + pm.get_type().replace("const","").strip() + "));\n"

        body = body + "    }\n\n" \
                      "    if(reply_message != NULL)\n" \
                      "    {\n" \
                      "        MM4A_free(reply_message);\n" \
                      "    }\n" \
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
    def get_local_function_definition(self, compoent_id=''):
        buffer = "static void " + self.get_local_name() + "("
        buffer = buffer + "const MQ4A_SERV_ADDR server," + compoent_id + "4I_REQUEST_STRUCT * request," + compoent_id + "4I_REPLY_STRUCT * reply"
        buffer = buffer + ");\n"
        return buffer

    # const MQ4A_SERV_ADDR server,XX4I_REQUEST_STRUCT * request,XX4I_REPLY_STRUCT * reply
    def get_local_function(self, compoent_id=''):
        buffer = "static ZOO_INT32 " + self.get_local_name() + "("
        buffer = buffer + "const MQ4A_SERV_ADDR server," + compoent_id + "4I_REQUEST_STRUCT * request," + "ZOO_UINT32 msg_id)"
        return buffer

    def get_local_function_body(self, compoent_id=''):
        body = ''
        handle_type = compoent_id + "4I_REPLY_HANDLE"
        handler = compoent_id + "4I_REPLY_HANDLER_STRUCT"
        body = body + "\n{ \n"
        body = body + "    "+ handle_type + " reply_handle = NULL;\n"
        body = body + "    ZOO_INT32 rtn = OK;\n" \
                      "    if(request == NULL)\n" \
                      "    {\n" \
                      "        rtn = " + compoent_id + "4A_SYSTEM_ERR;\n" \
                      "        EH4A_show_exception(" + compoent_id + "4I_COMPONET_ID,__FILE__,__ZOO_FUNC__,__LINE__," + compoent_id + "4A_PARAMETER_ERR,0,\"request pointer is NULL ...ERROR\");\n" \
                      "        return rtn;\n" \
                      "    }\n\n" \
                      "    if(rtn == OK)\n" \
                      "    {\n" \
                      "        reply_handle = ("+handle_type+")MM4A_malloc(sizeof("+handler+"));\n" \
                      "        if(reply_handle == NULL)\n" \
                      "        {\n" \
                      "            rtn = " + compoent_id + "4A_SYSTEM_ERR;\n"\
                      "            EH4A_show_exception(" + compoent_id + "4I_COMPONET_ID,__FILE__,__ZOO_FUNC__,__LINE__," + compoent_id + "4A_SYSTEM_ERR,0,\"malloc reply_handle failed ...ERROR\");\n" \
                      "            return rtn;\n" \
                      "        }\n" \
                      "    }\n\n"\
                      "    if(OK == rtn)\n" \
                      "    {\n" \
                      "        memcpy(reply_handle->reply_addr,server,MQ4A_SERVER_LENGHT * sizeof(char));\n"\
                      "        reply_handle->msg_id = msg_id;\n"\
                      "        reply_handle->reply_wanted = request->request_header.need_reply;\n"\
                      "        reply_handle->func_id = request->request_header.function_code;\n"
        body = body + "        " + self.get_implement_name() + "("
        for pm in self.get_input_parameters_list():
            print("********************************************************************************************************")
            print(pm.get_type())
            print(pm.get_name())
            if "char" in pm.get_type() or "ZOO_CHAR" in pm.get_type():
                if pm.check_variable_contain_square_brackets():
                    body = body + "request->request_body." + self.get_request_struct_var() + "." + pm.get_name_without_square_brackets() + ",\n                                           "
                elif pm.check_variable_contain_asterisk():
                    body = body + "request->request_body." + self.get_request_struct_var() + "." + pm.get_name_without_square_brackets() + ",\n                                           "
                else:
                    body = body + "request->request_body." + self.get_request_struct_var() + "." + pm.get_name_without_asterisk() + ",\n                                           "
            else:
                if pm.check_variable_contain_square_brackets():
                    body = body + "request->request_body." + self.get_request_struct_var() + "." + pm.get_name_without_square_brackets() + ",\n                                           "
                elif pm.check_variable_contain_asterisk():
                    body = body + "&request->request_body." + self.get_request_struct_var() + "." + pm.get_name_without_square_brackets() + ",\n                                           "
                else:
                    body = body + "request->request_body." + self.get_request_struct_var() + "." + pm.get_name_without_asterisk() + ",\n                                           "

        body = body + 'reply_handle);\n'
        body = body + "    }\n    return rtn;\n}\n"
        return body

    def get_implement_name(self):
        l = self._name.split("4")
        id = l[0]
        name = id + "MA_implement_4" + l[1]
        return name

    def get_implement_function_definition(self, compoent_id=''):
        handle_type = compoent_id + "4I_REPLY_HANDLE"
        buffer = "ZOO_EXPORT void " + self.get_implement_name() + "("

        blank = ""
        for i in range(0, len(buffer)):
            blank = blank + " "
        l = 0
        for s in self._input_parameters:
            if l >= 1:
                buffer = buffer + blank + "    IN " + s.get_type() + " " + s.get_name() + ",\n"
            else:
                buffer = buffer + "IN " + s.get_type() + " " + s.get_name() + ",\n"
            l = l + 1
        if l == 0:
            buffer = buffer + "IN " + handle_type + " reply_handle);"
        else:
            buffer = buffer + blank + "    IN " + handle_type + " reply_handle);"
        return buffer

    def get_implement_function(self, compoent_id=''):
        handle_type = compoent_id + "4I_REPLY_HANDLE"
        buffer = "void " + self.get_implement_name() + "("
        blank = ""
        for i in range(0, len(buffer)):
            blank = blank + " "
        l = 0
        for s in self._input_parameters:
            if l >= 1 :
                buffer = buffer + blank + "    IN " + s.get_type() + " " + s.get_name() + ",\n"
            else:
                buffer = buffer + "IN " + s.get_type() + " " + s.get_name() + ",\n"
            l = l + 1
        if l == 0:
            buffer = buffer +  "IN " + handle_type + " reply_handle)"
        else:
            buffer = buffer + blank + "    IN " + handle_type + " reply_handle)"
        return buffer

    def get_implement_function_body(self, compoent_id=''):
        buffer = "{\n"
        buffer = buffer + "    ZOO_INT32 rtn = OK;\n"

        for pm in self._output_parameters:
            if pm.check_variable_contain_square_brackets():
                buffer = buffer + "    " + pm.get_type() + " " + pm.get_name() + ";\n"
                buffer = buffer + "    " + "memset(&" + pm.get_name_with_square_brackets_header_addr() + ",0,sizeof(" + pm.get_type() + ") * " + pm.get_array_length() + ");\n"
            elif "ZOO_INT" in pm.get_type():
                buffer = buffer + "    " + pm.get_type() + " " + pm.get_name() + "  = 0;\n"
            elif "_STRUCT" in pm.get_type() or "_struct" in pm.get_type():
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name() + " ;\n"
                buffer = buffer + "    " + "memset(&" + pm.get_name() + ",0,sizeof(" + pm.get_type().strip("*") + "));\n"
            elif "ZOO_FLOAT" in pm.get_type() or "ZOO_DOUBLE" in pm.get_type():
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name().strip("*") + "  = 0.0;\n"
            elif "ZOO_BOOL" in pm.get_type() :
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name().strip("*") + "  = ZOO_FALSE;\n"
            elif "bool" in pm.get_type() :
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name().strip("*") + "  = false;\n"
            elif "ZOO_CHAR" in pm.get_type() :
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name().strip("*") + "  = 0;\n"
            elif "char" in pm.get_type() :
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name().strip("*") + "  = 0;\n"
            else:
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name().strip("*") + ";\n"

        for pm in self._inoutput_parameters:
            if pm.check_variable_contain_square_brackets():
                buffer = buffer + "    " + pm.get_type() + " " + pm.get_name() + ";\n"
                buffer = buffer + "    " + "memset(&" + pm.get_name_with_square_brackets_header_addr() + ",0,sizeof(" + pm.get_type() + ") * " + pm.get_array_length() + ");\n"
            elif "ZOO_INT" in pm.get_type():
                buffer = buffer + "    " + pm.get_type() + " " + pm.get_name() + "  = 0;\n"
            elif "_STRUCT" in pm.get_type() or "_struct" in pm.get_type():
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name() + " ;\n"
                buffer = buffer + "    " + "memset(&" + pm.get_name() + ",0,sizeof(" + pm.get_type().strip("*") + "));\n"
            elif "ZOO_FLOAT" in pm.get_type() or "ZOO_DOUBLE" in pm.get_type():
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name().strip("*") + "  = 0.0;\n"
            elif "ZOO_BOOL" in pm.get_type() :
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name().strip("*") + "  = ZOO_FALSE;\n"
            elif "bool" in pm.get_type() :
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name().strip("*") + "  = false;\n"
            elif "ZOO_CHAR" in pm.get_type() :
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name().strip("*") + "  = 0;\n"
            elif "char" in pm.get_type() :
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name().strip("*") + "  = 0;\n"
            else:
                buffer = buffer + "    " + pm.get_type().strip("*") + " " + pm.get_name().strip("*") + ";\n"

        buffer = buffer + "    /* User add some code here if had special need. */\n"
        buffer = buffer + "    rtn = " + compoent_id +"_"+ self.get_wrapper_name_implement() + ";\n\n"

        if "_sig" in self._function:
            buffer = buffer + "    /* Do not reply a signal request.*/\n"
            buffer = buffer + "    if(reply_handle != NULL)\n" \
                              "    {\n" \
                              "        /* Ignore unused parameter warnning.*/\n" \
                              "        rtn = rtn;\n" \
                              "        MM4A_free(reply_handle);\n" \
                              "        reply_handle = NULL;\n" \
                              "    }\n"
        else:
            buffer = buffer + "    /* User add ... END*/\n"
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

            buffer = buffer + "reply_handle);\n"
        buffer = buffer + "}\n"
        return buffer

    def get_event_name(self):
        l = self._name.split("4")
        id = l[0]
        name = id + "MA_raise_4" + l[1]
        return name

    def get_event_function_definition(self, compoent_id=''):
        handle_type = compoent_id + "4I_REPLY_HANDLE"
        buffer = "ZOO_EXPORT ZOO_INT32 " + self.get_event_name()
        blank = ""
        for i in range(0, len(buffer)):
            blank = blank + " "
        buffer = buffer + "(IN ZOO_INT32 error_code,\n"
        l = 0
        for s in self._output_parameters:
            buffer = buffer + blank + "     IN " + s.get_type().strip("*") + " " + s.get_name() + ",\n"
        for s in self._inoutput_parameters:
            buffer = buffer + blank + "     IN " + s.get_type().strip("*") + " " + s.get_name() + ",\n"
        buffer = buffer + blank + "     IN " + handle_type + " reply_handle);\n"
        return buffer

    def get_event_function(self, compoent_id=''):
        handle_type = compoent_id + "4I_REPLY_HANDLE"
        buffer = "ZOO_INT32 " + self.get_event_name()
        blank = ""
        for i in range(0, len(buffer)):
            blank = blank + " "
        buffer = buffer + "(IN ZOO_INT32 error_code,\n"
        l = 0
        for s in self._output_parameters:
            buffer = buffer + blank + "     IN " + s.get_type().strip("*") + " " + s.get_name() + ",\n"
        for s in self._inoutput_parameters:
            buffer = buffer + blank + "     IN " + s.get_type().strip("*") + " " + s.get_name() + ",\n"
        buffer = buffer + blank + "     IN " + handle_type + " reply_handle)"
        return buffer

    def get_event_function_body(self, compoent_id=''):
        body = "{\n"
        body = body + "    "+compoent_id+"4I_REPLY_STRUCT* reply_message = NULL;\n"
        body = body + "    ZOO_INT32 rtn = OK;\n"
        body = body + "    ZOO_INT32 reply_length = 0;\n"
        body = body + "    if(reply_handle == NULL)\n"
        body = body + "    {\n"
        body = body + "        rtn = " + compoent_id + "4A_PARAMETER_ERR;\n"
        body = body + "        EH4A_show_exception(" + compoent_id + "4I_COMPONET_ID,__FILE__,__ZOO_FUNC__,__LINE__," + compoent_id + "4A_SYSTEM_ERR,0,\" reply_handle is null ...ERROR\");\n"
        body = body + "    }\n\n"
        body = body + "    if(OK == rtn)\n"
        body = body + "    {\n"
        body = body + "        if(reply_handle->reply_wanted == ZOO_TRUE)\n"
        body = body + "        {\n"
        body = body + "            rtn = " + compoent_id + "4I_get_reply_message_length("+self.get_function_code_upper()+", &reply_length);\n"
        body = body + "            if(OK == rtn)\n"
        body = body + "            {\n"
        body = body + "                reply_message = ("+compoent_id+"4I_REPLY_STRUCT*)MM4A_malloc(reply_length);\n"
        body = body + "                if(reply_message == NULL)\n"
        body = body + "                {\n"
        body = body + "                    rtn = " + compoent_id + "4A_SYSTEM_ERR;\n"
        body = body + "                    EH4A_show_exception(" + compoent_id + "4I_COMPONET_ID,__FILE__,__ZOO_FUNC__,__LINE__," + compoent_id + "4A_SYSTEM_ERR,0,\" MM4A_malloc failed ...ERROR\");\n"
        body = body + "                }\n"
        body = body + "            }\n\n"
        body = body + "            if(OK == rtn)\n"
        body = body + "            {\n"
        body = body + "                reply_message->reply_header.function_code  = "+self.get_function_code_upper()+";\n"
        body = body + "                reply_message->reply_header.execute_result = error_code;\n"

        for pm in self._output_parameters:
            if pm.check_variable_contain_square_brackets():
                body = body + "                memcpy(&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + ",&" + pm.get_name_with_square_brackets_header_addr() + "," + "sizeof(" + pm.get_type() + ") * " + pm.get_array_length() + ");\n"
            elif "*" in pm.get_type() and is_char_type(pm.get_type()) :
                body = body + "                memcpy(&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",&" + pm.get_name() + ",sizeof(" + pm.get_type().strip("const").strip().strip("*") + ") * " + compoent_id + "4I_BUFFER_LENGTH" + ");\n"
            else:
                body = body + "                memcpy(&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",&" + pm.get_name() + ",sizeof(" + pm.get_type().strip("*").strip(" ") + "));\n"

        for pm in self._inoutput_parameters:
            if pm.check_variable_contain_square_brackets():
                body = body + "                memcpy(&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name_with_square_brackets_header_addr() + ",&" + pm.get_name_with_square_brackets_header_addr() + "," + "sizeof(" + pm.get_type() + ") * " + pm.get_array_length() + ");\n"
            elif "*" in pm.get_type() and is_char_type(pm.get_type()):
                body = body + "                memcpy(&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",&" + pm.get_name() + ",sizeof(" + pm.get_type().strip("const").strip().strip("*") + ") * " + compoent_id + "4I_BUFFER_LENGTH" + ");\n"
            else:
                body = body + "                memcpy(&reply_message->reply_body." + self.get_reply_struct_var() + "." + pm.get_name() + ",&" + pm.get_name() + ",sizeof(" + pm.get_type().strip("*").strip(" ") + "));\n"

        body = body + "                rtn = " + compoent_id + "4I_send_reply_message(reply_handle->reply_addr,reply_handle->msg_id,reply_message);\n"
        body = body + "                if(OK != rtn)\n"
        body = body + "                {\n"
        body = body + "                    rtn = " + compoent_id + "4A_SYSTEM_ERR;\n"
        body = body + "                    EH4A_show_exception(" + compoent_id + "4I_COMPONET_ID,__FILE__,__ZOO_FUNC__,__LINE__," + compoent_id + "4A_SYSTEM_ERR,0,\" send_reply message failed ...ERROR\");\n"
        body = body + "                }\n"
        body = body + "            }\n"
        body = body + "        }\n"
        body = body + "    }\n\n"
        body = body + "    if(reply_handle != NULL)\n"
        body = body + "    {\n"
        body = body + "        MM4A_free(reply_handle);\n" \
                      "        reply_handle = NULL;\n"
        body = body + "    }\n\n"
        body = body + "    if(reply_message != NULL)\n"
        body = body + "    {\n"
        body = body + "        MM4A_free(reply_message);\n" \
                      "        reply_message = NULL;\n"
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
        print("function code:" + code)
        return code

    def generate_struct_string(self, type='', members=[PARAMETERS_CLASS()], compoent_id=''):
        tr = "/**\n*@brief " + type + "\n**/\n" + "typedef struct \n{\n"
        n_8_p = []
        n_4_p = []
        size_4_count = 0
        for n in members:
            if type_to_size(n.get_type(), n.get_name()) == 4:
                n_4_p.append(n)
                size_4_count = size_4_count + 1
            else :
                n_8_p.append(n)

        for s in n_4_p:
            #print(s.get_type() + "-" + s.get_name() + "--4")
            if "ZOO_CHAR *" in s.get_type() or "ZOO_CHAR*" in s.get_type() or "ZOO_CHAR  *" in s.get_type() or "char *" in s.get_type() or "char*" in s.get_type() or "char  *" in s.get_type():
                tr = tr + "    " + s.get_type().replace("const","").strip("*").lstrip() + " " + s.get_name().strip("*") + "[" + compoent_id + "4I_BUFFER_LENGTH];\n"
            else:
                tr = tr + "    " + s.get_type().replace("const","").strip("*") + " " + s.get_name().strip("*") + ";\n"
                #print(tr)

        if size_4_count % 2 == 1:
            tr = tr + "    ZOO_CHAR c_filler[4];\n"

        fill_8_exist = 0
        for s in n_8_p:
            #print(s.get_type() + "-" + s.get_name() + "--8")
            if "ZOO_CHAR *" in s.get_type() or "ZOO_CHAR*" in s.get_type() or "ZOO_CHAR  *" in s.get_type() or "char *" in s.get_type() or "char*" in s.get_type() or "char  *" in s.get_type():
                tr = tr + "    " + s.get_type().replace("const","").strip("*").lstrip() + " " + s.get_name().strip("*") + "[" + compoent_id + "4I_BUFFER_LENGTH];\n"
            else:
                tr = tr + "    " + s.get_type().replace("const","").strip("*") + " " + s.get_name().strip("*") + ";\n"
                #print(tr)
            if "filler[8]" in s.get_name():
                fill_8_exist = 1

        if fill_8_exist == 0:
            tr = tr + "    ZOO_CHAR g_filler[8];\n"

        tr = tr + "}" + type + ";\n\n"
        return tr

    def generate_subscribe_struct_string(self, type=''):
        st = "/**\n*@brief " + type + "\n**/\n" + "typedef struct \n{\n"
        #print("in size = " + str(self._name))
        for t in self._input_parameters:
            st = st + "    " + t.get_type() + " *callback_function;\n"
            st = st + "    void * parameter;\n"
        st = st + "}" + type + ";\n\n"
        return st

    def get_request_struct_typ(self, compoent_id=''):
        result = self.get_function_code_upper() + "_REQ_STRUCT"
        new = compoent_id + "4I_"
        old = compoent_id + "4A_"
        # print(old+" " + new)
        # print(result)
        if "4T_" in result:
            old = compoent_id + "4T_"
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

        #print("request_struct_var: " + result)
        return result

    def get_reply_struct_typ(self, compoent_id=''):
        result = self.get_function_code_upper() + "_REP_STRUCT"
        new = compoent_id + "4I_"
        old = compoent_id + "4A_"
        if "4T_" in result:
            old = compoent_id + "4T_"
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

    def get_callback_struct_typ(self, compoent_id=''):
        result = self.get_function_code_upper() + "_CALLBACK_STRUCT"
        new = compoent_id + "4I_"
        old = compoent_id + "4A_"
        if "4T_" in result:
            old = compoent_id + "4T_"
        return result.replace(old, new)

    def get_request_struct_msg(self, compoent_id=''):
        tp = self.get_function_code_upper() + "_REQ_STRUCT"
        old = '4A_'
        if "4T_" in tp:
            old = "4T_"
        r = tp.replace(old, "4I_")
        result = self.generate_struct_string(r, self.get_input_parameters_list(), compoent_id)
        return result

    def get_reply_struct_msg(self, compoent_id=''):
        tp = self.get_function_code_upper() + "_REP_STRUCT"
        result = ''
        mem = [PARAMETERS_CLASS("OUT", "ZOO_CHAR", "g_filler[8]")]
        if len(self.get_output_parameters_list()) > 0:
            if self._interface_type == "Sync":
                mem = self._output_parameters
        if len(self.get_inoutput_parameters_list()) > 0:
            mem = self._inoutput_parameters
        old = '4A_'
        if "4T_" in tp:
            old = "4T_"
        r = tp.replace(old, "4I_")
        result = self.generate_struct_string(r, mem, compoent_id)
        return result

    def get_callback_struct_msg(self, compoent_id=''):
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
        type = self._name.split("_")
        marking_code = "_"+type[-1]

        print("marking code : " + marking_code)
        if '_req' == marking_code:
            self._interface_type = 'req'
        elif '_wait' == marking_code:
            self._interface_type = 'wait'
        elif '_unsubscribe' == marking_code:
            self._interface_type = 'unsubscribe'
        elif '_subscribe' == marking_code:
            self._interface_type = 'subscribe'
        print("function name : " + self._name)
        return self._name

    def get_input_parameters_list(self):
        if not self._in_flag:
            self._in_flag = 1
            param_patten = re.compile(r"^\s*"
                                      "(ZOO_EXPORT)?"
                                      "\s+"
                                      "(ZOO_INT32|void|ZOO_BOOL|int)\s+"
                                      "(\w+)"
                                      "\s*"
                                      "\(([^)]*)\)\s*;", re.UNICODE | re.VERBOSE | re.MULTILINE | re.DOTALL)
            type_patten = re.compile(r"^\s*(\w+)\s+(\w*)\s+(\w*]+)")

            name = param_patten.findall(self._function)
            #print(name)
            param = name[0][-1]
            result = re.sub('[\r\n\t]', '', param).replace(",...", "").split(',')
            #print(result)
            tmp = []
            for p in result:
                #print(p)
                m = p.strip()
                if "*" in m:
                    m = m.replace("*", "")
                    m = " ".join(m.split())
                    #print(m)
                    t = m.split(" ")
                    if t[0] == 'IN':
                        #print("function: " + self._name)
                        #print("parameter direction: " + t[0])
                        #print("len: " + str(len(t)))
                        if len(t) == 3:
                            #print("parameter type: " + t[1] + "*")
                            #print("parameter name: " + t[2])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + "*", t[2].strip()))
                        if len(t) == 4:
                            #print("parameter type: " + t[1] + " " + t[2] + "*")
                            #print("parameter name: " + t[3])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + " " + t[2] + "*", t[3].strip()))
                        if len(t) == 5:
                            #print("parameter type: " + t[1] + " " + t[2] + " " + t[3] + "*")
                            #print("parameter name: " + t[4].strip("*"))
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + " " + t[2] + " " + t[3] + "*", t[4].strip()))
                else:
                    m = " ".join(m.split())
                    t = m.split(" ")
                    if t[0] == 'IN':
                        #print("function: " + self._name)
                        #print("parameter direction: " + t[0])
                        if len(t) == 3:
                            #print("parameter      type: " + t[1])
                            #print("parameter      name: " + t[2])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1], t[2].strip()))
                        if len(t) == 4:
                            #print("parameter      type: " + t[1] + " " + t[2].strip())
                            #print("parameter      name: " + t[3])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + " " + t[2], t[3].strip()))
                        if len(t) == 5:
                            #print("parameter      type: " + t[1] + " " + t[2] + " " + t[3].strip())
                            #print("parameter      name: " + t[4])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + " " + t[2] + " " + t[3], t[4].strip()))

            self._input_parameters = tmp
        return self._input_parameters

    def get_output_parameters_list(self):
        if not self._out_flag:
            self._out_flag = 1

            param_patten = re.compile(r"^\s*"
                                      "(ZOO_EXPORT)?"
                                      "\s+"
                                      "(ZOO_INT32|void|ZOO_BOOL|int)\s+"
                                      "(\w+)"
                                      "\s*"
                                      "\(([^)]*)\)\s*;", re.UNICODE | re.VERBOSE | re.MULTILINE | re.DOTALL)
            type_patten = re.compile(r"^\s*(\w+)\s+(\w*)\s+(\w*]+)")
            name = param_patten.findall(self._function)
            #print(name)
            param = name[0][-1]
            result = re.sub('[\r\n\t]', '', param).replace(",...", "").split(',')
            #print(result)
            tmp = []
            for p in result:
                # print(p)
                m = p.strip()
                if "*" in m:
                    m = m.replace("*", "")
                    m = " ".join(m.split())
                    t = m.split(" ")
                    if t[0] == 'OUT':
                        #print("function: " + self._name)
                        #print("parameter direction: " + t[0])
                        if len(t) == 3:
                            #print("parameter type: " + t[1] + "*")
                            #print("parameter name: " + t[2])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1].strip() + "*", t[2].strip()))
                        if len(t) == 4:
                            #print("parameter type: " + t[1] + " " + t[2] + "*")
                            #print("parameter name: " + t[3])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1].strip() + " " + t[2].strip() + "*", t[3].strip()))
                        if len(t) == 5:
                            #print("parameter type: " + t[1] + " " + t[2] + " " + t[3] + "*")
                            #print("parameter name: " + t[4].strip("*"))
                            tmp.append(
                                PARAMETERS_CLASS(t[0], t[1].strip() + " " + t[2].strip() + " " + t[3].strip() + "*",
                                                 t[4].strip()))
                else:
                    m = " ".join(m.split())
                    t = m.split(" ")
                    if t[0] == 'OUT':
                        #print("function: " + self._name)
                        #print("parameter direction: " + t[0])
                        if len(t) == 3:
                            #print("parameter      type: " + t[1])
                            #print("parameter      name: " + t[2])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1].strip(), t[2].strip()))
                        if len(t) == 4:
                            #print("parameter      type: " + t[1].strip() + " " + t[2])
                            #print("parameter      name: " + t[3])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1].strip() + " " + t[2], t[3].strip()))
                        if len(t) == 5:
                            #print("parameter      type: " + t[1] + " " + t[2] + " " + t[3])
                            #print("parameter      name: " + t[4])
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
                                      "(ZOO_INT32|void|ZOO_BOOL|int)\s+"
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
                    m = " ".join(m.split())
                    t = m.split(" ")
                    if t[0] == 'INOUT':
                        #print("function: " + self._name)
                        #print("parameter direction: " + t[0])
                        if len(t) == 3:
                            #print("parameter type: " + t[1] + "*")
                            #print("parameter name: " + t[2])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + "*", t[2]))
                        if len(t) == 4:
                            #print("parameter type: " + t[1] + " " + t[2] + "*")
                            #print("parameter name: " + t[3])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + " " + t[2] + "*", t[3]))
                        if len(t) == 5:
                            #print("parameter type: " + t[1] + " " + t[2] + " " + t[3] + "*")
                            #print("parameter name: " + t[4].strip("*"))
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + " " + t[2] + " " + t[3] + "*", t[4]))
                else:
                    m = " ".join(m.split())
                    t = m.split(" ")
                    if t[0] == 'INOUT':
                        #print("function: " + self._name)
                        #print("parameter direction: " + t[0])
                        if len(t) == 3:
                            #print("parameter      type: " + t[1])
                            #print("parameter      name: " + t[2])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1], t[2]))
                        if len(t) == 4:
                            #print("parameter      type: " + t[1] + " " + t[2])
                            #print("parameter      name: " + t[3])
                            tmp.append(PARAMETERS_CLASS(t[0], t[1] + t[2], t[3]))
                        if len(t) == 5:
                            #print("parameter      type: " + t[1] + " " + t[2] + " " + t[3])
                            #print("parameter      name: " + t[4])
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
        self._input_parameters = []
        self._output_parameters = []
        self._inoutput_parameters = []
        self._interface_type = 'subscribe'
        self._return_type = ''
        self._name = ''
        self._code_index = code_index
        self._parts = parts
        self._struct_type = ''
        self._callback_f = ''
        if function != '':
            self.initialize()

    def get_function_name(self):
        return  self._function

    def get_function_name_reply_msg(self):
        name_patten = re.compile(r"^\s*(\w+)\s+(\w+)\s*(\w+)\(", re.UNICODE | re.VERBOSE | re.MULTILINE | re.DOTALL)
        name = name_patten.findall(self._function)
        if len(name) == 0:
            return self._function
        self._return_type = name[0][1]
        self._name = name[0][2]
        return self._name

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

    def get_callback_struct_typ(self, compoent_id=''):
        result = self.get_function_code_upper() + "_CALLBACK_STRUCT"
        new = compoent_id + "4I_"
        old = compoent_id + "4A_"
        if "4T_" in result:
            old = compoent_id + "4T_"
        return result.replace(old, new)

    def get_function_code_upper(self):
        return self._name.upper() + "_CODE"

    def get_name(self):
        return self._name

    def get_function_difinition(self, funtion_name='', compoent_id='XX'):
        d = funtion_name.replace(compoent_id, compoent_id + "MA_raise_")
        f = "ZOO_EXPORT void " + d + "("
        for s in self._input_parameters:
            f = f + "IN " + s.get_type() + " " + s.get_name() + ","

        f = f + ");"
        return f.replace(",);", ");")

    def get_function_name_extend(self, funtion_name='', compoent_id='XX'):
        d = funtion_name.replace(compoent_id, compoent_id + "MA_raise_")
        f = "void " + d + "("
        for s in self._input_parameters:
            f = f + "IN " + s.get_type() + " " + s.get_name() + ","

        f = f + ")"
        return f.replace(",)", ")")

    def get_sub_callback_name(self,name=''):
        return name.replace("subscribe","callback")

    def generate_sub_callback_code(self,function=FUNCTION_CLASS(),compoent_id='XX'):
        code = "static void " + self.get_sub_callback_name(function.get_function_name()) + "(void *context_p, MQ4A_CALLBACK_STRUCT *local_proc, void *msg)\n"
        callback_t = self._name
        code = code + "{\n" \
                      "    ZOO_INT32 result = OK;\n" \
                      "    ZOO_INT32 error_code = OK;\n" \
                      "    "+compoent_id+"4I_REPLY_STRUCT *reply_msg = NULL;\n" \
                      "    "+function.get_callback_struct_typ(compoent_id)+" * callback_struct = NULL;\n"\
                      "    ZOO_INT32 rep_length = 0;\n"
        for p in self._input_parameters:
            print(self._name)
            print(p.get_type())
            if p.get_type() in "ZOO_INT32":
                code = code + "    "+ p.get_type() + " "+ p.get_name() + " = 0;\n"
            elif p.get_type() in "ZOO_UINT32":
                code = code + "    " + p.get_type() + " " + p.get_name() + " = 0;\n"
            elif p.get_type() in "ZOO_INT16":
                code = code + "    "+ p.get_type() + " "+ p.get_name() + " = 0;\n"
            elif p.get_type() in "ZOO_UINT16":
                code = code + "    " + p.get_type() + " " + p.get_name() + " = 0;\n"
            elif p.get_type() in "ZOO_CHAR":
                code = code + "    " + p.get_type() + " " + p.get_name() + " = 0;\n"
            elif "int" in p.get_type() or "char" in p.get_type():
                code = code + "    " + p.get_type() + " " + p.get_name() + " = 0;\n"
            elif "unsigned int" in p.get_type():
                code = code + "    " + p.get_type() + " " + p.get_name() + " = 0;\n"
            elif "STRUCT" in p.get_type() or "struct" in  p.get_type():
                code = code + "    " + p.get_type() + " " + p.get_name() + ";\n"
                code = code + "    " + "memset(&" +p.get_name() +",0,sizeof("+ p.get_type() + "));\n"
            else:
                code = code + "    " + p.get_type() + " " + p.get_name() + ";\n"
            break

        code = code + "    if(msg == NULL)\n"\
                        "    {\n"\
                        "        result = " + compoent_id + "4A_PARAMETER_ERR;\n"\
                        "        EH4A_show_exception("+ compoent_id + "4I_COMPONET_ID, __FILE__, __ZOO_FUNC__, __LINE__,result,0,\"msg is NULL.\");\n" \
                        "    }\n\n"\
                        "    if(OK == result)\n"\
                        "    {\n"\
                        "        result = " + compoent_id + "4I_get_reply_message_length("+function.get_function_code_upper()+", &rep_length);\n"\
                        "        if(OK != result)\n"\
                        "        {\n"\
                        "            result = " + compoent_id + "4A_PARAMETER_ERR;\n"\
                        "            EH4A_show_exception("+ compoent_id + "4I_COMPONET_ID, __FILE__, __ZOO_FUNC__, __LINE__,result,0,\"get_reply_messge_length failed.\");\n" \
                        "        }\n" \
                        "    }\n\n"\
                        "    if(OK == result)\n"\
                        "    {\n"\
                        "        reply_msg = ("+compoent_id+"4I_REPLY_STRUCT * )MM4A_malloc(rep_length);\n"\
                        "        if(NULL == reply_msg)\n"\
                        "        {\n"\
                        "            result = " + compoent_id + "4A_PARAMETER_ERR;\n"\
                        "            EH4A_show_exception("+ compoent_id + "4I_COMPONET_ID, __FILE__, __ZOO_FUNC__, __LINE__,result,0,\"MM4A_malloc failed.\");\n" \
                        "        }\n" \
                        "    }\n\n"\
                        "    if(OK == result)\n"\
                        "    {\n"\
                        "        memcpy(reply_msg, msg, rep_length);\n" \
                        "        if ("+function.get_function_code_upper()+" != reply_msg->reply_header.function_code)\n"\
                        "        {\n"\
                        "            result = " + compoent_id + "4A_PARAMETER_ERR;\n"\
                        "            EH4A_show_exception("+ compoent_id + "4I_COMPONET_ID, __FILE__, __ZOO_FUNC__, __LINE__,result,0,\"function code incorrect.\");\n" \
                        "        }\n" \
                        "        error_code = reply_msg->reply_header.execute_result;\n"
        for p in self._input_parameters:
            code = code +"        memcpy((void*)&"+p.get_name()+", &reply_msg->reply_body."+self.get_struct_var()+"."+p.get_name()+", sizeof("+p.get_type()+"));\n" \
                         "        callback_struct = (" + function.get_callback_struct_typ(compoent_id) + "*) local_proc;\n" \
                         "        ((" + callback_t + ")callback_struct->callback_function)("+p.get_name()+",error_code,context_p);\n "
            break

        code = code +   "   }\n\n"\
                        "    if(reply_msg != NULL)\n"\
                        "    {\n"\
                        "        MM4A_free(reply_msg);\n"\
                        "    }\n"\
                        "}"
        return code



    def generate_callback(self, function=FUNCTION_CLASS(), compoent_id='XX'):
        f = ''
        print(function.get_function_name())
        f = f + self.generate_sub_callback_code(function,compoent_id) + "\n\n"
        f = f + function.get_func_declaration()+"\n"
        f = f + "{\n"
        f = f + "    ZOO_INT32 result = OK;\n"
        f = f + "    ZOO_INT32 event_id = 0;\n"
        cb = "callback"
        f = f + "    MQ4A_CALLBACK_STRUCT* callback = NULL;\n"
        f = f + "    if (NULL == callback_function)\n" \
                "    {\n" \
                "        result = " + compoent_id + "4A_PARAMETER_ERR;\n" \
                "        EH4A_show_exception("+ compoent_id + "4I_COMPONET_ID, __FILE__, __ZOO_FUNC__, __LINE__,result,0,\"callback_function is NULL.\");\n" \
                "        return result;\n" \
                "    }\n\n" \
                "    /*function entry*/\n" \
                "    TR4A_trace("+ compoent_id + "4I_COMPONET_ID, __ZOO_FUNC__, \"> function entry ... \");\n"

        f = f + "    /*fill callback strcut*/\n" \
                "    callback = (MQ4A_CALLBACK_STRUCT*)MM4A_malloc(sizeof(" + function.get_callback_struct_typ(compoent_id) + "));\n"

        f = f + "    if (NULL == callback)\n" \
                "    {\n" \
                "        result = " + compoent_id + "4A_PARAMETER_ERR;\n" \
                "        EH4A_show_exception("+ compoent_id + "4I_COMPONET_ID, __FILE__, __ZOO_FUNC__, __LINE__,result,0,\"callback is NULL.\");\n" \
                "    }\n\n"

        f = f + "    if (OK == result)\n" \
                "    {\n" \
                "        callback->callback_function = callback_function;\n" \
                "        event_id = " + function.get_function_code_upper() + ";\n" \
                "        result = "+compoent_id+"4I_send_subscribe(" + compoent_id + "4A_SERVER,\n" \
                "                                      " + self.get_sub_callback_name(function.get_function_name()) + ",\n" \
                "                                      callback,\n" \
                "                                      event_id,\n" \
                "                                      (ZOO_HANDLE*)handle,\n" \
                "                                      context);\n" \
                "        if (OK != result)\n" \
                "        {\n" \
                "           result = " + compoent_id + "4A_PARAMETER_ERR;\n" \
                "           EH4A_show_exception("+ compoent_id + "4I_COMPONET_ID, __FILE__, __ZOO_FUNC__, __LINE__,result,0,\"send_subscribe failed.\");\n" \
                "           MM4A_free(callback);\n" \
                "        }\n" \
                "    }\n\n" \
                "    TR4A_trace("+ compoent_id + "4I_COMPONET_ID, __ZOO_FUNC__,\"< function exit ...\");\n" \
                "    return result;\n" \
                "}\n\n"
        f= f + self.generate_unsubscribe(function,compoent_id)
        return f

    def generate_unsubscribe(self,function=FUNCTION_CLASS(), compoent_id='XX'):
        body = "ZOO_INT32 " + function.get_function_name().replace("_subscribe","_unsubscribe") + "(IN ZOO_UINT32 handle)\n{\n"
        body = body + "    ZOO_INT32 result = OK;\n"
        body = body + "    ZOO_INT32 event_id = " + function.get_function_code_upper() + ";\n"
        body = body + "    if(OK == result)\n"
        body = body + "    {\n"
        body = body + "        result = "+compoent_id+"4I_send_unsubscribe("+compoent_id+"4A_SERVER,event_id,handle);\n" \
                      "    }\n"
        body = body + "    return result;\n}\n\n"
        return body

    def get_function_body(self, function=FUNCTION_CLASS(), compoent_id='XX'):
        body = "{\n"
        body = body + "    ZOO_INT32 rtn = OK;\n" \
                      "    " + compoent_id + "4I_REPLY_STRUCT * reply_message = NULL;\n" \
                                              "    reply_message = (" + compoent_id + "4I_REPLY_STRUCT * ) " + "MM4A_malloc(sizeof(" + compoent_id + "4I_REPLY_STRUCT));\n"
        body = body + "    if(NULL == reply_message)\n" \
                      "    {\n" \
                      "        rtn = " + compoent_id + "4A_PARAMETER_ERR;\n" \
                    "    }\n" \
                    "    \n" \
                    "    if(OK == rtn)\n" \
                    "    {\n" \
                    "        reply_message->reply_header.function_code = " + function.get_function_code_upper() + ";\n" \
                                                                                                                  "        reply_message->reply_header.execute_result = error_code;\n"

        for p in self._input_parameters:
            if "STRUCT" in p.get_type() or "struct" in p.get_type():
                body = body + "        memcpy(&reply_message->reply_body." + self.get_struct_var() + "." + p.get_name() + ",&" + p.get_name() + ",sizeof(" + p.get_type() + "));\n"
        body = body + "    }\n\n" \
                      "    if(OK == rtn)\n" \
                      "    {\n" \
                      "        rtn = " + compoent_id + "4I_publish_event(" + compoent_id + "4A_SERVER,\n" \
                      "                                            " + function.get_function_code_upper() + ",\n" \
                      "                                            reply_message);\n"
        body = body + "    }\n\n" \
                      "    if(OK != rtn)\n"\
                      "    {\n"\
                      "        EH4A_show_exception("+ compoent_id + "4I_COMPONET_ID, __FILE__, __ZOO_FUNC__, __LINE__,rtn,0,\"publish_event failed.\");\n" \
                      "    }\n\n" \
                      "    if(reply_message != NULL)\n" \
                      "    {\n"\
                      "        MM4A_free(reply_message);\n" \
                      "    }\n\n" \
                      "    return;\n" \
                      "}"
        return body

    def initialize(self):
        print(self._parts)
        self._return_type = self._parts[0]
        self._name = self._parts[1]
        tmp = self._parts[2]
        tmp = tmp.replace('\t','')
        tmp = tmp.replace('\n', '')
        tmp = tmp.split(',')
        print(tmp)
        for p in tmp:
            result = p.lstrip().rstrip()
            t = result.split(" ")
            if 'IN' in t[0]:
                #print("parameter direction: " + t[0])
                #print("parameter      type: " + t[1])
                #print("parameter      name: " + t[2])
                self._input_parameters.append(PARAMETERS_CLASS(t[0], t[1], t[2]))
            if t[0] == 'OUT':
                #print("parameter direction: " + t[0])
                #print("parameter      type: " + t[1])
                #print("parameter      name: " + t[2])
                self._output_parameters.append(PARAMETERS_CLASS(t[0], t[1], t[2]))
            if t[0] == 'INOUT':
                #print("parameter direction: " + t[0])
                #print("parameter      type: " + t[1])
                #print("parameter      name: " + t[2])
                self._inoutput_parameters.append(PARAMETERS_CLASS(t[0], t[1], t[2]))

    def generate_struct_string(self, type='', members=[PARAMETERS_CLASS()]):
        tr = "/**\n*@brief " + type + "\n**/\n" + "typedef struct \n{\n"
        total_size = 0
        for n in members:
            total_size = total_size + type_to_size(n.get_type(), n.get_name())
        #print("total size: " + str(total_size))
        for s in members:
            '''if type_to_size(s.get_type(),s.get_name()) % 8 > 0 :
                fill_size = (type_to_size(s.get_type(),s.get_name()) % 8)
                tr = tr + "    ZOO_CHAR filler[" + str(fill_size) + "];\n"'''
            if "STRUCT" in s.get_type() or "struct" in s.get_type():
                tr = tr + "    " + s.get_type() + " " + s.get_name().strip("*") + ";\n"
                tr = tr + "    ZOO_CHAR g_filler[8];\n"
                break
            else :
                tr = tr + "    " + s.get_type() + " " + s.get_name() + ";\n"
                if type_to_size(n.get_type(), n.get_name()) % 8 > 0 :
                    tr = tr + "    ZOO_CHAR c_filler[4];\n"
                else:
                    tr = tr + "    ZOO_CHAR g_filler[8];\n"
                break

        if len(members) == 0:
            tr = tr + "    ZOO_CHAR g_filler[8];\n"
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
        mem = [PARAMETERS_CLASS("OUT", "ZOO_CHAR", "g_filler[8]")]
        if len(self._input_parameters) > 0:
            mem = self._input_parameters
            #print(len(self._input_parameters))
        old = '4A_'
        if "4T_" in tp:
            old = "4T_"
        r = tp.replace(old, "4I_")
        result = self.generate_struct_string(r, mem)
        #print('------------------------------------------------------------------------------')
        #print(result)
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
            #print("callback: *************************************BEGIN")
            #print(entity)
            #print("callback: *************************************END")
            fc = 0
            for result in entity:
                fp = "ZOO_EXPORT " + result[0] + " " + result[1] + "(" + result[2] + ")"
                #print(result[0])
                #print(result[1])
                #print(result[2])
                #print(fp)
                tmp.append(CALLBACK_FUNCTION_CLASS(fp, fc, result))
                fc = fc + 1
        self._callback_list = tmp

    def get_callback_list(self):
        return self._callback_list

    def get_function_list(self,fc):
        function_entity = re.compile(r"^\s*"
                                     "ZOO_EXPORT?"
                                     "\s+"
                                     "\w+\s+"
                                     "\w+"
                                     "\s*"
                                     "\([^)]*\)\s*;", re.UNICODE | re.VERBOSE | re.MULTILINE | re.DOTALL)
        tmp = []
        fc = 1
        with open(self._file_name, 'r+', encoding='utf-8') as f:
            text = f.read()
            entity = function_entity.findall(text)
            print(entity)
            for result in entity:
                tmp.append(FUNCTION_CLASS(result, fc))
                print(result)
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
        #print(self._file)
        with open(self._file, 'r+', encoding='utf-8') as f:
            text = f.read()
            entity = enum_patten.findall(text)
            #print(entity)
            for result in entity:
                tmp = []
                double_slash_patten = re.compile(r'//.*')
                slash_star_patten = re.compile(r'/\*.*?\*/')
                name_patten = re.compile(r"(\w\w4\w\_\w*\_ENUM)")
                mem_patten = re.compile(r"\s*(\w\w4\w\_\w*)+")
                s = re.sub(double_slash_patten, ' ', result)
                x = re.sub(slash_star_patten, '', s)
                m = re.sub('[\r\n\t]', '', x)
                #print(m)
                name = name_patten.findall(m)
                #print(name)
                r = mem_patten.findall(m)
                #print(r)
                for mm in r:
                    tmp.append(mm)
                e.append(ENUM_CLASSS(name, tmp))
        return e

    def get_struct_list(self):
        enum_patten = re.compile(
            r"typedef\s+struct\s*{[^}]*}[^;]+")  # re.compile(r"typedef\s+struct\s*{[^{}]*}\s*([a-zA-Z0-9_]+)\s*;")
        e = []
        #print(self._file)
        with open(self._file, 'r+', encoding='utf-8') as f:
            text = f.read()
            e = enum_patten.findall(text)
            #print(e)
        return e

    def get_mirco_list(self):
        return


# *
# create directory for XX component
# *
class XX_DIR_GENERATOR(object):
    def __init__(self, compoent_id='XX'):
        self._current_path = os.getcwd()
        self._inc_dir = self._current_path + '/' + compoent_id + '/' + 'inc'
        self._com_dir = self._current_path + '/' + compoent_id + '/' + 'com'
        self._lib_dir = self._current_path + '/' + compoent_id + '/' + 'lib'
        self._bin_dir = self._current_path + '/' + compoent_id + '/' + 'bin'
        self._bin_tst = self._current_path + '/' + compoent_id + '/' + 'test'
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
    def get_test_path(self):
        return self._bin_tst


# *
# create XX4I_type.h
# *
class XX4I_type_h(object):
    def __init__(self, compoent_id='', function_list=[], callback_lsit=[], path=''):
        self._compoent_id = compoent_id
        self._function_list = function_list
        self._file_name = path + '/' + compoent_id + '4I_type.h'
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', compoent_id + '4I_type.h')
        self._callback_list = callback_lsit

    def generate_header_comment(self):
        with open(self._file_name, 'w') as f:
            for header in self._header_comment.get_list():
                f.write(header)
                f.write('\n')
        return

    def generate_include(self):
        with open(self._file_name, 'a+') as f:
            f.write('#ifndef ' + self._compoent_id + '4I_TYPE_H')
            f.write('\n')
            f.write('#define ' + self._compoent_id + '4I_TYPE_H')
            f.write('\n')
            f.write('#include <MQ4A_type.h>')
            f.write('\n')
            f.write('#include "' + self._compoent_id + '4A_type.h"\n')
            f.write('#include "' + self._compoent_id + '4A_if.h"\n')
            f.write('\n')
            f.write('\n')
        return

    def get_server_address(self):
        return self._compoent_id + '4A_SERVER'

    def generate_mirco_defintion(self):
        with open(self._file_name, 'a+') as f:
            f.write(COMMENT_CLASS().get_comment('Macro Definitions'))
            f.write('#define ' + self._compoent_id + '4I_COMPONET_ID "' + self._compoent_id + "\"")
            f.write('\n')
            f.write('#define ' + self._compoent_id + '4A_SERVER     "' + self._compoent_id + '4A_SERVER"')
            f.write('\n')
            f.write('#define ' + self._compoent_id + '4I_BUFFER_LENGTH    256')
            f.write('\n')
            f.write('#define ' + self._compoent_id + '4I_RETRY_INTERVAL   3')
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
                    "    MQ4A_SERV_ADDR reply_addr;\n"
                    "    ZOO_UINT32 msg_id;\n"
                    "    ZOO_BOOL reply_wanted;\n"
                    "    ZOO_UINT32 func_id;\n"
                    "}" + self._compoent_id + "4I_REPLY_HANDLER_STRUCT;\n\n")

            f.write("typedef  " + self._compoent_id + "4I_REPLY_HANDLER_STRUCT * " + self._compoent_id + "4I_REPLY_HANDLE;\n")
            f.write("\n")
            f.write("/*Request message header struct*/\n"
                    "typedef struct\n"
                    "{\n"
                    "    ZOO_UINT32 function_code;\n"
                    "    ZOO_BOOL need_reply;\n"
                    "}" + self._compoent_id + "4I_REQUEST_HEADER_STRUCT;")
            f.write("\n\n")
            f.write("/*Reply message header struct*/\n"
                    "typedef struct\n"
                    "{\n"
                    "    ZOO_UINT32 function_code;\n"
                    "    ZOO_BOOL execute_result;\n"
                    "}" + self._compoent_id + "4I_REPLY_HEADER_STRUCT;")
            f.write("\n\n")
        return

    def generate_request_message(self):
        with open(self._file_name, 'a+') as f:
            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write(func.get_request_struct_msg(self._compoent_id))
        return

    def generate_reply_message(self):

        with open(self._file_name, 'a+') as f:
            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write(func.get_reply_struct_msg(self._compoent_id))

            #callback只放了回调函数的类型，订阅函数是放在普通函数的列表里，需要通过回调函数的名字查找普通函数的参数列表，来活得订阅函数名
            for cb in self._callback_list:
                for func in self._function_list:
                    for p in func.get_input_parameters_list():
                       if p.get_type() == cb.get_function_name_reply_msg():
                            f.write(cb.get_reply_msg(func.get_function_name()))
        return

    def generate_subsribe_message(self):
        with open(self._file_name, 'a+') as f:
            for func in self._function_list:
                if func.check_is_subscribe():
                    f.write(func.get_callback_struct_msg())
        return

    def generate_request_messages(self):
        with open(self._file_name, 'a+') as f:
            f.write("typedef struct\n")
            f.write("{\n")
            f.write("    " + self._compoent_id + "4I_REQUEST_HEADER_STRUCT request_header;\n")
            f.write("    union\n")
            f.write("    {\n")
            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write("        " + func.get_request_struct_typ(
                        self._compoent_id) + " " + func.get_request_struct_var() + ";\n")
            f.write("     }request_body;\n")
            f.write("}" + self._compoent_id + "4I_" + "REQUEST_STRUCT;\n")
            f.write("\n\n")
        return

    def generate_reply_messages(self):
        with open(self._file_name, 'a+') as f:
            f.write("typedef struct\n")
            f.write("{\n")
            f.write("    " + self._compoent_id + "4I_REPLY_HEADER_STRUCT reply_header;\n")
            f.write("    union\n")
            f.write("    {\n")
            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write("        " + func.get_reply_struct_typ(
                        self._compoent_id) + " " + func.get_reply_struct_var() + ";\n")
            for cb in self._callback_list:
                f.write("        " + cb.get_struct_typ() + " " + cb.get_struct_var() + ";\n")
            f.write("    }reply_body;\n")
            f.write("}" + self._compoent_id + "4I_" + "REPLY_STRUCT;\n")
            f.write("\n\n")
        return

    def end_file(self):
        with open(self._file_name, 'a+') as f:
            f.write("#endif //" + self._compoent_id + '4I_type.h' + "\n")

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
    def __init__(self, compoent_id='', function_list=[], callback_lsit=[], path=''):
        self._compoent_id = compoent_id
        self._function_list = function_list
        self._callback_list = callback_lsit
        self._path = path
        self._file_name = self._compoent_id + "4A.c"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', compoent_id + '4A.c')

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
                                             self._compoent_id + "4I_type.h",
                                             self._compoent_id + "4A_type.h",
                                             self._compoent_id + "4I_if.h",
                                             ]).get_list():
                f.write(incld)
                f.write("\n")
            i = 0
            for fc in self._function_list:
                if fc.get_interface_type() == "Sync":
                    f.write(fc.get_comment(fc.get_function_name()))
                    f.write(fc.get_function().replace("ZOO_EXPORT ", "").rstrip(";"))
                    f.write("\n")
                    f.write(fc.get_body(self._compoent_id))
                    f.write("\n")

                if fc.get_interface_type() == "req":
                    f.write(fc.get_comment(fc.get_function_name()))
                    f.write(fc.get_function().replace("ZOO_EXPORT ", "").rstrip(";"))
                    f.write("\n")
                    f.write(fc.get_body_req(self._compoent_id))
                    f.write("\n")

                if fc.get_interface_type() == "wait":
                    f.write(fc.get_comment(fc.get_function_name()))
                    f.write(fc.get_function().replace("ZOO_EXPORT ", "").rstrip(";"))
                    f.write("\n")
                    f.write(fc.get_body_wait(self._compoent_id))
                    f.write("\n")

                '''if fc.get_interface_type() == "subscribe":
                    cb = self._callback_list[i]
                    f.write(cb.generate_callback(fc, self._compoent_id))
                    i = i+1'''
            for cb_fc in self._callback_list:
                for fc in self._function_list:
                    for p in fc.get_input_parameters_list():
                        if cb_fc.get_name() in p.get_type():
                            f.write(cb_fc.generate_callback(fc, self._compoent_id))
        return

# *
# create XX4I_if.c
# *
class XX4T_c(object):
    def __init__(self, compoent_id='', function_list=[], callback_lsit=[], path=''):
        self._compoent_id = compoent_id
        self._function_list = function_list
        self._callback_list = callback_lsit
        self._path = path
        self._file_name = self._compoent_id + "4T.c"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', compoent_id + '4T.c')

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
                                             self._compoent_id + "4I_type.h",
                                             self._compoent_id + "4A_type.h",
                                             self._compoent_id + "4I_if.h",
                                             ]).get_list():
                f.write(incld)
                f.write("\n")
            i = 0
            for fc in self._function_list:
                if fc.get_interface_type() == "Sync":
                    f.write(fc.get_comment(fc.get_function_name()))
                    f.write(fc.get_function().replace("ZOO_EXPORT ", "").rstrip(";"))
                    f.write("\n")
                    f.write(fc.get_body(self._compoent_id))
                    f.write("\n")

                if fc.get_interface_type() == "req":
                    f.write(fc.get_comment(fc.get_function_name()))
                    f.write(fc.get_function().replace("ZOO_EXPORT ", "").rstrip(";"))
                    f.write("\n")
                    f.write(fc.get_body_req(self._compoent_id))
                    f.write("\n")

                if fc.get_interface_type() == "wait":
                    f.write(fc.get_comment(fc.get_function_name()))
                    f.write(fc.get_function().replace("ZOO_EXPORT ", "").rstrip(";"))
                    f.write("\n")
                    f.write(fc.get_body_wait(self._compoent_id))
                    f.write("\n")

                '''if fc.get_interface_type() == "subscribe":
                    cb = self._callback_list[i]
                    f.write(cb.generate_callback(fc, self._compoent_id))
                    i = i+1'''
            for cb_fc in self._callback_list:
                for fc in self._function_list:
                    for p in fc.get_input_parameters_list():
                        if cb_fc.get_name() in p.get_type():
                            f.write(cb_fc.generate_callback(fc, self._compoent_id))
        return

class XX4I_if_h(object):
    def __init__(self, compoent_id='', path=''):
        self._compoent_id = compoent_id
        self._path = path
        self._file_name = self._compoent_id + "4I_if.h"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', compoent_id + '4I_if.h')

    def get_request_message_length_function_difinition(self):
        fd = "/*\n" \
             "@brief Get request message length[bytes]\n" \
             "*@param function_code   function id\n" \
             "*@param *message_length  message length \n" \
             "*@precondition:\n" \
             "*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._compoent_id + "4I_get_request_message_length(IN ZOO_INT32 function_code,\n" \
                                                                 "													INOUT ZOO_INT32 *message_length );"
        return fd

    def get_reply_message_length_function_difinition(self):
        fd = "/*" \
             "\n@brief Get request message length[bytes]\n" \
             "*@param function_code    function id\n" \
             "*@param *message_length  message length \n" \
             "*@precondition:\n*@postcondition:\n" \
             "*/" \
             "\n" \
             "ZOO_EXPORT ZOO_INT32 " + self._compoent_id + "4I_get_reply_message_length(IN ZOO_INT32 function_code,\n" \
                                                            "													INOUT ZOO_INT32 *message_length );"
        return fd

    def get_send_request_and_reply_function_difinition(self):
        fd = "/*\n" \
             "*@brief Send message to server and wait response,it is a sync api\n" \
             "*@param MQ4A_SERV_ADDR   server address\n" \
             "*@param *request_message request message\n" \
             "*@param *reply_message   reply message\n" \
             "*@param timeout          timeout value for waiting reply[milliseconds] \n" \
             "*@precondition:\n" \
             "*@postcondition: \n" \
             "*/\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._compoent_id + "4I_send_request_and_reply(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "													IN " + self._compoent_id + "4I_REQUEST_STRUCT  *request_message,\n" \
                                                                 "													INOUT " + self._compoent_id + "4I_REPLY_STRUCT *reply_message,\n" \
                                                                 "													IN ZOO_INT32 timeout);"
        return fd

    def get_send_request_message_difinition(self):
        fd = "/*\n" \
             "*@brief Send message to server and wait response,it is a async api" + self._compoent_id + "4I_receive_reply_message\n" \
                                                                    "*@param MQ4A_SERV_ADDR   server address\n" \
                                                                    "*@param *request_message request message \n" \
                                                                    "*@precondition:\n*@postcondition:\n" \
                                                                    "*/\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._compoent_id + "4I_send_request_message(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "													IN " + self._compoent_id + "4I_REQUEST_STRUCT *request_message);"
        return fd

    def get_send_reply_message_difinition(self):
        fd = "/*\n" \
             "*@brief Response message to client after has a request" + self._compoent_id + "4I_send_reply_message\n" \
                                                                    "*@param MQ4A_SERV_ADDR    server address\n" \
                                                                    "*@param msg_id            message id\n" \
                                                                    "*@param *reply_message    response message \n" \
                                                                    "*@precondition:\n*@postcondition:\n" \
                                                                    "*/\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._compoent_id + "4I_send_reply_message(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "								                IN ZOO_INT32 msg_id,\n" \
                                                                 "                                                IN " + self._compoent_id + "4I_REPLY_STRUCT *reply_message);"
        return fd

    def get_receive_reply_message_difinition(self):
        fd = "/*\n" \
             "*@brief Recieve message from server\n	" \
             "*@param server         server address\n" \
             "*@param function_code  message id\n" \
             "*@param *reply_message reply message\n" \
             "*@param timeout        reply timeout value[milliseconds]\n" \
             "*@description:         async interface, use in combination with send_request_message\n" \
             "*@precondition:\n" \
             "*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._compoent_id + "4I_receive_reply_message(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "													IN ZOO_INT32 function_code,\n" \
                                                                 "													INOUT " + self._compoent_id + "4I_REPLY_STRUCT *reply_message,\n" \
                                                                 "													IN ZOO_INT32 timeout);"
        return fd

    def get_publish_event_difinition(self):
        fd = "/*\n" \
             "*@brief Publish message to subscribers\n" \
             "*@param event_id       message id\n" \
             "*@param *reply_message response message\n" \
             "*@description:          \n" \
             "*@precondition:\n*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._compoent_id + "4I_publish_event(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "													IN ZOO_INT32 event_id,\n" \
                                                                 "													INOUT " + self._compoent_id + "4I_REPLY_STRUCT *reply_message);"
        return fd

    def get_send_subscribe_difinition(self):
        fd = "/*\n" \
             "*@brief Subscribe messages\n*@param server            \n" \
             "*@param callback_function server message handler \n" \
             "*@param callback_struct   hanle context\n" \
             "*@param event_id          message\n" \
             "*@param *handle           the subscriber id\n" \
             "*@param *context          context\n " \
             "*@precondition:\n*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._compoent_id + "4I_send_subscribe(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "													IN MQ4A_EVENT_CALLBACK_FUNCTION callback_function,\n" \
                                                                 "													IN MQ4A_CALLBACK_STRUCT *callback_struct,\n" \
                                                                 "													IN ZOO_INT32 event_id,\n" \
                                                                 "													INOUT ZOO_HANDLE *handle,\n" \
                                                                 "													INOUT void *context);"
        return fd

    def get_send_unsubscribe_difinition(self):
        fd = "/*\n" \
             "*@brief Unsubsribe message\n" \
             "*@param server   address\n" \
             "*@param event_id \n" \
             "*@param handle   \n" \
             "*@precondition:  \n" \
             "*@postcondition: \n" \
             "*/\n"
        fd = fd + "ZOO_EXPORT ZOO_INT32 " + self._compoent_id + "4I_send_unsubscribe(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "													IN ZOO_INT32 event_id,\n" \
                                                                 "													IN ZOO_HANDLE handle);"
        return fd

    def generate(self):
        with open(self._path + '/' + self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            for incld in FILE_INCLUDE_CLASS(["ZOO.h", "ZOO_tc.h","stdio.h", "stdlib.h", "EH4A_if.h", "TR4A_if.h",
                                             "MQ4A_if.h",
                                             "MQ4A_type.h",
                                             "MM4A_if.h",
                                             self._compoent_id + "4I_type.h",
                                             self._compoent_id + "4A_type.h",
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
            f.write(self.get_send_reply_message_difinition())
            f.write("\n\n")
            f.write(self.get_publish_event_difinition())
            f.write("\n\n")
            f.write(self.get_send_subscribe_difinition())
            f.write("\n\n")
            f.write(self.get_send_unsubscribe_difinition())
            f.write("\n\n")
            f.write(get_endif(self._file_name))
            f.write("\n")
        return


class XX4I_c(object):
    def __init__(self, compoent_id='', function_list=[], path=''):
        self._compoent_id = compoent_id
        self._function_list = function_list
        self._path = path
        self._file_name = self._compoent_id + "4I.c"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', compoent_id + '4I.c')

    def get_request_message_length_function_difinition(self):
        fd = "/*\n" \
             "@brief Get request message length[bytes]\n" \
             "*@param function_code   function id\n" \
             "*@param *message_length  message length \n" \
             "*@precondition:\n" \
             "*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_INT32 " + self._compoent_id + "4I_get_request_message_length(IN ZOO_INT32 function_code,\n" \
                                                      "													INOUT ZOO_INT32 *message_length )\n"
        fd = fd + "{" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    /* Check input parameter */\n" \
                  "    if ( NULL == message_length )\n" \
                  "    {\n" \
                  "        result = " + self._compoent_id + "4A_PARAMETER_ERR;\n" \
                  "        EH4A_show_exception(" + self._compoent_id + "4I_COMPONET_ID, __FILE__,\n " \
                  "                            __ZOO_FUNC__, __LINE__,result,0,\"request msg length is NULL.\");\n" \
                  "    }\n" \
                  "    else\n" \
                  "    {\n" \
                  "        *message_length = 0;\n" \
                  "    }\n" \
                  "    /*Check result */\n" \
                  "    if ( OK == result )\n" \
                  "    {\n" \
                  "        switch( function_code )\n" \
                  "        {\n"
        for fn in self._function_list:
            if fn.get_interface_type() == "Sync":
                fd = fd + "        case " + fn.get_function_code_upper() + ":\n"
                fd = fd + "            *message_length = sizeof(" + self._compoent_id + "4I_REQUEST_HEADER_STRUCT)+sizeof(" + fn.get_request_struct_typ(self._compoent_id) + ");\n"
                fd = fd + "            break;\n"
        fd = fd + "        default:\n" \
                  "               result = " + self._compoent_id + "4A_PARAMETER_ERR;\n" \
                  "               EH4A_show_exception("+ self._compoent_id + "4I_COMPONET_ID, __FILE__, __ZOO_FUNC__,__LINE__,result,0,\" Error in " + self._compoent_id + "4I_get_request_message_length.\");\n" \
                  "               break;\n" \
                  "        }\n" \
                  "    }\n" \
                  "    return result;\n"
        fd = fd + "}\n"
        return fd

    def get_reply_message_length_function_difinition(self):
        fd = "/*" \
             "\n@brief Get reply message length[bytes]\n" \
             "*@param function_code    function id\n" \
             "*@param *message_length  message length \n" \
             "*@precondition:\n*@postcondition:\n" \
             "*/" \
             "\n" \
             "ZOO_INT32 " + self._compoent_id + "4I_get_reply_message_length(IN ZOO_INT32 function_code,\n" \
                                                 "													INOUT ZOO_INT32 *message_length )\n"
        fd = fd + "{" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    /*  Check input parameter */\n" \
                  "    if ( NULL == message_length )\n" \
                  "    {\n" \
                  "        result = " + self._compoent_id + "4A_PARAMETER_ERR;\n" \
                  "        EH4A_show_exception("+ self._compoent_id + "4I_COMPONET_ID, __FILE__,__ZOO_FUNC__,__LINE__,result,0,\"request msg length is NULL.\");\n" \
                  "    }\n" \
                  "    else\n" \
                  "    {\n" \
                  "        *message_length = 0;\n" \
                  "    }\n" \
                  "    /*Check result */\n" \
                  "    if ( OK == result )\n" \
                  "    {\n" \
                  "        switch( function_code )\n" \
                  "        {\n"
        for fn in self._function_list:
            if fn.get_interface_type() == "Sync":
                fd = fd + "        case " + fn.get_function_code_upper() + ":\n"
                fd = fd + "            *message_length = sizeof(" + self._compoent_id + "4I_REPLY_HEADER_STRUCT)+sizeof(" + fn.get_reply_struct_typ(
                    self._compoent_id) + ");\n"
                fd = fd + "            break;\n"
            if fn.get_interface_type() == "subscribe":
                fd = fd + "        case " + fn.get_function_code_upper() + ":\n"
                fd = fd + "            *message_length = sizeof(" + self._compoent_id + "4I_REPLY_HEADER_STRUCT)+sizeof(" + fn.get_reply_struct_typ(
                    self._compoent_id) + ");\n"
                fd = fd + "            break;\n"
        fd = fd + "        default:\n" \
                  "               result = " + self._compoent_id + "4A_PARAMETER_ERR;\n" \
                  "               EH4A_show_exception("+ self._compoent_id + "4I_COMPONET_ID, __FILE__,__ZOO_FUNC__, __LINE__,result,0,\" Error in " + self._compoent_id + "4I_get_reply_message_length.\");\n" \
                  "               break;\n" \
                  "        }\n" \
                  "    }\n" \
                  "    return result;\n"
        fd = fd + "}\n"
        return fd

    def get_send_request_and_reply_function_difinition(self):
        fd = "/*\n" \
             "*@brief Send message to server and wait reply\n" \
             "*@param MQ4A_SERV_ADDR   server address\n" \
             "*@param *request_message \n" \
             "*@param *reply_message   \n" \
             "*@param timeout          milliseconds\n" \
             "*@precondition:\n" \
             "*@postcondition: \n" \
             "*/\n"
        fd = fd + "ZOO_INT32 " + self._compoent_id + "4I_send_request_and_reply(IN const MQ4A_SERV_ADDR server,\n" \
                                                      "													IN " + self._compoent_id + "4I_REQUEST_STRUCT  *request_message,\n" \
                                                      "													INOUT " + self._compoent_id + "4I_REPLY_STRUCT *reply_message,\n" \
                                                      "													IN ZOO_INT32 timeout)\n"
        fd = fd + "{\n" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    ZOO_INT32 request_length = 0;\n" \
                  "    ZOO_INT32 reply_length = 0;\n" \
                  "    ZOO_INT32 actual_reply_length = 0;\n\n" \
                  "    if(request_message == NULL)\n" \
                  "    {\n" \
                  "        result = " + self._compoent_id + "4A_PARAMETER_ERR;\n" \
                  "    }\n\n" \
                  "    if(result == OK)\n" \
                  "    {\n" \
                  "        result = " + self._compoent_id + "4I_get_request_message_length(request_message->request_header.function_code, &request_length);\n" \
                  "    }\n\n" \
                  "    if(result == OK)\n" \
                  "    {\n" \
                  "        result = " + self._compoent_id + "4I_get_reply_message_length(reply_message->reply_header.function_code, &reply_length);\n" \
                  "    }\n\n" \
                  "    if(result == OK)\n" \
                  "    {\n" \
                  "        result = MQ4A_send_request_and_receive_reply(server,\n" \
                  "												            request_message,\n" \
                  "												            request_length,\n" \
                  "												            reply_message,\n" \
                  "												            reply_length,\n" \
                  "												            &actual_reply_length,\n	" \
                  "											                " + self._compoent_id + "4I_RETRY_INTERVAL,\n" \
                  "												            timeout);\n    }\n\n" \
                  " 	return result;\n" \
                  "}"
        return fd

    def get_send_request_message_difinition(self):
        fd = "/*\n" \
             "*@brief 4I_receive_reply_message\n" \
             "*@param MQ4A_SERV_ADDR   \n" \
             "*@param *request_message  \n" \
             "*@precondition:\n*@postcondition:\n" \
             "*/\n"
        fd = fd + "ZOO_INT32 " + self._compoent_id + "4I_send_request_message(IN const MQ4A_SERV_ADDR server,\n" \
                                                      "													IN " + self._compoent_id + "4I_REQUEST_STRUCT *request_message)\n"
        fd = fd + "\n{\n" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    ZOO_INT32 request_length = 0;\n" \
                  "    /*Get message length*/\n" \
                  "    if ( OK == result )\n" \
                  "    {\n" \
                  "        result = " + self._compoent_id + "4I_get_request_message_length(request_message->request_header.function_code, &request_length );\n\n" \
                  "    }\n\n" \
                  "    /*Send message to server*/\n" \
                  "    if ( OK == result )\n" \
                  "    {\n" \
                  "        result = MQ4A_send_request( server,				 /*address*/\n" \
                  "                                    request_message,					 /*message*/\n" \
                  "                                    request_length,						 /*length*/\n" \
                  "                                    " + self._compoent_id + "4I_RETRY_INTERVAL );           /*retry  times*/\n" \
                  "    }\n\n" \
                  "    return result;\n" \
                  "}"
        return fd

    def get_send_reply_message_difinition(self):
        fd = "/*\n" \
             "*@brief server send reply to client" + self._compoent_id + "4I_send_reply_message\n" \
                                                                    "*@param MQ4A_SERV_ADDR   \n" \
                                                                    "*@param *request_message  \n" \
                                                                    "*@precondition:\n*@postcondition:\n" \
                                                                    "*/\n"
        fd = fd + "ZOO_INT32 " + self._compoent_id + "4I_send_reply_message(IN const MQ4A_SERV_ADDR server,\n" \
                                                                 "								IN ZOO_INT32 msg_id,\n" \
                                                                 "                              IN " + self._compoent_id + "4I_REPLY_STRUCT *reply_message)\n"
        fd = fd + "\n{\n" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    ZOO_INT32 reply_length = 0;\n" \
                  "    /*Get message length*/\n" \
                  "    if ( OK == result )\n" \
                  "    {\n" \
                  "        result = " + self._compoent_id + "4I_get_reply_message_length( reply_message->reply_header.function_code, &reply_length );\n" \
                  "    }\n\n" \
                  "    /**/\n" \
                  "    if ( OK == result )\n" \
                  "    {\n" \
                  "        result = MQ4A_send_reply( server,				 /*address*/\n" \
                  "                                    msg_id,				 /*id */\n" \
                  "                                    reply_message,		 /*message*/\n" \
                  "                                    reply_length );       /*length*/\n" \
                  "    }\n\n" \
                  "    return result;\n" \
                  "}"
        return fd

    def get_receive_reply_message_difinition(self):
        fd = "/*\n" \
             "*@brief reply message from server\n	" \
             "*@param server         \n" \
             "*@param function_code  \n" \
             "*@param *reply_message \n" \
             "*@param timeout        \n" \
             "*@description:         4I_send_request_message\n" \
             "*@precondition:\n" \
             "*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_INT32 " + self._compoent_id + "4I_receive_reply_message(IN const MQ4A_SERV_ADDR server,\n" \
                                                      "													IN ZOO_INT32 function_code,\n" \
                                                      "													INOUT " + self._compoent_id + "4I_REPLY_STRUCT *reply_message,\n" \
                                                      "													IN ZOO_INT32 timeout)\n"

        fd = fd + "{\n" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    ZOO_INT32 actual_replay_length = 0;    /*the actual reply message length*/\n" \
                  "    ZOO_INT32 reply_length = 0; /*expect reply message length*/\n" \
                  "    result = " + self._compoent_id + "4I_get_reply_message_length( function_code, &reply_length );\n" \
                     "    /*Get message*/\n" \
                     "    if ( OK == result )\n" \
                     "    {\n" \
                     "        result = MQ4A_receive_reply( server, \n" \
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
             "*@brief \n" \
             "*@param event_id       \n" \
             "*@param *reply_message \n" \
             "*@description:         \n" \
             "*@precondition:\n*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_INT32 " + self._compoent_id + "4I_publish_event(IN const MQ4A_SERV_ADDR server,\n" \
                "													IN ZOO_INT32 event_id,\n" \
                "													INOUT " + self._compoent_id + "4I_REPLY_STRUCT *reply_message)\n"
        fd = fd + "{\n" \
                  "    ZOO_INT32 result = OK;\n" \
                  "    ZOO_INT32 reply_length = 0;\n" \
                  "    result = " + self._compoent_id + "4I_get_reply_message_length(reply_message->reply_header.function_code, &reply_length);\n" \
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
             "*@brief send subscribe message\n" \
             "*@param server            \n" \
             "*@param callback_function \n" \
             "*@param callback_struct   \n" \
             "*@param event_id          \n" \
             "*@param *handle           \n" \
             "*@param *context          \n " \
             "*@precondition:\n*@postcondition:\n" \
             "*/" \
             "\n"
        fd = fd + "ZOO_INT32 " + self._compoent_id + "4I_send_subscribe(IN const MQ4A_SERV_ADDR server,\n" \
                                                      "													IN MQ4A_EVENT_CALLBACK_FUNCTION callback_function,\n" \
                                                      "													IN MQ4A_CALLBACK_STRUCT *callback_struct,\n" \
                                                      "													IN ZOO_INT32 event_id,\n" \
                                                      "													INOUT ZOO_HANDLE *handle,\n" \
                                                      "													INOUT void *context)\n"
        fd = fd + "{\n" \
                  "    ZOO_INT32 result = OK;\n" \
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
             "*@brief Cancel subscribe \n" \
             "*@param server   \n" \
             "*@param event_id \n" \
             "*@param handle    \n" \
             "*@precondition:\n" \
             "*@postcondition:\n" \
             "*/\n"
        fd = fd + "ZOO_INT32 " + self._compoent_id + "4I_send_unsubscribe(IN const MQ4A_SERV_ADDR server,\n" \
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


    def generate(self):
        with open(self._path + '/' + self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")
            for incld in FILE_INCLUDE_CLASS([self._compoent_id + "4I_if.h"]).get_list():
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
            f.write(self.get_send_reply_message_difinition())
            f.write("\n\n")
            f.write(self.get_publish_event_difinition())
            f.write("\n\n")
            f.write(self.get_send_subscribe_difinition())
            f.write("\n\n")
            f.write(self.get_send_unsubscribe_difinition())
            f.write("\n\n")

        return


class XX4A_main_c(object):
    def __init__(self, compoent_id='', function_list=[], path=''):
        self._compoent_id = compoent_id
        self._function_list = function_list
        self._path = path
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', compoent_id + 'MA_main.c')
        self._file_name = path + '/' + self._compoent_id + "MA_main.c"
        self._server = compoent_id + "4A_SERVER"
        self._callback_handler = compoent_id + "MA_callback_handler"

    def generate(self):
        with open(self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")

            f.write("\n")
            for c in FILE_INCLUDE_CLASS(
                    ["string.h", "ZOO.h", "MQ4A_if.h", "MQ4A_type.h", "MM4A_if.h", self._compoent_id + "4I_type.h",self._compoent_id + "MA_executor_wrapper.h",
                     self._compoent_id + "MA_dispatch.h"]).get_list():
                f.write(c)
                f.write("\n")

            f.write("\n\n")
            f.write("/* Task or Process Entrance */\n")
            f.write("/* Accept one parameter for server address or use default server address by task name*/\n")
            f.write("ZOO_INT32 main(int argc,char *argv[])")
            f.write("\n")
            f.write("{")
            f.write("\n")
            f.write("    ZOO_INT32 rtn = OK;\n"
                    "    /* Server address */\n"
                    "    MQ4A_SERV_ADDR server_addr = {0};\n"
                    "    if(argc >= 2 )\n"
                    "    {\n"
                    "        strncpy(server_addr, argv[1], strlen(argv[1]));\n"
                    "        server_addr[31]= '\\0';\n"
                    "    }\n"
                    "    else\n"
                    "    {\n"
                    "        strncpy(server_addr," + self._server + ",strlen(" + self._server + "));\n"
                    "    }\n\n" 
                    "    /* Initialize memory pool */\n"
                    "    MM4A_initialize();\n\n"                            
                    "    /* Initliaze system and register info */\n"  
                    "    " + self._compoent_id +"MA_startup();\n\n"                      
                    "    /* Subscribe messages */\n"  
                    "    " + self._compoent_id +"MA_subscribe_driver_event();\n\n"                                           
                    "    if(OK == rtn)\n"
                    "    {\n"
                    "        /* Initialize server to prepare recv messages*/\n"
                    "        rtn = MQ4A_server_initialize(server_addr);\n"
                    "    }\n\n"
                    "    if(OK == rtn)\n"
                    "    {\n"
                    "        /* Register handler for recieve and response messages */\n"
                    "        rtn = MQ4A_register_event_handler(server_addr," + self._callback_handler + ");\n"
                    "    }\n\n"
                    "    if(OK == rtn)\n"
                    "    {\n"
                    "        /* Enter in listen state ,it is a sync interface*/\n"
                    "        rtn = MQ4A_enter_event_loop(server_addr);\n"
                    "    }\n\n"
                    "    /* Close server */\n"
                    "    MQ4A_server_terminate(server_addr);\n\n"
                    "    /* Shutdown memory pool */\n"
                    "    MM4A_terminate();\n\n"
                    "    /* Task cleanup */\n"
                    "    " + self._compoent_id +"MA_shutdown();\n"                                                                                                        
                    "    return rtn;\n")
            f.write("}")
            f.write("\n")
        return


class XX4A_dispatch_h(object):
    def __init__(self, compoent_id='', function_list=[], path=''):
        self._compoent_id = compoent_id
        self._function_list = function_list
        self._path = path
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', compoent_id + 'MA_dispatch.h')
        self._file_name = path + '/' + compoent_id + "MA_dispatch.h"
        self._callback_handler = compoent_id + "MA_callback_handler"

    def generate(self):
        with open(self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")

            f.write("\n")
            file_name = self._compoent_id + "MA_dispatch.h"
            f.write(get_ifndef(file_name))
            for c in FILE_INCLUDE_CLASS(["ZOO.h",
                                         "MQ4A_if.h",
                                         "MQ4A_type.h",
                                         "MM4A_if.h",
                                         self._compoent_id + "4I_type.h",
                                         self._compoent_id + "4I_if.h",
                                         self._compoent_id + "4A_type.h",
                                         self._compoent_id + "MA_implement.h",
                                         ]).get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")
            f.write("/**\n")
            f.write("*@brief " + "Dispatch message from client to server internal interface\n")
            f.write("*@param context       " + " \n")
            f.write("*@param server        " + "address\n")
            f.write("*@param msg           " + "request message to server\n")
            f.write("*@param len           " + "request message length\n")
            f.write("*@param reply_msg     " + "reply message length to caller\n")
            f.write("*@param reply_msg_len " + "reply message length\n")
            f.write("**/\n")
            f.write(
                "ZOO_EXPORT void " + self._callback_handler + "(void * context,const MQ4A_SERV_ADDR server,void * msg,ZOO_INT32 len);")
            f.write("\n\n")
            f.write(get_endif(file_name))
        return


class XX4A_dispatch_c(object):
    def __init__(self, compoent_id='', function_list=[], path=''):
        self._compoent_id = compoent_id
        self._function_list = function_list
        self._path = path
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', compoent_id + 'MA_dispatch.c')
        self._file_name = path + '/' + compoent_id + "MA_dispatch.c"
        self._callback_handler = compoent_id + "MA_callback_handler"

    def generate(self):
        with open(self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")

            f.write("\n")
            for c in FILE_INCLUDE_CLASS([self._compoent_id + "MA_dispatch.h",
                                         self._compoent_id + "MA_implement.h"]).get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")

            for func in self._function_list:
                if func.get_interface_type() == 'Sync':
                    f.write(func.get_comment(func.get_local_name()))
                    f.write(func.get_local_function(self._compoent_id))
                    f.write(func.get_local_function_body(self._compoent_id))
                    f.write("\n")

            f.write("/**\n")
            f.write("*@brief " + "Dispatch message from client to server internal interface\n")
            f.write("*@param context       " + " \n")
            f.write("*@param server        " + "address\n")
            f.write("*@param msg           " + "request message to server\n")
            f.write("*@param len           " + "request message length\n")
            f.write("*@param reply_msg     " + "reply message length to caller\n")
            f.write("*@param reply_msg_len " + "reply message length\n")
            f.write("**/\n")
            f.write(
                "void " + self._callback_handler + "(void * context,const MQ4A_SERV_ADDR server,void * msg,ZOO_INT32 len)")
            f.write("\n")
            f.write("{\n")
            f.write("    ZOO_INT32 rtn = OK;\n")
            f.write("    ZOO_INT32 rep_length = 0;\n")
            f.write("    " + self._compoent_id + "4I_REQUEST_STRUCT *request = (" + self._compoent_id + "4I_REQUEST_STRUCT*)msg;\n")
            f.write("    " + self._compoent_id + "4I_REPLY_STRUCT *reply = NULL;\n")
            f.write("    if(request == NULL)\n")
            f.write("    {\n")
            f.write("        rtn = " + self._compoent_id + "4A_SYSTEM_ERR;\n")
            f.write("        EH4A_show_exception("+ self._compoent_id + "4I_COMPONET_ID,__FILE__,__ZOO_FUNC__,__LINE__," + self._compoent_id + "4A_PARAMETER_ERR,0,\"request_message pointer is NULL ...ERROR\");\n")
            f.write("        return;\n")
            f.write("    }\n\n")
            f.write("    if(OK == rtn)\n")
            f.write("    {\n")
            f.write("        switch(request->request_header.function_code)\n")
            f.write("        {\n")
            for func in self._function_list:
                if func.get_interface_type() == 'Sync':
                    f.write("            " + "case " + func.get_function_code_upper() + ":\n")
                    f.write("                " + func.get_local_name() + "(server,request,request->request_header.function_code);" + "\n")
                    f.write("                break;\n")
            f.write("            default:\n")
            f.write("                EH4A_show_exception("+ self._compoent_id + "4I_COMPONET_ID,__FILE__,__ZOO_FUNC__,__LINE__," + self._compoent_id + "4A_SYSTEM_ERR,0,\"invalid function code ...ERROR\");\n")
            f.write("                rtn = " + self._compoent_id+"4A_SYSTEM_ERR;\n")
            f.write("                break;\n")
            f.write("        }\n")
            f.write("    }\n\n")
            f.write("    if(OK != rtn && request->request_header.need_reply)\n")
            f.write("    {\n")
            f.write("        rtn = "+ self._compoent_id + "4I_get_reply_message_length(request->request_header.function_code, &rep_length);\n")
            f.write("        if(OK != rtn)\n")
            f.write("        {\n")
            f.write("            EH4A_show_exception(" + self._compoent_id + "4I_COMPONET_ID,__FILE__,__ZOO_FUNC__,__LINE__," + self._compoent_id + "4A_SYSTEM_ERR,0,\"Get message length failed ...ERROR\");\n")
            f.write("            rtn = " + self._compoent_id + "4A_SYSTEM_ERR;\n")
            f.write("        }\n\n")
            f.write("        if(OK == rtn)\n")
            f.write("        {\n")
            f.write("            reply = (" + self._compoent_id + "4I_REPLY_STRUCT *)MM4A_malloc(rep_length);\n")
            f.write("            if(reply == NULL)\n")
            f.write("            {\n")
            f.write("                EH4A_show_exception(" + self._compoent_id + "4I_COMPONET_ID,__FILE__,__ZOO_FUNC__,__LINE__," + self._compoent_id + "4A_SYSTEM_ERR,0,\"malloc failed ...ERROR\");\n")
            f.write("                rtn = " + self._compoent_id + "4A_SYSTEM_ERR;\n")
            f.write("            }\n")
            f.write("        }\n\n")
            f.write("        if(OK == rtn)\n")
            f.write("        {\n")
            f.write("            memset(reply, 0x0, rep_length);\n")
            f.write("            reply->reply_header.execute_result = rtn;\n")
            f.write("            reply->reply_header.function_code = request->request_header.function_code;\n")
            f.write("            rtn = " + self._compoent_id + "4I_send_reply_message(server,reply->reply_header.function_code,reply);\n")
            f.write("        }\n")
            f.write("    }\n")
            f.write("    return;\n")
            f.write("}\n\n")
        return


class XX4A_event_h(object):
    def __init__(self, compoent_id='', function_list=[], path='', callback_list=[]):
        self._compoent_id = compoent_id
        self._function_list = function_list
        self._callback_list = callback_list
        self._path = path
        self._file_name = self._compoent_id + "MA_event.h"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', compoent_id + 'MA_event.h')

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
                                         self._compoent_id + "4I_type.h",
                                         self._compoent_id + "4I_if.h",
                                         self._compoent_id + "4A_type.h",
                                         ]).get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")

            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write(func.get_comment(func.get_event_name()))
                    f.write(func.get_event_function_definition(self._compoent_id))
                    f.write("\n")
                if func.get_interface_type() == "subscribe":
                    for callback in self._callback_list:
                        callback_type = callback.get_name()
                        for pm in func.get_input_parameters_list():
                            if pm.get_type() in callback_type:
                                f.write(callback.get_comment(func.get_function_name()))
                                f.write(callback.get_function_difinition(func.get_function_name(), self._compoent_id))
                                f.write("\n\n")
                            break
            f.write("\n")
            f.write(get_endif(self._file_name))
        return


class XX4A_event_c(object):
    def __init__(self, compoent_id='', function_list=[], path='', callback_list=[]):
        self._compoent_id = compoent_id
        self._function_list = function_list
        self._callback_list = callback_list
        self._path = path
        self._file_name = self._compoent_id + "MA_event.c"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', compoent_id + 'MA_event.c')

    def generate(self):
        with open(self._path + '/' + self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")

            for c in FILE_INCLUDE_CLASS([self._compoent_id + 'MA_event.h']).get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")

            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write(func.get_comment(func.get_event_name()))
                    f.write(func.get_event_function(self._compoent_id))
                    f.write("\n")
                    f.write(func.get_event_function_body(self._compoent_id))
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
                                f.write(callback.get_function_name_extend(func.get_function_name(),self._compoent_id))
                                f.write("\n")
                                f.write(callback.get_function_body(func, self._compoent_id))
                                f.write("\n")
                            break
            f.write("\n")
        return


class XX4A_implement_h(object):
    def __init__(self, compoent_id='', function_list=[], path=''):
        self._compoent_id = compoent_id
        self._function_list = function_list
        self._path = path
        self._file_name = self._compoent_id + "MA_implement.h"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', compoent_id + 'MA_implement.h')

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
                                         self._compoent_id + "MA_event.h",
                                         self._compoent_id + "4I_type.h",
                                         self._compoent_id + "4A_type.h",
                                         ]).get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")
            f.write("\n")
            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write(func.get_comment(func.get_implement_name()))
                    f.write(func.get_implement_function_definition(self._compoent_id))
                    f.write("\n")
            f.write("\n")
            f.write(get_endif(self._file_name))
        return


class XX4A_implement_c(object):
    def __init__(self, compoent_id='', function_list=[], path=''):
        self._compoent_id = compoent_id
        self._function_list = function_list
        self._path = path
        self._file_name = self._compoent_id + "MA_implement.c"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', 'XX', compoent_id + 'MA_implement.c')

    def generate(self):
        with open(self._path + '/' + self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")

            for c in FILE_INCLUDE_CLASS([self._compoent_id + 'MA_implement.h']).get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \""+ self._compoent_id +"_FLOW_FACADE_WRAPPER.h\"\n\n")
            for func in self._function_list:
                if func.get_interface_type() == "Sync":
                    f.write(func.get_comment(func.get_implement_name()))
                    f.write(func.get_implement_function(self._compoent_id))
                    f.write("\n")
                    f.write(func.get_implement_function_body(self._compoent_id))
                    f.write("\n")
            f.write("\n")
        return


class Makefile(object):
    def __init__(self, compoent_id='', path=''):
        self._compoent_id = compoent_id
        self._path = path
        self._bin_makefile_name = compoent_id + "MA.mk"
        self._lib_makefile_name = "lib" + compoent_id + "4A.mk"
        self._test_mk = "utmf_"+compoent_id + "MA.mk"


    def generate_makefile(self):

        if not os.path.exists(self._path + '/' + self._bin_makefile_name):
            with open(self._path + '/' + self._bin_makefile_name, 'w+') as f:
                f.write("include ../Makefile_tpl_cov\n" \
                        "include ../Project_config\n\n" \
                        "TARGET   := " + self._compoent_id + "MA\n" \
                        "SRCEXTS  := .cpp .c \n" \
                        "INCDIRS  := ./inc ./com\n" \
                        "SOURCES  := \n" \
                        "SRCDIRS  := ./bin ./lib\n" \
                        "CFLAGS   := \n" \
                        "CXXFLAGS := -std=c++14 -fstack-protector-all\n" \
                        "CPPFLAGS := -DBOOST_ALL_DYN_LINK\n" \
                        "LDFPATH  := -L$(THIRD_PARTY_LIBRARY_PATH)\n" \
                        "LDFLAGS  := $(GCOV_LINK) $(LDFPATH) -lTR4A -lEH4A -lMM4A -lMQ4A -lDB4A -lZOO \n\n"\
                        "include ../Makefile_tpl_linux")

        if not os.path.exists(self._path + '/' + self._lib_makefile_name):
            with open(self._path + '/' + self._lib_makefile_name, 'w+') as f:
                f.write("include ../Makefile_tpl_cov\n" \
                        "TARGET   := lib" + self._compoent_id + "4A.so\n" \
                        "SRCEXTS  := .c .cpp \n" \
                        "INCDIRS  := ./inc ./com\n" \
                        "SOURCES  := \n" \
                        "SRCDIRS  := ./lib \n" \
                        "CFLAGS   := -fPIC\n" \
                        "CXXFLAGS := -std=c++14\n" \
                        "CPPFLAGS := $(GCOV_FLAGS) -fPIC\n" \
                        "LDFLAGS  := $(GCOV_LINK)  -lnsl -shared\n\n" \
                        "include ../Project_config\n" \
                        "include ../Makefile_tpl_linux")

        if not os.path.exists(self._path + '/' + self._test_mk):
            with open(self._path + '/' + self._test_mk, 'w+') as f:
                f.write("include ../Makefile_tpl_cov\n" \
                         "include ../Project_config\n\n" \
                         "TARGET   := utmf_" + self._compoent_id + "MA\n" \
                         "SRCEXTS  := .cpp .c \n" \
                         "INCDIRS  := ./inc ./com ./test/inc ./test/com\n" \
                         "SOURCES  := ./bin/MOCK_DATA_PARSER_CLASS.cpp ./bin/MOCK_DATA_CLASS.cpp ./test/bin/"+self._compoent_id+"_unit_test_main.cpp\n" \
                         "SRCDIRS  := \n" \
                         "CFLAGS   := \n" \
                         "CXXFLAGS := -std=c++14 -fstack-protector-all\n" \
                         "CPPFLAGS := -DBOOST_ALL_DYN_LINK\n" \
                         "LDFPATH  := -L$(THIRD_PARTY_LIBRARY_PATH)\n" \
                         "LDFLAGS  := $(GCOV_LINK) $(LDFPATH) -l"+self._compoent_id+"4A -lTR4A -lEH4A -lMM4A -lMQ4A -lZOO -lboost_unit_test_framework\n\n" \
                         "include ../Makefile_tpl_linux")

        if not os.path.exists(self._path + '/Makefile'):
            with open(self._path + '/Makefile', 'w+') as f:
                f.write("#Gun make/Qmake编译对象列表，不区分Unix/Linux(必须以.mk为后缀)\n")
                f.write("SUB_PRJ_NAME = "+ self._compoent_id + "\n")
                f.write("VPATH_MAKEFILES := ../$(SUB_PRJ_NAME)\n")
                f.write("EXT_HEADERS   := $(VPATH_MAKEFILES) ../zinc/ZOO.h ../zinc/ZOO_station.h ../zinc/ZOO_type.h\n\n")

                f.write("PLATFORM := $(shell uname)\n")
                f.write("ifeq ($(PLATFORM), Linux)\n\n")

                f.write("#Linux平台Makefile\n")
                f.write("SUN_MA_MAKEFILES  := ./" +self._bin_makefile_name + "\n")
                f.write("SUN_LIB_MAKEFILES := ./" + self._lib_makefile_name + "\n")
                f.write("SUN_TST_MAKEFILES := ./"+self._test_mk +"\n\n")
                f.write("else\n\n")
                f.write("#Firmware平台Makefile\n")
                f.write("FW_MA_MAKEFILES  := \n")
                f.write("FW_LIB_MAKEFILES := \n")
                f.write("FW_TST_MAKEFILES := \n\n")
                f.write("endif\n\n")
                f.write("include ../Project_config\n")
                f.write("include ../Makefile_tpl_cc\n")
        return

class EXECUTOR_WRAPPER_h(object):
    def __init__(self,compoent_id = '',path=''):
        self._compoent_id = compoent_id
        self._path = path
        self._file_name = compoent_id + "MA_executor_wrapper.h"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', compoent_id, compoent_id + 'MA_executor_wrapper.h')

    def generate(self):
        with open(self._path + '/' + self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("#ifdef __cplusplus \nextern \"C\" \n{\n#endif\n\n")
            for c in FILE_INCLUDE_CLASS(['ZOO.h',self._compoent_id+"4I_type.h"]).get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")
            f.write("    /**\n    *@brief This function response to create factory instance or load environment configurations \n    **/\n")
            f.write("    ZOO_EXPORT void " + self._compoent_id + "MA_startup(void);\n\n")
            f.write("    /**\n    *@brief This function response to release instance or memory \n    **/\n")
            f.write("    ZOO_EXPORT void " + self._compoent_id + "MA_shutdown(void);\n\n")
            f.write("    /**\n    *@brief Subscribe events published from hardware drivers \n    **/\n")
            f.write("    ZOO_EXPORT void " + self._compoent_id +"MA_subscribe_driver_event(void);\n\n")
            f.write("\n")
            f.write("#ifdef __cplusplus \n }\n#endif\n\n")
            f.write(get_endif(self._file_name))

class EXECUTOR_WRAPPER_c(object):
    def __init__(self,compoent_id = '',path=''):
        self._compoent_id = compoent_id
        self._path = path
        self._file_name = compoent_id + "MA_executor_wrapper.cpp"
        self._header_comment = FILE_HEADER_COMMENT_CLASS('ZOO', compoent_id, compoent_id + 'MA_executor_wrapper.c')
    def generate(self):
        with open(self._path + '/' + self._file_name, 'w+') as f:
            for c in self._header_comment.get_list():
                f.write(c)
                f.write("\n")
            for c in FILE_INCLUDE_CLASS([self._compoent_id + 'MA_executor_wrapper.h',"ZOO_COMMON_MACRO_DEFINE.h"]).get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")
            f.write("#include \"utils/THREAD_POOL.h\"\n")
            f.write("#include \"COMMON_FLOW_FACADE_CLASS.h\"\n")
            f.write("#include \"PROCESSING_FLOW_FACADE_CLASS.h\"\n")
            f.write("#include \"STATE_MANAGER_CLASS.h\"\n")
            f.write("#include \"DEVICE_CONTROLLER_CLASS.h\"\n")
            f.write("#include \"EVENT_PUBLISHER_CLASS.h\"\n")
            f.write("#include \""+self._compoent_id+"_CONFIGURE.h\"\n")

            f.write("/*\n")
            f.write(" * @brief Define the device controller.\n")
            f.write("**/\n")
            f.write("boost::shared_ptr<" + self._compoent_id + "::DEVICE_CONTROLLER_INTERFACE> g_device_controller;\n\n")

            f.write("/*\n")
            f.write(" * @brief Define common flow instance.\n")
            f.write("**/\n")
            f.write("boost::shared_ptr<" + self._compoent_id + "::COMMON_FLOW_FACADE_INTERFACE> g_common_flow;\n\n")

            f.write("/*\n")
            f.write(" * @brief Define processing flow instance.\n")
            f.write("**/\n")
            f.write("boost::shared_ptr<" + self._compoent_id + "::PROCESSING_FLOW_FACADE_INTERFACE> g_processing_flow;\n\n")

            f.write("/*\n")
            f.write(" * @brief Define the state manager.\n")
            f.write("**/\n")
            f.write("boost::shared_ptr<" + self._compoent_id + "::STATE_MANAGER_CLASS> g_state_manager;\n\n")

            f.write("/*\n")
            f.write(" * @brief The event publisher instance.\n")
            f.write("**/\n")
            f.write("boost::shared_ptr<" + self._compoent_id + "::EVENT_PUBLISHER_CLASS> g_event_publisher;\n\n")

            f.write("/**  \n"
                    " * @brief Register system signal handler,throw PARAMETER_EXCEPTION_CLASS if register fail,\n"\
                    " * the default signal handling is save stack trace to the log file and generate a dump file at execute path.\n"\
                    " * register a self-defined callback to SYSTEM_SIGNAL_HANDLER::resgister_siganl will change the default behavior.\n**/\n"\
                    "static void "+ self._compoent_id + "MA_register_system_signals()\n"\
                    "{\n"\
                    "    __ZOO_TRACE("+ self._compoent_id + "4I_COMPONET_ID,\" function entry ...\");\n" \
                    "    __ZOO_SYSTEM_SIGNAL_REGISTER("+ self._compoent_id + "4I_COMPONET_ID,SIGSEGV); \n" \
                    "    __ZOO_SYSTEM_SIGNAL_REGISTER("+ self._compoent_id + "4I_COMPONET_ID,SIGABRT);\n\n"\
                    "    /* Add more signals if needs,or register self-defined callback function\n"
                    "       to change the default behavior... */\n"\
                    "    __ZOO_TRACE("+ self._compoent_id + "4I_COMPONET_ID,\"< function exit ...\");\n}\n\n")

            f.write("/**\n"\
                    " *@brief Execute the start up flow.\n"\
                    " * This function is executed in 3 steps: \n"\
                    " * Step 1: Load configurations \n"
                    " * Step 2: Create controllers\n"\
                    " * Step 3: Create facades and set controllers to created facades\n"\
                    "**/ \n"\
                    "void " + self._compoent_id + "MA_startup(void)\n"\
                    "{\n"\
                    "    __ZOO_TRACE("+ self._compoent_id + "4I_COMPONET_ID,\"> function entry ...\");\n" \
                    "    try\n" \
                    "    {\n" \
                    "        /**\n         * @brief Signal handler for system behavior \n        */\n"\
                    "        "+ self._compoent_id + "MA_register_system_signals();\n\n"\
                    "        /** \n         *@brief Step 1: Load configurations \n        */\n"
                    "        " + self._compoent_id + "::" + self._compoent_id + "_CONFIGURE::get_instance()->initialize();\n"
                    "        /** \n         *@brief Startup thread pool. \n        */\n"\
                    "        ZOO_COMMON::THREAD_POOL::get_instance()->startup();\n\n"\
                    "        /** \n         *@brief Step 2: Create controllers \n        */\n"
                    "        g_state_manager.reset(new " + self._compoent_id + "::STATE_MANAGER_CLASS());\n"\
                    "        g_device_controller.reset(new " + self._compoent_id + "::DEVICE_CONTROLLER_CLASS());\n"\
                    "        g_event_publisher.reset(new " + self._compoent_id + "::EVENT_PUBLISHER_CLASS());\n"\
                    "        g_device_controller->set_event_publisher(g_event_publisher);\n\n"\
                    "        /** \n         *@brief Step 3: Create facades and set controllers to created facades \n        */\n"\
                    "        g_processing_flow.reset(new "+self._compoent_id +"::PROCESSING_FLOW_FACADE_CLASS());\n"\
                    "        g_processing_flow->set_device_controller(g_device_controller);\n"\
                    "        g_processing_flow->set_state_manager(g_state_manager);\n"\
                    "        g_common_flow.reset(new "+self._compoent_id +"::COMMON_FLOW_FACADE_CLASS());\n"\
                    "        g_common_flow->set_device_controller(g_device_controller);\n"\
                    "        g_common_flow->set_state_manager(g_state_manager);\n\n"\
                    "        g_device_controller->add_observer(g_common_flow.get());\n"\
                    "        g_device_controller->add_observer(g_processing_flow.get());\n\n"\
                    "    }\n" \
                    "    catch(...)\n" \
                    "    {\n" \
                    "        __ZOO_TRACE("+ self._compoent_id + "4I_COMPONET_ID,\":: unhandle exception ...ERROR\");\n" \
                    "    }\n" \
                    "    __ZOO_TRACE("+ self._compoent_id + "4I_COMPONET_ID,\"< function exit ...\");\n"\
                    "}\n\n")

            f.write("/**\n "\
                    "*@brief This function response to release instance or memory \n"\
                    "**/ \n"\
                    "void " + self._compoent_id + "MA_shutdown(void)\n"\
                    "{\n"\
                    "    __ZOO_TRACE("+ self._compoent_id + "4I_COMPONET_ID,\"> function entry ...\");\n"\
                    "    try\n    {\n"   
                    "        /** User add */\n"\
                    "        g_processing_flow.reset();\n"\
                    "        g_common_flow.reset();\n"\
                    "        g_device_controller.reset();\n"\
                    "        g_state_manager.reset();\n"\
                    "        ZOO_COMMON::THREAD_POOL::get_instance()->shutdown();\n"\
                    "    }\n" \
                    "    catch(...)\n" \
                    "    {\n" \
                    "        __ZOO_TRACE("+ self._compoent_id + "4I_COMPONET_ID,\":: unhandle exception ...ERROR\");\n" \
                    "    }\n" \
                    "    __ZOO_TRACE("+ self._compoent_id + "4I_COMPONET_ID,\"< function exit ...\");\n"\
                    "}\n\n")

            f.write("/**\n"
                    " *@brief Subscribe events published from hardware drivers \n"\
                    "**/\n"\
                    "void " + self._compoent_id +"MA_subscribe_driver_event(void)\n"\
                    "{\n"\
                    "    __ZOO_TRACE("+ self._compoent_id + "4I_COMPONET_ID,\"> function entry ...\");\n"\
                    "    try\n"
                    "    {\n"
                    "        g_common_flow->subscribe_driver_events();\n"\
                    "    }\n"\
                    "    catch(...)\n" \
                    "    {\n" \
                    "        __ZOO_TRACE("+ self._compoent_id + "4I_COMPONET_ID,\":: unhandle exception ...ERROR\");\n" \
                    "    }\n" \
                    "    __ZOO_TRACE("+ self._compoent_id + "4I_COMPONET_ID,\"< function exit ...\");\n"\
                    "}\n\n")

class UNIT_TEST(object):
    def  __init__(self, compoent_id='', path='',function_list = [FUNCTION_CLASS()]):
        self._compoent_id = compoent_id
        self._path = path
        self._function_list = function_list
        self._makefile = "Makefile"
        self._mk = compoent_id + "_test.mk"
        self._file_name_global = compoent_id + "_GLOBAL_FIXTRUE.h"
        self._file_name_utp = compoent_id + "_positive_test_suite.h"
        self._file_name_utn = compoent_id + "_nagetive_test_suite.h"
        self._file_name_shutdown = compoent_id + "_SHUTDOWN.h"
        self._file_name_test_files = []
        self._file_name_main = compoent_id + "_unit_test_main.cpp"
        self._reporter_file = compoent_id + "_TC_result.reporter\""
        self._reporter_file_path = "\"../../../reporter/"
        self._header_comment_4a = FILE_HEADER_COMMENT_CLASS('ZOO', compoent_id, compoent_id + '_unit_test.h')

    def generate(self):
        self.generate_dir()
        self.generate_global_fixture()
        self.generate_test_cases()
        self.generate_main()
        self.generate_shutdown()

    def generate_dir(self):
        path = os.getcwd() + '/' + self._compoent_id + '/' + 'test' +'/'
        if not os.path.exists(path +"inc"):
            os.makedirs(path +"inc")
        if not os.path.exists(path +"lib"):
            os.makedirs(path +"lib")
        if not os.path.exists(path +"bin"):
            os.makedirs(path +"bin")
        if not os.path.exists(path +"com"):
            os.makedirs(path +"com")

    def generate_global_fixture(self):
        global_fixture_name = "TC_" + self._compoent_id.upper() + "_GOLBAL_FIXTURE"
        global_report_name = "TC_" + self._compoent_id.upper() + "_REPORTER"
        with open(self._path + '/com/TC_' + self._file_name_global, 'w+') as f:
            for c in self._header_comment_4a.get_list():
                f.write(c)
                f.write("\n")
            f.write("extern \"C\"\n")
            f.write("{\n")
            f.write("    #include <" + self._compoent_id + "4A_if.h>\n")
            f.write("    #include <" + self._compoent_id + "4A_type.h>\n")
            f.write("    #include <MM4A_if.h>\n")
            f.write("}\n")
            f.write("#include <boost/test/included/unit_test.hpp>\n")
            f.write("#include <boost/test/tools/output_test_stream.hpp>\n")
            f.write("#include <boost/test/results_reporter.hpp>\n")
            f.write("#include <boost/test/unit_test_log.hpp>\n")
            f.write("#include <string>\n")
            f.write("/**\n"
                    "* @brief Define mock data parser instance.\n"
                    "*/\n")
            f.write("using namespace "+self._compoent_id+";\n")
            f.write("/**\n"
                    "* @brief Define a test suite entry/exit,so that the setup function is called only once\n"
                    "* upon entering the test suite.\n"
                    "*/\n")
            f.write("struct " +global_fixture_name + "\n"
                    "{\n"
                    "    " + global_fixture_name + "()\n"
                    "    {\n"
                    "        BOOST_TEST_MESSAGE(\"TC global fixture initialize ...\");\n"
                    "        MM4A_initialize();\n"
                    "    }\n\n"
                    "    ~" + global_fixture_name + "()\n"
                    "    {\n"
                    "        BOOST_TEST_MESSAGE(\"TC teardown ...\");\n"
                    "        MM4A_terminate();\n"
                    "    }\n"
                    "};\n\n")
            f.write("BOOST_TEST_GLOBAL_FIXTURE("+global_fixture_name+");\n\n")
            f.write("\n")
            f.write("/**\n"\
                    " * @brief Define test report output formate, default --log_level=message.\n"\
                    "*/")
            f.write("\n")
            f.write("struct " + global_report_name + "\n"
                    "{\n"
                    "    " + global_report_name + "():reporter("+self._reporter_file_path + self._reporter_file +")\n"
                    "    {\n"
                    "        boost::unit_test::unit_test_log.set_stream( reporter );\n"
                    "        boost::unit_test::unit_test_log.set_threshold_level(boost::unit_test::log_test_units);\n"
                    "    }\n\n"
                    "    ~" + global_report_name + "()\n"
                    "    {\n"
                    "        boost::unit_test::unit_test_log.set_stream( std::cout );;\n"
                    "    }\n"
                     "   std::ofstream reporter;\n"
                    "};\n\n")
            f.write("BOOST_TEST_GLOBAL_CONFIGURATION(" + global_report_name + ");\n\n")

    def generate_main(self):
        with open(self._path + '/bin/' + self._file_name_main, 'w+') as f:
            for c in self._header_comment_4a.get_list():
                f.write(c)
                f.write("\n")
            f.write("#define BOOST_TEST_MODULE " + self._compoent_id + "_test_module \n")
            f.write("#define BOOST_TEST_DYN_LINK \n")
            f.write("#include <boost/test/unit_test.hpp>\n")
            f.write("#include <boost/test/unit_test_log.hpp>\n")
            f.write("#include <boost/test/unit_test_suite.hpp>\n")
            f.write("#include <boost/test/framework.hpp>\n")
            f.write("#include <boost/test/unit_test_parameters.hpp>\n")
            f.write("#include <boost/test/utils/nullstream.hpp>\n")

            f.write("/**\n"
                    " * @brief Execute <" + self._compoent_id + "> UTMF ...\n"
                    " * @brief <Global Fixture> header file can define the global variable.\n"
                    " * @brief modify the include header files sequence to change the unit test execution sequence but not case SHUTDOWN.\n"
                    " */\n")
            f.write("#include <TC_" + self._file_name_global + ">\n")
            for file in self._file_name_test_files:
                f.write("#include <TC_" + file + ".h>\n")
            f.write("\n")
            f.write("/**\n"
                    " * @brief This case should be executed at the end of all test cases to exit current process.\n"
                    " * @brief Close all this process events subscribe.\n"
                    " * @brief Close message queue context thread.\n"
                    " */\n")
            f.write("#include <TC_" + self._compoent_id + "_SHUTDOWN.h>\n")

    def generate_test_cases(self):
        i = 1
        for fc in self._function_list:
            self.generate_test_case(fc,i)
            i = i+1

    def generate_shutdown(self):
        with open(self._path + '/inc/' + "TC_" + self._compoent_id + "_SHUTDOWN.h", 'w+') as f:
            for c in self._header_comment_4a.get_list():
                f.write(c)
                f.write("\n")
            f.write("extern \"C\"\n")
            f.write("{\n")
            f.write("    #include <" + self._compoent_id + "4A_if.h>\n")
            f.write("    #include <" + self._compoent_id + "4A_type.h>\n")
            f.write("    #include <MM4A_if.h>\n")
            f.write("    #include <MQ4A_if.h>\n")
            f.write("}\n")
            f.write("BOOST_AUTO_TEST_SUITE(TC_" + self._compoent_id + "_SHUTDOWN_001)\n\n")
            f.write("    BOOST_AUTO_TEST_CASE( TC_" + self._compoent_id + "_SHUTDOWN_001_001 )\n")
            f.write("    {\n")
            f.write("        BOOST_TEST(MQ4A_shutdown_all_clients() == OK);\n")
            f.write("    }\n\n")
            f.write("BOOST_AUTO_TEST_SUITE_END()")

    def generate_test_case(self,fc = FUNCTION_CLASS(),fd = 1):
        test_case = fc.get_function_name().upper().replace("4A","")+ "_00"+str(fd)
        self._file_name_test_files.append(test_case)
        with open(self._path + '/inc/' + "TC_" +test_case + ".h", 'w+') as f:
            for c in self._header_comment_4a.get_list():
                f.write(c)
                f.write("\n")
            f.write("extern \"C\"\n")
            f.write("{\n")
            f.write("    #include <" + self._compoent_id + "4A_if.h>\n")
            f.write("    #include <" + self._compoent_id + "4A_type.h>\n")
            f.write("    #include <MM4A_if.h>\n")
            f.write("}\n")
            f.write("BOOST_AUTO_TEST_SUITE(TC_"+test_case+")\n\n")
            f.write("" + fc.get_comment())
            f.write("    BOOST_AUTO_TEST_CASE( TC_" + fc.get_function_name().upper().replace("4A", "") + "_00" + str(fd) + "_001 )\n")
            f.write("    {\n")
            for ip in fc.get_input_parameters_list():
                f.write("        " + ip.get_type() + " " + ip.get_name() + ";\n")
            for ip in fc.get_output_parameters_list():
                f.write("        " + ip.get_type() + " " + ip.get_name() + ";\n")
            for ip in fc.get_inoutput_parameters_list():
                f.write("        " + ip.get_type() + " " + ip.get_name() + ";\n")

            f.write("        BOOST_TEST(" + fc.get_function_name() + "(")
            p_list = ""
            for ip in fc.get_input_parameters_list():
                p_list += self.parse_parameter_name(ip.get_name()) + ","
            for ip in fc.get_output_parameters_list():
                p_list += self.parse_parameter_name(ip.get_name()) + ","
            for ip in fc.get_inoutput_parameters_list():
                p_list += self.parse_parameter_name(ip.get_name()) + ","
            p_list += ")"
            f.write(p_list.replace(",)", ")") + " == OK);\n")
            f.write("    }\n\n")
            f.write("BOOST_AUTO_TEST_SUITE_END()")

    def parse_parameter_name(self,p=""):
        pp = p.strip("*").strip()
        pattern = re.compile('\w*')
        result = re.search(pattern,pp)
        return result[0]

class FLOW_FACADE_WRAPPER(object):
    def __init__(self,functions = [],comp = '',dir = ''):
        self.functions = functions
        self.comp = comp
        self.file_h = dir + '/'  + comp + "_FLOW_FACADE_WRAPPER.h"
        self.file_cpp = dir + '/' + comp + "_FLOW_FACADE_WRAPPER.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,comp + '_FLOW_FACADE_WRAPPER.h')
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO',comp,comp + '_FLOW_FACADE_WRAPPER.cpp')
        self._file_name = comp + "_FLOW_FACADE_WRAPPER.h"

    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("#ifdef __cplusplus\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("#endif\n")
            f.write("    #include \"" + self.comp + "4A_type.h\"\n")
            f.write("    #include \"" + self.comp + "4I_type.h\"\n")
            for fn in self.functions:
                name = fn.get_function_name()
                name.replace("4A","")
                full_name = fn.get_function()
                flow_name = full_name.replace("ZOO_EXPORT","")
                flow_name = flow_name.replace("ZOO_INT32 "+ self.comp + "4A","ZOO_INT32 " + self.comp)
                if 'Sync' in fn.get_interface_type() :
                    f.write("    /*\n")
                    f.write("     * @brief " + fn.get_function_name() + "\n")
                    f.write("    **/\n")
                    f.write("    " + flow_name + "\n\n")
            f.write("#ifdef __cplusplus\n")
            f.write("}\n")
            f.write("#endif\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_cpp.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \"" + self.comp + "_FLOW_FACADE_WRAPPER.h\"\n")
            f.write("#include \"COMMON_FLOW_FACADE_CLASS.h\"\n")
            f.write("#include \"PROCESSING_FLOW_FACADE_CLASS.h\"\n\n")
            f.write("/*\n")
            f.write(" * @brief extern g_common_flow defined from executor_wrapper.cpp\n")
            f.write("**/\n")
            f.write("extern " + self.comp + "::COMMON_FLOW_FACADE_CLASS * g_common_flow;\n\n")
            f.write("/*\n")
            f.write(" * @brief extern g_processing_flow defined from executor_wrapper.cpp\n")
            f.write("**/\n")
            f.write("extern " + self.comp + "::PROCESSING_FLOW_FACADE_CLASS * g_processing_flow;\n\n")
            for fn in self.functions:
                name = fn.get_function_name()
                name.replace("4A","")
                full_name = fn.get_function()
                flow_name = full_name.replace("ZOO_EXPORT","")
                flow_name = flow_name.replace("ZOO_INT32 "+ self.comp + "4A","ZOO_INT32 " + self.comp)
                flow_name = flow_name.replace(";","")
                flow_name = flow_name.lstrip()
                if 'Sync' in fn.get_interface_type() :

                    flow = "g_processing_flow"
                    if "_initialize" in fn.get_function_name() \
                            or "_terminate" in fn.get_function_name() \
                            or "_get_driver_state" in fn.get_function_name() \
                            or "_get_status" in fn.get_function_name() \
                            or "_change_to_work_mode" in fn.get_function_name() \
                            or "_change_to_debug_mode" in fn.get_function_name() \
                            or "_download_machine_constants" in fn.get_function_name():
                        flow = "g_common_flow"

                    f.write("/*\n")
                    f.write(" * @brief " + fn.get_function_name() + "\n")
                    f.write("**/\n")
                    f.write(flow_name + "\n")
                    f.write("{\n")
                    f.write("    if(" + flow +" != nullptr)\n")
                    f.write("    {\n")
                    if "_get_driver_state" in fn.get_function_name():
                        f.write("        " + flow + "->" +fn.get_wrapper_name() + ";\n")
                        f.write("        return OK;\n")
                    else:
                        f.write("        return " + flow + "->" +fn.get_wrapper_name() + ";\n")
                    f.write("    }\n")
                    f.write("    return "+ self.comp +"4A_SYSTEM_ERR;\n")
                    f.write("}\n\n")

class STATE_MANAGER_CLASS(object):
    def __init__(self,  comp='', dir=''):
        self.comp = comp
        self.file_h = dir + '/' + "STATE_MANAGER_CLASS.h"
        self.file_cpp = dir + '/' + "STATE_MANAGER_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO', comp, 'STATE_MANAGER_CLASS.h')
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO', comp, 'STATE_MANAGER_CLASS.cpp')
        self._file_name = "STATE_MANAGER_CLASS.h"

    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("    #include <ZOO_tc.h>\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("}\n")
            f.write("#include <boost/shared_ptr.hpp>\n\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    class STATE_MANAGER_CLASS\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       STATE_MANAGER_CLASS();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~STATE_MANAGER_CLASS();\n")
            f.write("    public:\n")

            f.write("       /*\n")
            f.write("        * @brief Set driver state\n")
            f.write("       **/ \n")
            f.write("       void set_driver_state(IN ZOO_DRIVER_STATE_ENUM state);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Get driver state\n")
            f.write("       **/ \n")
            f.write("       ZOO_DRIVER_STATE_ENUM  get_driver_state();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Update driver state\n")
            f.write("       **/ \n")
            f.write("       void update_driver_state(IN ZOO_DRIVER_STATE_ENUM state);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Set running mode\n")
            f.write("       **/ \n")
            f.write("       void set_running_mode(IN ZOO_RUNNING_MODE_ENUM running_mode);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Get running mode\n")
            f.write("       **/ \n")
            f.write("       ZOO_RUNNING_MODE_ENUM  get_running_mode();\n\n")

            f.write("    private:\n")
            f.write("       /*\n")
            f.write("        * @brief The driver state.\n")
            f.write("       **/ \n")
            f.write("       ZOO_DRIVER_STATE_ENUM  m_driver_state;\n\n")

            f.write("       /*\n")
            f.write("        * @brief The running mode.\n")
            f.write("       **/ \n")
            f.write("       ZOO_RUNNING_MODE_ENUM  m_running_mode;\n\n")

            f.write("    };\n")
            f.write("}// namespace " + self.comp + "\n\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_cpp.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \"STATE_MANAGER_CLASS.h\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    STATE_MANAGER_CLASS::STATE_MANAGER_CLASS()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    STATE_MANAGER_CLASS::~STATE_MANAGER_CLASS()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Set driver state\n")
            f.write("    **/ \n")
            f.write("    void STATE_MANAGER_CLASS::set_driver_state(IN ZOO_DRIVER_STATE_ENUM state)\n")
            f.write("    {\n")
            f.write("        this->m_driver_state = state;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Get driver state\n")
            f.write("    **/ \n")
            f.write("    ZOO_DRIVER_STATE_ENUM STATE_MANAGER_CLASS::get_driver_state()\n")
            f.write("    {\n")
            f.write("        return this->m_driver_state;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Update driver state\n")
            f.write("    **/ \n")
            f.write("    void STATE_MANAGER_CLASS::update_driver_state(IN ZOO_DRIVER_STATE_ENUM state)\n")
            f.write("    {\n")
            f.write("        if(this->m_driver_state != state)\n")
            f.write("        {\n")
            f.write("            this->m_driver_state = state;\n")
            f.write("        }\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Set running mode\n")
            f.write("    **/ \n")
            f.write("    void STATE_MANAGER_CLASS::set_running_mode(IN ZOO_RUNNING_MODE_ENUM running_mode)\n")
            f.write("    {\n")
            f.write("        this->m_running_mode = running_mode;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Get running mode\n")
            f.write("    **/ \n")
            f.write("    ZOO_RUNNING_MODE_ENUM STATE_MANAGER_CLASS::get_running_mode()\n")
            f.write("    {\n\n")
            f.write("        return this->m_running_mode;\n")
            f.write("    }\n")
            f.write("}//namespace " + self.comp + "\n")

class ENUM_CONVERTER_CLASS(object):
    def __init__(self,  comp='', dir=''):
        self.comp = comp
        self.file_h = dir + '/' + "ENUM_CONVERTER_CLASS.h"
        self.file_cpp = dir + '/' + "ENUM_CONVERTER_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO', comp, 'ENUM_CONVERTER_CLASS.h')
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO', comp, 'ENUM_CONVERTER_CLASS.cpp')
        self._file_name = "ENUM_CONVERTER_CLASS.h"

    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("}\n")
            f.write("#include \"converters/ENUM_BASE_CONVERTER_CLASS.h\"\n")
            f.write("#include \"PROPERTY_CHANGE_KEY_DEFINE.h\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    REGISTER_ENUM_BEGIN(ZOO_DRIVER_STATE_ENUM)\n")
            f.write("    {\n")
            f.write("        REGISTER_ENUM(ZOO_DRIVER_STATE_MIN);\n")
            f.write("        REGISTER_ENUM(ZOO_DRIVER_STATE_UNKNOWN);\n")
            f.write("        REGISTER_ENUM(ZOO_DRIVER_STATE_IDLE);\n")
            f.write("        REGISTER_ENUM(ZOO_DRIVER_STATE_BUSY);\n")
            f.write("        REGISTER_ENUM(ZOO_DRIVER_STATE_TERMINATED);\n")
            f.write("        REGISTER_ENUM(ZOO_DRIVER_STATE_MAX);\n")
            f.write("    }\n")
            f.write("    REGISTER_ENUM_END;\n\n")

            f.write("    REGISTER_ENUM_BEGIN(ZOO_SIM_MODE_ENUM)\n")
            f.write("    {\n")
            f.write("        REGISTER_ENUM(ZOO_SIM_MODE_MIN);\n")
            f.write("        REGISTER_ENUM(ZOO_SIM_DISABLE);\n")
            f.write("        REGISTER_ENUM(ZOO_SIM_MODE_1);\n")
            f.write("        REGISTER_ENUM(ZOO_SIM_MODE_2);\n")
            f.write("        REGISTER_ENUM(ZOO_SIM_MODE_3);\n")
            f.write("        REGISTER_ENUM(ZOO_SIM_MODE_4);\n")
            f.write("        REGISTER_ENUM(ZOO_SIM_MODE_MAX);\n")
            f.write("    }\n")
            f.write("    REGISTER_ENUM_END;\n\n")

            f.write("    REGISTER_ENUM_BEGIN(ZOO_RUNNING_MODE_ENUM)\n")
            f.write("    {\n")
            f.write("        REGISTER_ENUM(ZOO_RUNNING_MODE_MIN);\n")
            f.write("        REGISTER_ENUM(ZOO_RUNNING_MODE_DEBUG);\n")
            f.write("        REGISTER_ENUM(ZOO_RUNNING_MODE_WORK);\n")
            f.write("        REGISTER_ENUM(ZOO_RUNNING_MODE_MAX);\n")
            f.write("    }\n")
            f.write("    REGISTER_ENUM_END;\n")

            f.write("}//namespace " + self.comp + "\n")
            f.write("#endif\n")


class DEVICE_INTERFACE(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  + "DEVICE_INTERFACE.h"
        self.file_cpp = dir + '/' + "DEVICE_INTERFACE.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,'DEVICE_INTERFACE.h')
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO',comp,'DEVICE_INTERFACE.cpp')
        self._file_name =  "DEVICE_INTERFACE.h"

    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include \"ZOO.h\"\n")
            f.write("    #include \"" + self.comp + "4A_type.h\"\n")
            f.write("    #include \"" + self.comp + "4I_type.h\"\n")
            f.write("}\n")
            f.write("#include \"" +self.comp + "_COMMON_MACRO_DEFINE.h\"\n")
            f.write("#include \"ENUM_CONVERTER_CLASS.h\"\n")
            f.write("#include \"MARKING_MODEL_INTERFACE.hpp\"\n\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    class DEVICE_INTERFACE: public virtual MARKING_MODEL_INTERFACE\n"\
                    "                             ,public virtual PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>\n"\
                    "                             ,public virtual NOTIFY_PROPERTY_CHANGED_INTERFACE<MARKING_MODEL_INTERFACE>\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       DEVICE_INTERFACE();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~DEVICE_INTERFACE();\n")
            f.write("    public:\n")

            f.write("       /*\n")
            f.write("        * @brief Add observer will be notified when property changed.\n")
            f.write("        * @param observer  Property changed observer\n")
            f.write("       **/ \n")
            f.write("       virtual void add_observer(PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>* observer);\n\n")


            f.write("       /*\n")
            f.write("        * @brief Remove observer will be notified when property changed.\n")
            f.write("        * @param observer  Property changed observer\n")
            f.write("       **/ \n")
            f.write("       virtual void remove_observer(PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>* observer);\n\n")


            f.write("       /*\n")
            f.write("        * @brief Clean.\n")
            f.write("       **/ \n")
            f.write("       void clean();\n")

            f.write("       /*\n")
            f.write("        * @brief Notify property has been changed.\n")
            f.write("        * @param property_name     The property has been changed\n")
            f.write("       **/ \n")
            f.write("       virtual void notify_of_property_changed(const ZOO_UINT32 property_name);\n\n")

            f.write("    protected:\n")
            f.write("       /*\n")
            f.write("        * @brief The list of observer instances will be notified when property has been changed.\n")
            f.write("       **/ \n")
            f.write("       std::vector<PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>*> m_observers;\n")

            f.write("    };\n")
            f.write("}// namespace " + self.comp + "\n\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_cpp.get_list():
                f.write(c)
                f.write("\n")
            f.write("\n")
            f.write("#include \"DEVICE_INTERFACE.h\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    DEVICE_INTERFACE::DEVICE_INTERFACE()\n")
            f.write("    {\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Destructor\n")
            f.write("    **/ \n")
            f.write("    DEVICE_INTERFACE::~DEVICE_INTERFACE()\n")
            f.write("    {\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Add observer will be notified when property changed.\n")
            f.write("     * @param observer  Property changed observer\n")
            f.write("    **/ \n")
            f.write("    void DEVICE_INTERFACE::add_observer(PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>* observer)\n")
            f.write("    {\n")
            f.write("        this->remove_observer(observer);\n")
            f.write("        this->m_observers.push_back(observer);\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Remove observer will be notified when property changed.\n")
            f.write("     * @param observer  Property changed observer\n")
            f.write("    **/ \n")
            f.write("    void DEVICE_INTERFACE::remove_observer(PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>* observer)\n")
            f.write("    {\n")
            f.write("        std::vector<PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>*>::iterator observer_itr =\n")
            f.write("            this->m_observers.begin();\n")
            f.write("        while (observer_itr != this->m_observers.end())\n")
            f.write("        {\n")
            f.write("            PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>* find_observer = *observer_itr;\n")
            f.write("            if (observer == find_observer)\n")
            f.write("            {\n")
            f.write("                this->m_observers.erase(observer_itr);\n")
            f.write("                break;\n")
            f.write("            }\n")
            f.write("        }\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Clean.\n")
            f.write("    **/\n")
            f.write("    void DEVICE_INTERFACE::clean()\n")
            f.write("    {\n")
            f.write("        this->m_observers.clear();\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Notify property has been changed.\n")
            f.write("     * @param property_name     The property has been changed\n")
            f.write("    **/ \n")
            f.write("    void DEVICE_INTERFACE::notify_of_property_changed(const ZOO_UINT32 property_name)\n")
            f.write("    {\n")
            f.write("        for (vector<PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>*>::iterator observer_itr =\n")
            f.write("            this->m_observers.begin(); observer_itr != this->m_observers.end(); observer_itr++)\n")
            f.write("        {\n")
            f.write("            PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>* observer = *observer_itr;\n")
            f.write("            if (observer != nullptr)\n")
            f.write("            {\n")
            f.write("                observer->on_property_changed(this,property_name);\n")
            f.write("            }\n")
            f.write("        }\n")
            f.write("    }\n\n")

            f.write("} // namespace " + self.comp + "\n\n")

class FLOW_FACADE_INTERFACE(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  + "FLOW_FACADE_INTERFACE.h"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,'FLOW_FACADE_INTERFACE.h')
        self._file_name =  "FLOW_FACADE_INTERFACE.h"

    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("    #include <" + self.comp + "4I_type.h>\n")
            f.write("}\n")
            f.write("#include \"MARKING_MODEL_INTERFACE.hpp\"\n")
            f.write("#include \"STATE_MANAGER_CLASS.h\"\n")
            f.write("#include \"DEVICE_CONTROLLER_INTERFACE.h\"\n\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    class FLOW_FACADE_INTERFACE: public virtual PROPERTY_CHANGED_OBSERVER_INTERFACE<CONTROLLER_INTERFACE>\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       FLOW_FACADE_INTERFACE(){}\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~FLOW_FACADE_INTERFACE(){}\n")
            f.write("    public:\n")

            f.write("       /*\n")
            f.write("        * @brief Set device controller instance\n")
            f.write("       **/ \n")
            f.write("       virtual void set_device_controller(IN boost::shared_ptr<DEVICE_CONTROLLER_INTERFACE> device_controller) = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Set state manager instance\n")
            f.write("       **/ \n")
            f.write("       virtual void set_state_manager(IN boost::shared_ptr<STATE_MANAGER_CLASS> state_manager) = 0;\n\n")

            f.write("    };\n")
            f.write("} // namespace " + self.comp + "\n\n")
            f.write("#endif\n")

class EVENT_PUBLISHER_CLASS(object):
    def __init__(self,comp = '',dir = '',function_list = [],callback_list = []):
        self.comp = comp
        self.file_h = dir + '/'  + "EVENT_PUBLISHER_CLASS.h"
        self.file_cpp = dir + '/' + "EVENT_PUBLISHER_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,'EVENT_PUBLISHER_CLASS.h')
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO',comp,'EVENT_PUBLISHER_CLASS.cpp')
        self._file_name =  "EVENT_PUBLISHER_CLASS.h"
        self._function_list = function_list
        self._callback_list = callback_list
        self._event_header_file = comp + "MA_event.h"

    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("}\n")
            f.write("#include \"" +self.comp + "_COMMON_MACRO_DEFINE.h\"\n")
            f.write("#include <boost/shared_ptr.hpp>\n\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     *@brief Define publish event to subsriber class.\n")
            f.write("    **/\n")
            f.write("    class EVENT_PUBLISHER_CLASS \n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       EVENT_PUBLISHER_CLASS();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~EVENT_PUBLISHER_CLASS();\n")
            f.write("    public:\n")

            i = 0
            for cf in self._function_list:
                if cf.get_interface_type() == "subscribe":
                    f.write("       /*\n")
                    prefix = self.comp + "4A_"
                    subfix = "_subscribe"
                    brief = cf.get_function_name().replace(prefix,"").replace(subfix,"")
                    f.write("        * @brief Publish " + brief +" changed event to subscriber.\n")

                    callback = self._callback_list[i]
                    for p in callback.get_input_parameters():
                        f.write("        * @param "+ p.get_name() + "\n")
                    for p in callback.get_output_parameters():
                        f.write("        * @param "+ p.get_name() + "\n")
                    for p in callback.get_inoutput_parameters():
                        f.write("        * @param "+ p.get_name() + "\n")
                    f.write("       **/ \n")

                    f_name =  cf.get_event_name() + "("
                    #callback = self._callback_list[i]
                    for p in callback.get_input_parameters():
                        f_name = f_name + p.get_type() + " " + p.get_name() + ","
                    for p in callback.get_output_parameters():
                        f_name = f_name + p.get_type() + " " + p.get_name() + ","
                    for p in callback.get_inoutput_parameters():
                        f_name = f_name + p.get_type() + " " + p.get_name() + ","
                    f_name = f_name.rstrip(",")
                    f_name = f_name + ")"
                    f.write("       void publish_" + f_name + ";\n\n")
                    i = i + 1

            f.write("    };\n")
            f.write("} // namespace " + self.comp + "\n\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_cpp.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \"EVENT_PUBLISHER_CLASS.h\"\n")
            f.write("#include \""+self._event_header_file+"\"\n\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    EVENT_PUBLISHER_CLASS::EVENT_PUBLISHER_CLASS()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    EVENT_PUBLISHER_CLASS::~EVENT_PUBLISHER_CLASS()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")

            i = 0
            for cf in self._function_list:
                if cf.get_interface_type() == "subscribe":
                    f.write("    /*\n")
                    prefix = self.comp + "4A_"
                    subfix = "_subscribe"
                    brief = cf.get_function_name().replace(prefix, "").replace(subfix, "")
                    f.write("    * @brief Publish " + brief + " changed event to subscriber.\n")
                    callback = self._callback_list[i]
                    for p in callback.get_input_parameters():
                        f.write("    * @param " + p.get_name() + "\n")
                    for p in callback.get_output_parameters():
                        f.write("    * @param " + p.get_name() + "\n")
                    for p in callback.get_inoutput_parameters():
                        f.write("    * @param " + p.get_name() + "\n")
                    f.write("    **/ \n")

                    f_name = cf.get_event_name() + "("
                    raise_function = cf.get_event_name()+ "("

                    #callback = self._callback_list[i]
                    for p in callback.get_input_parameters():
                        f_name = f_name + p.get_type() + " " + p.get_name() + ","
                        raise_function = raise_function + p.get_name().strip("*") + ","
                    for p in callback.get_output_parameters():
                        f_name = f_name + p.get_type() + " " + p.get_name() + ","
                        raise_function = raise_function + p.get_name().strip("*") + ","

                    for p in callback.get_inoutput_parameters():
                        f_name = f_name + p.get_type() + " " + p.get_name() + ","
                        raise_function = raise_function + p.get_name().strip("*") + ","

                    f_name = f_name.rstrip(",")
                    f_name = f_name + ")"
                    raise_function = raise_function.rstrip(",")
                    raise_function = raise_function + ")"
                    f.write("    void EVENT_PUBLISHER_CLASS::publish_" + f_name + "\n")
                    f.write("    {\n")
                    f.write("        " + raise_function + ";\n")
                    f.write("    }\n\n")
                    i = i + 1

            f.write("} //namespace " + self.comp + "\n\n")


class FLOW_FACADE_ABSTRACT_CLASS(object):
    def __init__(self,comp = '',dir = '',function_list = []):
        self.comp = comp
        self.file_h = dir + '/'  + "FLOW_FACADE_ABSTRACT_CLASS.h"
        self.file_cpp = dir + '/' + "FLOW_FACADE_ABSTRACT_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,'FLOW_FACADE_ABSTRACT_CLASS.h')
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO',comp,'FLOW_FACADE_ABSTRACT_CLASS.cpp')
        self._file_name =  "FLOW_FACADE_ABSTRACT_CLASS.h"

    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("}\n")
            f.write("#include \"" +self.comp + "_COMMON_MACRO_DEFINE.h\"\n")
            f.write("#include \"FLOW_FACADE_INTERFACE.h\"\n")
            f.write("#include \"ENUM_CONVERTER_CLASS.h\"\n")
            f.write("#include <cstdarg>\n")
            f.write("#include <boost/shared_ptr.hpp>\n\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    class FLOW_FACADE_ABSTRACT_CLASS : public virtual FLOW_FACADE_INTERFACE\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       FLOW_FACADE_ABSTRACT_CLASS();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~FLOW_FACADE_ABSTRACT_CLASS();\n")
            f.write("    public:\n")

            f.write("       /*\n")
            f.write("        * @brief Set device controller instance\n")
            f.write("       **/ \n")
            f.write("       void set_device_controller(IN boost::shared_ptr<DEVICE_CONTROLLER_INTERFACE> device_controller);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Get device controller instance\n")
            f.write("       **/ \n")
            f.write("       boost::shared_ptr<DEVICE_CONTROLLER_INTERFACE>  get_device_controller();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Set state manager instance\n")
            f.write("       **/ \n")
            f.write("       void set_state_manager(IN boost::shared_ptr<STATE_MANAGER_CLASS> state_manager);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Get state manager instance\n")
            f.write("       **/ \n")
            f.write("       boost::shared_ptr<STATE_MANAGER_CLASS>  get_state_manager();\n\n")

            f.write("       /*\n")
            f.write("        * @brief This method is executed when property changed value\n")
            f.write("        * @param model The source object contains property changed\n")
            f.write("        * @param property_name The property has been changed value\n")
            f.write("       **/ \n")
            f.write("       virtual void on_property_changed(IN CONTROLLER_INTERFACE* model,IN const ZOO_UINT32 property_name);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Check current driver state is ...\n")
            f.write("        * @param count    the driver state need to be verified\n")
            f.write("        * @exceptions     __THROW_XX_EXCEPTION\n")
            f.write("       **/\n")
            f.write("       void check_driver_state_is(ZOO_INT32 count, ...);\n\n")

            f.write("    protected:\n")
            f.write("       /*\n")
            f.write("        * @brief The device controller instance\n")
            f.write("       **/ \n")
            f.write("       boost::shared_ptr<DEVICE_CONTROLLER_INTERFACE>  m_device_controller;\n\n")

            f.write("       /*\n")
            f.write("        * @brief The state manager instance\n")
            f.write("       **/ \n")
            f.write("       boost::shared_ptr<STATE_MANAGER_CLASS>  m_state_manager;\n\n")
            f.write("    };\n")
            f.write("} //namespace " + self.comp + "\n\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_cpp.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \"FLOW_FACADE_ABSTRACT_CLASS.h\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    FLOW_FACADE_ABSTRACT_CLASS::FLOW_FACADE_ABSTRACT_CLASS()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    FLOW_FACADE_ABSTRACT_CLASS::~FLOW_FACADE_ABSTRACT_CLASS()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Set device controller instance\n")
            f.write("    **/ \n")
            f.write("    void FLOW_FACADE_ABSTRACT_CLASS::set_device_controller(IN boost::shared_ptr<DEVICE_CONTROLLER_INTERFACE> device_controller)\n")
            f.write("    {\n")
            f.write("        this->m_device_controller = device_controller;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Get device controller instance\n")
            f.write("    **/ \n")
            f.write("    boost::shared_ptr<DEVICE_CONTROLLER_INTERFACE>  FLOW_FACADE_ABSTRACT_CLASS::get_device_controller()\n")
            f.write("    {\n")
            f.write("        return this->m_device_controller;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Set state manager instance\n")
            f.write("    **/ \n")
            f.write("    void FLOW_FACADE_ABSTRACT_CLASS::set_state_manager(IN boost::shared_ptr<STATE_MANAGER_CLASS> state_manager)\n")
            f.write("    {\n")
            f.write("        this->m_state_manager = state_manager;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Get state manager instance\n")
            f.write("    **/ \n")
            f.write("    boost::shared_ptr<STATE_MANAGER_CLASS>  FLOW_FACADE_ABSTRACT_CLASS::get_state_manager()\n")
            f.write("    {\n")
            f.write("        return this->m_state_manager;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief This method is executed when property changed value\n")
            f.write("     * @param model The source object contains property changed\n")
            f.write("     * @param property_name The property has been changed value\n")
            f.write("    **/ \n")
            f.write("    void FLOW_FACADE_ABSTRACT_CLASS::on_property_changed(IN CONTROLLER_INTERFACE* model,IN const ZOO_UINT32 property_name)\n")
            f.write("    {\n")
            f.write("        // The implementation for this method will be written in concrete classes\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Check current driver state is ...\n")
            f.write("     * @param count    the driver state need to be verified\n")
            f.write("     * @exceptions     __THROW_XX_EXCEPTION\n")
            f.write("    **/\n")
            f.write("    void FLOW_FACADE_ABSTRACT_CLASS::check_driver_state_is(ZOO_INT32 count, ...)\n")
            f.write("    {\n")
            f.write("         __ZOO_TRACE("+self.comp+"4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("         ZOO_BOOL valid = ZOO_FALSE;\n")
            f.write("         ENUM_CONVERTER(ZOO_DRIVER_STATE_ENUM) driver_state_converter;\n")
            f.write("         va_list ap;\n")
            f.write("         va_start(ap,count);\n")
            f.write("         ZOO_DRIVER_STATE_ENUM current_driver_state = this->m_state_manager->get_driver_state();\n")
            f.write("         for(ZOO_INT32 i = 0; i < count ; ++i)\n")
            f.write("         {\n")
            f.write("             int state = static_cast<ZOO_DRIVER_STATE_ENUM>(va_arg(ap,ZOO_INT32));\n")
            f.write("             if(state == current_driver_state)\n")
            f.write("             {\n")
            f.write("                  valid =  ZOO_TRUE;\n")
            f.write("                  break;\n")
            f.write("             }\n")
            f.write("         }\n\n")
            f.write("         va_end(ap);\n")
            f.write("         if(!valid)\n")
            f.write("         {\n")
            f.write("             ZOO_CHAR std_err[128];\n")
            f.write("             sprintf(std_err,\"the driver state[%s] is not valid;\",driver_state_converter.to_string(current_driver_state));\n")
            f.write("             __THROW_"+self.comp+"_EXCEPTION("+self.comp+"4A_ILLEGAL_CALL_ERR,std_err,NULL);\n")
            f.write("         }\n")
            f.write("         __ZOO_TRACE("+self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("    }\n\n")

            f.write("} //namespace " + self.comp + "\n\n")

class PROCESSING_FLOW_FACADE(object):
    def __init__(self,functions = [],comp = '',dir = ''):
        self.functions = functions
        self.comp = comp
        self.file_h_interface = dir + '/'  + "PROCESSING_FLOW_FACADE_INTERFACE.h"
        self.file_h = dir + '/'  + "PROCESSING_FLOW_FACADE_CLASS.h"
        self.file_cpp = dir + '/' + "PROCESSING_FLOW_FACADE_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,'PROCESSING_FLOW_FACADE_CLASS.h')
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO',comp,'PROCESSING_FLOW_FACADE_CLASS.cpp')
        self._file_name =  "PROCESSING_FLOW_FACADE_CLASS.h"
        self._file_name_interface = "PROCESSING_FLOW_FACADE_INTERFACE.h"
        self._try = "__" + comp + "_TRY"
        self._catch_all = "__" + comp + "_CATCH_ALL(error_code)"
        self._illegal_call_err = comp + "4A_ILLEGAL_CALL_ERR"

    def generate_h(self):
        with open(self.file_h_interface, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name_interface))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("}\n")
            f.write("#include \"" +self.comp + "_COMMON_MACRO_DEFINE.h\"\n")
            f.write("#include \"MARKING_MODEL_INTERFACE.hpp\"\n")
            f.write("#include <boost/shared_ptr.hpp>\n")
            f.write("#include \"FLOW_FACADE_INTERFACE.h\"\n\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class PROCESSING_FLOW_FACADE_INTERFACE : public virtual FLOW_FACADE_INTERFACE\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       PROCESSING_FLOW_FACADE_INTERFACE(){}\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~PROCESSING_FLOW_FACADE_INTERFACE(){}\n")
            f.write("    public:\n")

            for fn in self.functions:
                name = fn.get_function_name()
                if "_initialize" in name:
                    continue
                if "_terminate" in name:
                    continue
                if "_get_status" in name:
                    continue
                if "_change_to_work_mode" in name:
                    continue
                if "_change_to_debug_mode" in name:
                    continue
                if "_download_machine_constants" in name:
                    continue
                if "_get_driver_state" in name:
                    continue
                name.replace(self.comp + "4A","")
                full_name = fn.get_function()
                flow_name = full_name.replace("ZOO_EXPORT","")
                flow_name = flow_name.replace("ZOO_INT32 "+ self.comp + "4A_","ZOO_INT32 ")
                if 'Sync' in fn.get_interface_type() :
                    f.write("        /*\n")
                    f.write("         * @brief " + fn.get_function_name() + "\n")
                    f.write("        **/\n")
                    f.write("        virtual" + flow_name.replace(";","") + " = 0;\n\n")
            f.write("    };\n")
            f.write("}// namespace " + self.comp + "\n\n")
            f.write("#endif\n")

        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("#include \"PROCESSING_FLOW_FACADE_INTERFACE.h\"\n")
            f.write("#include \"FLOW_FACADE_ABSTRACT_CLASS.h\"\n\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class PROCESSING_FLOW_FACADE_CLASS : public virtual PROCESSING_FLOW_FACADE_INTERFACE,\n"\
                    "                                         public FLOW_FACADE_ABSTRACT_CLASS \n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       PROCESSING_FLOW_FACADE_CLASS();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~PROCESSING_FLOW_FACADE_CLASS();\n")
            f.write("    public:\n")

            for fn in self.functions:
                name = fn.get_function_name()
                if "_initialize" in name:
                    continue
                if "_terminate" in name:
                    continue
                if "_get_status" in name:
                    continue
                if "_change_to_work_mode" in name:
                    continue
                if "_change_to_debug_mode" in name:
                    continue
                if "_download_machine_constants" in name:
                    continue
                if "_get_driver_state" in name:
                    continue
                name.replace(self.comp + "4A","")
                full_name = fn.get_function()
                flow_name = full_name.replace("ZOO_EXPORT","")
                flow_name = flow_name.replace("ZOO_INT32 "+ self.comp + "4A_","ZOO_INT32 ")
                if 'Sync' in fn.get_interface_type() :
                    f.write("        /*\n")
                    f_name = fn.get_function_name()
                    prefix = self.comp + "4A_"
                    f_name = f_name.replace(prefix,"").replace("_"," ").capitalize()
                    f.write("         * @brief " + f_name + "\n")
                    for p in fn.get_input_parameters_list():
                        f.write("         * @param "+ p.get_name() + "\n")
                    for p in fn.get_output_parameters_list():
                        f.write("         * @param "+ p.get_name() + "\n")
                    for p in fn.get_inoutput_parameters_list():
                        f.write("         * @param "+ p.get_name() + "\n")
                    f.write("        **/\n")
                    f.write("        " + flow_name + "\n\n")

            f.write("       /*\n")
            f.write("        * @brief This method is executed when property changed value\n")
            f.write("        * @param model             The model type\n")
            f.write("        * @param property_name     The property has been changed value\n")
            f.write("       **/ \n")
            f.write("       OVERRIDE\n")
            f.write("       void on_property_changed(CONTROLLER_INTERFACE * model,const ZOO_UINT32 property_name);\n\n")

            f.write("    };\n")
            f.write("}//namespace " + self.comp + "\n\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_cpp.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \"PROCESSING_FLOW_FACADE_CLASS.h\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    PROCESSING_FLOW_FACADE_CLASS::PROCESSING_FLOW_FACADE_CLASS()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    PROCESSING_FLOW_FACADE_CLASS::~PROCESSING_FLOW_FACADE_CLASS()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            for fn in self.functions:
                name = fn.get_function_name()
                if "_initialize" in name:
                    continue
                if "_terminate" in name:
                    continue
                if "_get_status" in name:
                    continue
                if "_change_to_work_mode" in name:
                    continue
                if "_change_to_debug_mode" in name:
                    continue
                if "_download_machine_constants" in name:
                    continue
                if "_get_driver_state" in name:
                    continue
                name.replace(self.comp + "4A", "")
                full_name = fn.get_function()
                flow_name = full_name.replace("ZOO_EXPORT", "")
                flow_name = flow_name.replace("ZOO_INT32 " + self.comp + "4A_", "ZOO_INT32 PROCESSING_FLOW_FACADE_CLASS::")
                flow_name = flow_name.replace(";","")
                if 'Sync' in fn.get_interface_type():
                    f.write("    /*\n")
                    f_name = fn.get_function_name()
                    prefix = self.comp + "4A_"
                    f_name = f_name.replace(prefix, "").replace("_"," ").capitalize()
                    f.write("     * @brief " + f_name + "\n")
                    for p in fn.get_input_parameters_list():
                        f.write("     * @param "+ p.get_name() + "\n")
                    for p in fn.get_output_parameters_list():
                        f.write("     * @param "+ p.get_name() + "\n")
                    for p in fn.get_inoutput_parameters_list():
                        f.write("     * @param "+ p.get_name() + "\n")
                    f.write("    **/\n")
                    f.write("   " + flow_name + "\n")
                    f.write("    {\n")
                    f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
                    f.write("        ZOO_INT32 error_code = OK;\n")
                    f.write("        "+ self._try + "\n")
                    f.write("        {\n")
                    f.write("           /*\n")
                    f.write("            * @step1 : check state is valid to do\n")
                    f.write("           **/\n")
                    f.write("           this->check_driver_state_is(2,ZOO_DRIVER_STATE_BUSY,ZOO_DRIVER_STATE_IDLE);\n\n")

                    f.write("           /*\n")
                    f.write("            * @step2 : TODO: ..\n")
                    f.write("           **/\n")

                    f.write("        }\n")
                    f.write("        "+ self._catch_all + "\n")
                    f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
                    f.write("        return error_code;\n")
                    f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief This method is executed when property changed value\n")
            f.write("     * @param model             The model type\n")
            f.write("     * @param property_name     The property has been changed value\n")
            f.write("    **/ \n")
            f.write("    void PROCESSING_FLOW_FACADE_CLASS::on_property_changed(CONTROLLER_INTERFACE * model,const ZOO_UINT32 property_name)\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("         //TODO: ...\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("    }\n\n")
            f.write("} //namespace " + self.comp + "\n\n")

class COMMON_FLOW_FACADE_CLASS(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h_interface = dir + '/'  + "COMMON_FLOW_FACADE_INTERFACE.h"
        self.file_h = dir + '/'  + "COMMON_FLOW_FACADE_CLASS.h"
        self.file_cpp = dir + '/' + "COMMON_FLOW_FACADE_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,'COMMON_FLOW_FACADE_CLASS.h')
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO',comp,'COMMON_FLOW_FACADE_CLASS.cpp')
        self._file_name =  "COMMON_FLOW_FACADE_CLASS.h"
        self._file_name_interface = "COMMON_FLOW_FACADE_INTERFACE.h"
        self._try = "__" + comp + "_TRY"
        self._catch_all = "__" + comp + "_CATCH_ALL(error_code)"
        self._illegal_call_err = comp + "4A_ILLEGAL_CALL_ERR"

    def generate_h(self):
        with open(self.file_h_interface, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name_interface))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("    #include <ZOO_tc.h>\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("}\n")
            f.write("#include <boost/shared_ptr.hpp>\n")
            f.write("#include \"" +self.comp + "_COMMON_MACRO_DEFINE.h\"\n")
            f.write("#include \"FLOW_FACADE_INTERFACE.h\"\n\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class COMMON_FLOW_FACADE_INTERFACE : public virtual FLOW_FACADE_INTERFACE\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       COMMON_FLOW_FACADE_INTERFACE(){}\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~COMMON_FLOW_FACADE_INTERFACE(){}\n")
            f.write("    public:\n")

            f.write("       /*\n")
            f.write("        * @brief Initialize the model\n")
            f.write("        * @return error_code \n")
            f.write("       **/ \n")
            f.write("       virtual ZOO_INT32 initialize() = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Terminate the model\n")
            f.write("        * @return error_code \n")
            f.write("       **/ \n")
            f.write("       virtual ZOO_INT32 terminate() = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Get driver state\n")
            f.write("        * @return state \n")
            f.write("       **/ \n")
            f.write("       virtual ZOO_DRIVER_STATE_ENUM get_driver_state() = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Get driver state\n")
            f.write("        * @return state \n")
            f.write("       **/ \n")
            f.write("       virtual void get_driver_state(INOUT ZOO_DRIVER_STATE_ENUM * state) = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Get device status.\n")
            f.write("        * @return error code \n")
            f.write("       **/ \n")
            f.write("       virtual ZOO_INT32 get_status(INOUT "+ self.comp+"4A_STATUS_STRUCT * status) = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Change to debug mode\n")
            f.write("       **/ \n")
            f.write("       virtual ZOO_INT32 change_to_debug_mode() = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Change to work mode\n")
            f.write("       **/ \n")
            f.write("       virtual ZOO_INT32 change_to_work_mode() = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Change to work mode\n")
            f.write("       **/ \n")
            f.write("       virtual ZOO_INT32 download_machine_constants() = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Subscribe events published from hardware drivers\n")
            f.write("       **/ \n")
            f.write("       virtual void subscribe_driver_events() = 0;\n\n")
            f.write("    };\n")
            f.write("}// namespace " + self.comp + "\n\n")
            f.write("#endif\n")

        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("#include \"COMMON_FLOW_FACADE_INTERFACE.h\"\n")
            f.write("#include \"FLOW_FACADE_ABSTRACT_CLASS.h\"\n\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class COMMON_FLOW_FACADE_CLASS : public virtual COMMON_FLOW_FACADE_INTERFACE,\n"\
                    "                                         public FLOW_FACADE_ABSTRACT_CLASS \n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       COMMON_FLOW_FACADE_CLASS();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~COMMON_FLOW_FACADE_CLASS();\n")
            f.write("    public:\n")

            f.write("       /*\n")
            f.write("        * @brief Initialize the model\n")
            f.write("        * @return error_code \n")
            f.write("       **/ \n")
            f.write("       ZOO_INT32 initialize();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Terminate the model\n")
            f.write("        * @return error_code \n")
            f.write("       **/ \n")
            f.write("       ZOO_INT32 terminate();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Get driver state\n")
            f.write("        * @return state \n")
            f.write("       **/ \n")
            f.write("       ZOO_DRIVER_STATE_ENUM get_driver_state();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Get driver state\n")
            f.write("        * @return state \n")
            f.write("       **/ \n")
            f.write("       void get_driver_state(INOUT ZOO_DRIVER_STATE_ENUM * state);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Get device status.\n")
            f.write("        * @return error code \n")
            f.write("       **/ \n")
            f.write("       ZOO_INT32 get_status(INOUT "+ self.comp+"4A_STATUS_STRUCT * status);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Change to debug mode\n")
            f.write("       **/ \n")
            f.write("       ZOO_INT32 change_to_debug_mode();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Change to work mode.The driver state is BUSY.\n")
            f.write("       **/ \n")
            f.write("       ZOO_INT32 change_to_work_mode();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Download mc\n")
            f.write("       **/ \n")
            f.write("       ZOO_INT32 download_machine_constants();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Subscribe events published from hardware drivers\n")
            f.write("       **/ \n")
            f.write("       void subscribe_driver_events();\n\n")

            f.write("       /*\n")
            f.write("        * @brief This method is executed when property changed value\n")
            f.write("        * @param model             The model type\n")
            f.write("        * @param property_name     The property has been changed value\n")
            f.write("       **/ \n")
            f.write("       OVERRIDE\n")
            f.write("       void on_property_changed(CONTROLLER_INTERFACE * model,const ZOO_UINT32 property_name);\n\n")

            f.write("    };\n")
            f.write("}//namespace " + self.comp + "\n\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_cpp.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \"COMMON_FLOW_FACADE_CLASS.h\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    COMMON_FLOW_FACADE_CLASS::COMMON_FLOW_FACADE_CLASS()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Destructor\n")
            f.write("    **/ \n")
            f.write("    COMMON_FLOW_FACADE_CLASS::~COMMON_FLOW_FACADE_CLASS()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Initialize the model,and switch the state to IDLE\n")
            f.write("     * @return error_code \n")
            f.write("    **/ \n")
            f.write("    ZOO_INT32 COMMON_FLOW_FACADE_CLASS::initialize()\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        ZOO_INT32 error_code = OK;\n")
            f.write("       "+ self._try + "\n")
            f.write("       {\n")
            f.write("           this->m_device_controller->initialize();\n")
            f.write("           this->m_state_manager->set_driver_state(ZOO_DRIVER_STATE_IDLE);\n")
            f.write("       }\n")
            f.write("       "+ self._catch_all + "\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("       return error_code;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Terminate the model,and switch the state to TERMINATE\n")
            f.write("     * @return error_code \n")
            f.write("    **/ \n")
            f.write("    ZOO_INT32 COMMON_FLOW_FACADE_CLASS::terminate()\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        ZOO_INT32 error_code = OK;\n")
            f.write("       "+ self._try + "\n")
            f.write("       {\n")
            f.write("           this->m_device_controller->terminate();\n")
            f.write("           this->m_state_manager->set_driver_state(ZOO_DRIVER_STATE_TERMINATED);\n")
            f.write("       }\n")
            f.write("       "+ self._catch_all + "\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("       return error_code;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Get driver state\n")
            f.write("     * @return state \n")
            f.write("    **/ \n")
            f.write("    ZOO_DRIVER_STATE_ENUM COMMON_FLOW_FACADE_CLASS::get_driver_state()\n")
            f.write("    {\n")
            f.write("        return this->m_state_manager->get_driver_state();\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Get driver state\n")
            f.write("     * @return state \n")
            f.write("    **/ \n")
            f.write("    void COMMON_FLOW_FACADE_CLASS::get_driver_state(INOUT ZOO_DRIVER_STATE_ENUM * state)\n")
            f.write("    {\n")
            f.write("        *state = this->m_state_manager->get_driver_state();\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Get device status.\n")
            f.write("     * @return error code \n")
            f.write("    **/ \n")
            f.write("    ZOO_INT32 COMMON_FLOW_FACADE_CLASS::get_status(INOUT " + self.comp + "4A_STATUS_STRUCT * status)\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        ZOO_INT32 error_code = OK;\n")
            f.write("       "+ self._try + "\n")
            f.write("       {\n")
            f.write("           this->m_device_controller->get_status(status);\n")
            f.write("       }\n")
            f.write("       "+ self._catch_all + "\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("       return error_code;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Download mc\n")
            f.write("     **/ \n")
            f.write("    ZOO_INT32 COMMON_FLOW_FACADE_CLASS::download_machine_constants()\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        ZOO_INT32 error_code = OK;\n")
            f.write("       "+ self._try + "\n")
            f.write("       {\n")
            f.write("           this->m_device_controller->download_mc();\n")
            f.write("       }\n")
            f.write("       "+ self._catch_all + "\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("       return error_code;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Change to debug mode\n")
            f.write("    **/ \n")
            f.write("    ZOO_INT32 COMMON_FLOW_FACADE_CLASS::change_to_debug_mode()\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        auto current_stae = this->m_state_manager->get_driver_state();\n")
            f.write("        if(current_stae == ZOO_DRIVER_STATE_BUSY)\n")
            f.write("        {\n")
            f.write("           this->m_state_manager->set_driver_state(ZOO_DRIVER_STATE_TERMINATED);\n")
            f.write("           return OK;\n")
            f.write("        }\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("        return "+self._illegal_call_err +";\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Change to work mode\n")
            f.write("    **/ \n")
            f.write("    ZOO_INT32 COMMON_FLOW_FACADE_CLASS::change_to_work_mode()\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        auto current_stae = this->m_state_manager->get_driver_state();\n")
            f.write("        if(current_stae == ZOO_DRIVER_STATE_IDLE)\n")
            f.write("        {\n")
            f.write("           this->m_state_manager->set_driver_state(ZOO_DRIVER_STATE_BUSY);\n")
            f.write("           return OK;\n")
            f.write("        }\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("        return "+self._illegal_call_err +";\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Subscribe events published from hardware drivers\n")
            f.write("    **/ \n")
            f.write("    void COMMON_FLOW_FACADE_CLASS::subscribe_driver_events()\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        this->m_device_controller->subscribe_all_devices();\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief This method is executed when property changed value\n")
            f.write("     * @param model             The model type\n")
            f.write("     * @param property_name     The property has been changed value\n")
            f.write("    **/ \n")
            f.write("    void COMMON_FLOW_FACADE_CLASS::on_property_changed(CONTROLLER_INTERFACE * model,const ZOO_UINT32 property_name)\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        //TODO: ...\n\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("    }\n\n")

            f.write("} //namespace " + self.comp + "\n\n")

class CONTROLLER_ABSTRACT_CLASS(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  + "CONTROLLER_ABSTRACT_CLASS.h"
        self.file_cpp = dir + '/' + "CONTROLLER_ABSTRACT_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,'CONTROLLER_ABSTRACT_CLASS.h')
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO',comp,'CONTROLLER_ABSTRACT_CLASS.cpp')
        self._file_name =  "CONTROLLER_ABSTRACT_CLASS.h"

    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("}\n")
            f.write("#include \"" +self.comp + "_COMMON_MACRO_DEFINE.h\"\n")
            f.write("#include \"CONTROLLER_INTERFACE.h\"\n")
            f.write("#include <boost/shared_ptr.hpp>\n\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    class CONTROLLER_ABSTRACT_CLASS : public virtual CONTROLLER_INTERFACE\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       CONTROLLER_ABSTRACT_CLASS();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~CONTROLLER_ABSTRACT_CLASS();\n")
            f.write("    public:\n")

            f.write("       /*\n")
            f.write("        * @brief Get the event_publisher attribute value\n")
            f.write("       **/ \n")
            f.write("       boost::shared_ptr<EVENT_PUBLISHER_CLASS> get_event_publisher();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Set the event_publisher attribute value\n")
            f.write("        * @param event_publisher    The new event_publisher attribute value\n")
            f.write("       **/ \n")
            f.write("       void set_event_publisher(IN boost::shared_ptr<EVENT_PUBLISHER_CLASS> event_publisher);\n\n")

            f.write("       /*\n")
            f.write("        * @brief brief Add observer will be notified when property changed\n")
            f.write("        * @param observer  Property changed observer\n")
            f.write("       **/ \n")
            f.write("       void add_observer(IN PROPERTY_CHANGED_OBSERVER_INTERFACE<CONTROLLER_INTERFACE>* observer);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Add observer will be notified when property changed\n")
            f.write("        * @param observer  Property changed observer\n")
            f.write("       **/ \n")
            f.write("       void remove_observer(IN PROPERTY_CHANGED_OBSERVER_INTERFACE<CONTROLLER_INTERFACE>* observer);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Clean\n")
            f.write("       **/ \n")
            f.write("       void clean();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Notify property has been changed\n")
            f.write("        * @property_name     The property has been changed\n")
            f.write("       **/ \n")
            f.write("       void notify_of_property_changed(IN const ZOO_UINT32 property_name);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Get status.\n")
            f.write("       **/ \n")
            f.write("       void get_status(INOUT " + self.comp +"4A_STATUS_STRUCT * status);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Set status.\n")
            f.write("       **/ \n")
            f.write("       void set_status(IN " + self.comp + "4A_STATUS_STRUCT * status);\n\n")

            f.write("    protected:\n")
            f.write("       /*\n")
            f.write("        * @brief The event_publisher attribute\n")
            f.write("       **/ \n")
            f.write("       boost::shared_ptr<EVENT_PUBLISHER_CLASS> m_event_publisher;\n\n")

            f.write("       /*\n")
            f.write("        * @brief The status of models.\n")
            f.write("       **/ \n")
            f.write("       " + self.comp +"4A_STATUS_STRUCT * m_status;\n\n")

            f.write("    private:\n")
            f.write("       /*\n")
            f.write("        * @brief The list of observer instances will be notified when property has been changed\n")
            f.write("       **/ \n")
            f.write("       std::vector<PROPERTY_CHANGED_OBSERVER_INTERFACE<CONTROLLER_INTERFACE>*> m_observers;\n\n")
            f.write("    };\n")
            f.write("}// namespace " + self.comp + "\n\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_cpp.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \"CONTROLLER_ABSTRACT_CLASS.h\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    CONTROLLER_ABSTRACT_CLASS::CONTROLLER_ABSTRACT_CLASS()\n")
            f.write("    {\n")
            f.write("       this->m_status = new " + self.comp +"4A_STATUS_STRUCT();\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    CONTROLLER_ABSTRACT_CLASS::~CONTROLLER_ABSTRACT_CLASS()\n")
            f.write("    {\n")
            f.write("        SAFTY_DELETE_POINTER(this->m_status);\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Get the event_publisher attribute value\n")
            f.write("    **/ \n")
            f.write("    boost::shared_ptr<EVENT_PUBLISHER_CLASS> CONTROLLER_ABSTRACT_CLASS::get_event_publisher()\n")
            f.write("    {\n")
            f.write("        return this->m_event_publisher;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Set the event_publisher attribute value\n")
            f.write("     * @param event_publisher    The new event_publisher attribute value\n")
            f.write("    **/ \n")
            f.write("    void CONTROLLER_ABSTRACT_CLASS::set_event_publisher(IN boost::shared_ptr<EVENT_PUBLISHER_CLASS> event_publisher)\n")
            f.write("    {\n")
            f.write("        this->m_event_publisher = event_publisher;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("      * @brief brief Add observer will be notified when property changed\n")
            f.write("      * @param observer  Property changed observer\n")
            f.write("    **/ \n")
            f.write("    void CONTROLLER_ABSTRACT_CLASS::add_observer(IN PROPERTY_CHANGED_OBSERVER_INTERFACE<CONTROLLER_INTERFACE>* observer)\n")
            f.write("    {\n")
            f.write("        this->m_observers.push_back(observer);\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("      * @brief Add observer will be notified when property changed\n")
            f.write("      * @param observer  Property changed observer\n")
            f.write("    **/ \n")
            f.write("    void CONTROLLER_ABSTRACT_CLASS::remove_observer(IN  PROPERTY_CHANGED_OBSERVER_INTERFACE<CONTROLLER_INTERFACE>* observer)\n")
            f.write("    {\n")
            f.write("        // TODO: implement clean up later\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Clean.\n")
            f.write("    **/ \n")
            f.write("    void CONTROLLER_ABSTRACT_CLASS::clean()\n")
            f.write("    {\n")
            f.write("        // TODO: implement clean up later\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief This method is executed when property changed value\n")
            f.write("     * @param model The source object contains property changed\n")
            f.write("     * @param property_name The property has been changed value\n")
            f.write("    **/ \n")
            f.write("    void CONTROLLER_ABSTRACT_CLASS::notify_of_property_changed(IN const ZOO_UINT32 property_name)\n")
            f.write("    {\n")
            f.write("        std::vector<PROPERTY_CHANGED_OBSERVER_INTERFACE<CONTROLLER_INTERFACE>*>::iterator observer_itr =\n")
            f.write("            this->m_observers.begin();\n")
            f.write("        while (observer_itr != this->m_observers.end())\n")
            f.write("        {\n")
            f.write("            PROPERTY_CHANGED_OBSERVER_INTERFACE<CONTROLLER_INTERFACE>* observer = *observer_itr;;\n")
            f.write("            observer->on_property_changed(this, property_name);\n")
            f.write("            observer_itr ++;\n")
            f.write("        }\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Get status.\n")
            f.write("    **/ \n")
            f.write("    void  CONTROLLER_ABSTRACT_CLASS::get_status(" + self.comp +"4A_STATUS_STRUCT * status)\n")
            f.write("    {\n")
            f.write("        memcpy(status,this->m_status,sizeof(" + self.comp +"4A_STATUS_STRUCT));\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Set status.\n")
            f.write("    **/ \n")
            f.write("    void CONTROLLER_ABSTRACT_CLASS::set_status(" + self.comp + "4A_STATUS_STRUCT * status)\n")
            f.write("    {\n")
            f.write("        memcpy(this->m_status,status,sizeof(" + self.comp +"4A_STATUS_STRUCT));\n")
            f.write("    }\n\n")

            f.write("} //namespace " + self.comp + "\n\n")


class DEVICE_CONTROLLER_CLASS(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h_interface = dir + '/'+ "DEVICE_CONTROLLER_INTERFACE.h"
        self.controller_interface_h = dir + '/'+ "CONTROLLER_INTERFACE.h"
        self.file_h = dir + '/'  +  "DEVICE_CONTROLLER_CLASS.h"
        self.file_cpp = dir + '/' + "DEVICE_CONTROLLER_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,"DEVICE_CONTROLLER_CLASS.h")
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO',comp,"DEVICE_CONTROLLER_CLASS.cpp")
        self._file_name =  "DEVICE_CONTROLLER_CLASS.h"
        self._class_name = "DEVICE_CONTROLLER_CLASS"
        self._class_interface = "DEVICE_CONTROLLER_INTERFACE"
        self._controller_interface = "CONTROLLER_INTERFACE"
        self._controller_interface_file = "CONTROLLER_INTERFACE.h"
        self._file_name_interface = "DEVICE_CONTROLLER_INTERFACE.h"
        self._func_init = "initialize()"
        self._create_model = "create_models(IN ZOO_INT32 type)"
        self._device_interface = comp + "_MODEL_INTERFACE"
        self._NOTIFY_PROPERTY_CHANGED_INTERFACE = "NOTIFY_PROPERTY_CHANGED_INTERFACE"
        self._PROPERTY_CHANGED_OBSERVER_INTERFACE = "PROPERTY_CHANGED_OBSERVER_INTERFACE"

    def generate_h(self):

        with open(self.controller_interface_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._controller_interface_file))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("}\n")
            f.write("#include <boost/shared_ptr.hpp>\n")
            f.write("#include \"MARKING_MODEL_INTERFACE.hpp\"\n")
            f.write("#include \"ENUM_CONVERTER_CLASS.h\"\n")
            f.write("#include \"EVENT_PUBLISHER_CLASS.h\"\n\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    class " + self._controller_interface +": public virtual PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>\n")
            f.write("                                             ,public virtual NOTIFY_PROPERTY_CHANGED_INTERFACE<CONTROLLER_INTERFACE>\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       " + self._controller_interface + "(){}\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~" + self._controller_interface + "(){}\n")
            f.write("    public:\n")

            f.write("       /*\n")
            f.write("        * @brief Get the event_publisher attribute value\n")
            f.write("       **/ \n")
            f.write("       virtual boost::shared_ptr<EVENT_PUBLISHER_CLASS> get_event_publisher() = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Set the event_publisher attribute value\n")
            f.write("        * @param event_publisher  The new event_publisher attribute value \n")
            f.write("       **/ \n")
            f.write("       virtual void set_event_publisher(boost::shared_ptr<EVENT_PUBLISHER_CLASS> event_publisher) = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Subscribe events for all devices\n")
            f.write("       **/ \n")
            f.write("       virtual void subscribe_all_devices() = 0;\n\n")

            f.write("    };\n")
            f.write("}// namespace " + self.comp + "\n\n")
            f.write("#endif\n")

        with open(self.file_h_interface, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name_interface))
            f.write("\n")
            f.write("#include \"" +self.comp + "_COMMON_MACRO_DEFINE.h\"\n")
            f.write("#include \"" +self.comp + "_MODEL_INTERFACE.h\"\n")
            f.write("#include \"CONTROLLER_INTERFACE.h\"\n")
            f.write("#include <map>\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class " + self._class_interface + ": public virtual CONTROLLER_INTERFACE"+"\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       "+self._class_interface +"(){}\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~"+self._class_interface +"(){}\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Initialize the model\n")
            f.write("        * @return throw exception \n")
            f.write("       **/ \n")
            f.write("       virtual void initialize() = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Terminate the model\n")
            f.write("        * @return throw exception \n")
            f.write("       **/ \n")
            f.write("       virtual void terminate() = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Change to work mode\n")
            f.write("       **/ \n")
            f.write("       virtual void download_mc() = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Change to work mode\n")
            f.write("       **/ \n")
            f.write("       virtual void get_status(INOUT " + self.comp + "4A_STATUS_STRUCT * status) = 0;\n\n")
            f.write("    };\n")
            f.write("} // namespace " + self.comp + "\n\n")
            f.write("#endif\n")

        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("#include \"CONTROLLER_ABSTRACT_CLASS.h\"\n")
            f.write("#include \"DEVICE_CONTROLLER_INTERFACE.h\"\n\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class "+self._class_name +": public virtual CONTROLLER_ABSTRACT_CLASS, public virtual "+self._class_interface +"\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       "+self._class_name +"();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~"+self._class_name +"();\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Initialize the model\n")
            f.write("        * @return throw exception \n")
            f.write("       **/ \n")
            f.write("       void initialize();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Terminate the model\n")
            f.write("        * @return throw exception \n")
            f.write("       **/ \n")
            f.write("       void terminate();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Change to work mode\n")
            f.write("       **/ \n")
            f.write("       void download_mc();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Subscribe events for all devices\n")
            f.write("       **/ \n")
            f.write("       void subscribe_all_devices();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Change to work mode\n")
            f.write("       **/ \n")
            f.write("       void get_status(INOUT " + self.comp + "4A_STATUS_STRUCT * status);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Create all models by configurations.\n")
            f.write("       **/ \n")
            f.write("       void create_all_models();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Notify property has been changed\n")
            f.write("        * @property_name     The property has been changed\n")
            f.write("       **/ \n")
            f.write("       OVERRIDE\n")
            f.write("       void on_property_changed(MARKING_MODEL_INTERFACE* model,const ZOO_UINT32 property_name);\n\n")

            f.write("    private:\n")
            f.write("       /*\n")
            f.write("        * @brief Create one model by the given type. and insert into m_entity_devices container\n")
            f.write("       **/ \n")
            f.write("       void create_model_by_type(IN ZOO_INT32 type);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Load device from config database or file\n")
            f.write("       **/ \n")
            f.write("       void load_devices_from_db();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Listen device model's property changes\n")
            f.write("       **/ \n")
            f.write("       void listen_model_property_change();\n\n")

            f.write("    private:\n")
            f.write("       /*\n")
            f.write("        * @brief Define device entities.\n")
            f.write("       **/ \n")
            f.write("       std::map<ZOO_INT32,boost::shared_ptr<"+self._device_interface+"> > m_entity_devices;\n\n")
            f.write("       /*\n")
            f.write("        * @brief Define device entities.\n")
            f.write("       **/ \n")
            f.write("       std::map<ZOO_INT32,boost::shared_ptr<"+self._device_interface+"> > m_enabled_devices;\n")
            f.write("    };\n")
            f.write("} //namespace " + self.comp + "\n\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_cpp.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \""+self._class_name +".h\"\n\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    "+self._class_name +"::"+self._class_name +"()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Destructor\n")
            f.write("    **/ \n")
            f.write("    "+self._class_name +"::~"+self._class_name +"()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Initialize the model\n")
            f.write("     * @return throw exception \n")
            f.write("    **/ \n")
            f.write("    void "+self._class_name +"::initialize()\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        this->load_devices_from_db();\n\n")
            f.write("        this->create_all_models();\n\n")
            f.write("        this->listen_model_property_change();\n\n")
            f.write("        std::for_each(this->m_entity_devices.begin(),this->m_entity_devices.end(),[&](auto & device)\n")
            f.write("        {\n")
            f.write("            auto model = device.second;\n")
            f.write("            if(model)\n")
            f.write("            {\n")
            f.write("                 model->initialize();\n")
            f.write("            }\n")
            f.write("        });\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Terminate the model\n")
            f.write("     * @return throw exception \n")
            f.write("    **/ \n")
            f.write("    void "+self._class_name +"::terminate()\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        std::for_each(this->m_entity_devices.begin(),this->m_entity_devices.end(),[&](auto & device)\n")
            f.write("        {\n")
            f.write("            auto model = device.second;\n")
            f.write("            if(model)\n")
            f.write("            {\n")
            f.write("                 model->terminate();\n")
            f.write("            }\n")
            f.write("        });\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Change to work mode\n")
            f.write("    **/ \n")
            f.write("    void "+self._class_name +"::download_mc()\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        std::for_each(this->m_entity_devices.begin(),this->m_entity_devices.end(),[&](auto & device)\n")
            f.write("        {\n")
            f.write("            auto model = device.second;\n")
            f.write("            if(model)\n")
            f.write("            {\n")
            f.write("                 model->download_mc();\n")
            f.write("            }\n")
            f.write("        });\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Subscribe events for all devices\n")
            f.write("    **/ \n")
            f.write("    void "+self._class_name +"::subscribe_all_devices()\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        std::for_each(this->m_entity_devices.begin(),this->m_entity_devices.end(),[&](auto & device)\n")
            f.write("        {\n")
            f.write("            auto model = device.second;\n")
            f.write("            if(model)\n")
            f.write("            {\n")
            f.write("                 //model->download_mc();\n")
            f.write("            }\n")
            f.write("        });\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Change to work mode\n")
            f.write("    **/ \n")
            f.write("    void " + self._class_name + "::get_status("+self.comp+"4A_STATUS_STRUCT * status)\n")
            f.write("    {\n")
            f.write("        this->CONTROLLER_ABSTRACT_CLASS::get_status(status);\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Create all models\n")
            f.write("    **/ \n")
            f.write("    void "+self._class_name +"::create_all_models()\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        //example : this->create_model_by_type(device type enum : XX4A_DEVICE_ID_1 ).\n")
            f.write("        //example : this->create_model_by_type(device type enum : XX4A_DEVICE_ID_2 ).\n")
            f.write("        //example : ...\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Notify property has been changed\n")
            f.write("     * @property_name     The property has been changed\n")
            f.write("    **/ \n")
            f.write("    void "+self._class_name +"::on_property_changed(MARKING_MODEL_INTERFACE* model,const ZOO_UINT32 property_name)\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        //example : ...\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Load device from config database or file.\n")
            f.write("     **/ \n")
            f.write("    void "+self._class_name +"::load_devices_from_db()\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        //TODO: \n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Create one model by the given type.\n")
            f.write("     **/ \n")
            f.write("    void "+self._class_name +"::create_model_by_type(IN ZOO_INT32 type)\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        //create device model and insert into m_entity_devices container.\n")
            f.write("        //TODO: \n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Create one model by the given type.\n")
            f.write("     **/ \n")
            f.write("    void " + self._class_name + "::listen_model_property_change()\n")
            f.write("    {\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"> function entry ...\");\n")
            f.write("        std::map<ZOO_INT32, boost::shared_ptr<"+self._device_interface+"> >::iterator device_itr =\n")
            f.write("           this->m_enabled_devices.begin();\n")
            f.write("        while (device_itr != this->m_enabled_devices.end())\n")
            f.write("        {\n")
            f.write("            boost::shared_ptr<"+self._device_interface+"> device_model = device_itr->second;\n")
            f.write("            device_model->clean();\n")
            f.write("            device_model->add_observer(this);\n")
            f.write("            device_itr++;\n")
            f.write("        }\n")
            f.write("        __ZOO_TRACE(" + self.comp + "4I_COMPONET_ID,\"< function exit ...\");\n")
            f.write("    }\n\n")

            f.write("} //namespace " + self.comp + "\n\n")

class DEVICE_MODEL_ABSTRACT_CLASS(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  +  "DEVICE_MODEL_ABSTRACT_CLASS.h"
        self.file_cpp = dir + '/' + "DEVICE_MODEL_ABSTRACT_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,"DEVICE_MODEL_ABSTRACT_CLASS.h")
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO',comp,"DEVICE_MODEL_ABSTRACT_CLASS.cpp")
        self._file_name = "DEVICE_MODEL_ABSTRACT_CLASS.h"
        self._class_name = "DEVICE_MODEL_ABSTRACT_CLASS"

    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("}\n")
            f.write("#include \"" + self.comp + "_COMMON_MACRO_DEFINE.h\"\n")
            f.write("#include \"" + self._file_name+"\"\n")
            f.write("#include \"DEVICE_INTERFACE.h\"\n")
            f.write("#include <boost/shared_ptr.hpp>\n\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class DEVICE_MODEL_ABSTRACT_CLASS : public virtual DEVICE_INTERFACE\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       "+self._class_name +"(){}\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~"+self._class_name +"(){}\n")
            f.write("    public:\n")
            f.write("    };\n")
            f.write("}// namespace " + self.comp + "\n\n")
            f.write("#endif\n")

class DEVICE_MODEL_CLASS(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h_interface = dir + '/' + comp  + "_MODEL_INTERFACE.h"
        self.file_h = dir + '/'  + comp + "_MODEL_CLASS.h"
        self.file_cpp = dir + '/' + comp + "_MODEL_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,comp + "_MODEL_CLASS.h")
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO',comp,comp + "_MODEL_CLASS.cpp")
        self._file_name =  comp + "_MODEL_CLASS.h"
        self._class_name = comp + "_MODEL_CLASS"
        self._class_interface = comp + "_MODEL_INTERFACE"
        self._func_init = "initialize()"
        self._file_name_interface = comp + "_MODEL_INTERFACE.h"
        self._hardware_service_class = comp  + "_HARDWARE_SERVICE_CLASS"
        self._hardware_service_interface = comp  + "_HARDWARE_SERVICE_INTERFACE"
        self._HARDWARE_MOCKER_CLASS = comp  + "_HARDWARE_MOCKER_CLASS"

    def generate_h(self):
        with open(self.file_h_interface, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name_interface))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("}\n")
            f.write("#include \"" + self.comp + "_COMMON_MACRO_DEFINE.h\"\n")
            f.write("#include \"" + self._file_name_interface+"\"\n")
            f.write("#include \"DEVICE_INTERFACE.h\"\n")
            f.write("#include \"STATE_MANAGER_CLASS.h\"\n")
            f.write("#include <boost/shared_ptr.hpp>\n\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class "+self._class_interface +": public virtual DEVICE_INTERFACE\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       "+self._class_interface +"(){}\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~"+self._class_interface +"(){}\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Initialize the model.\n")
            f.write("       **/ \n")
            f.write("       virtual void initialize() = 0;\n")

            f.write("       /*\n")
            f.write("        * @brief Terminate the model.\n")
            f.write("       **/ \n")
            f.write("       virtual void terminate() = 0;\n")

            f.write("       /*\n")
            f.write("        * @brief Terminate the model.\n")
            f.write("       **/ \n")
            f.write("       virtual void download_mc() = 0;\n")

            f.write("    };\n")
            f.write("}// namespace " + self.comp + "\n\n")
            f.write("#endif\n")

        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("#include \""+self._file_name_interface+"\"\n")
            f.write("#include \"DEVICE_MODEL_ABSTRCT_CLASS.h\"\n")
            f.write("#include \""+self._hardware_service_interface+".h\"\n")
            f.write("#include \""+self._HARDWARE_MOCKER_CLASS+".h\"\n\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class "+self._class_name +" : public virtual "+self._class_interface +",public virtual DEVICE_MODEL_ABSTRCT_CLASS\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       "+self._class_name +"();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~"+self._class_name +"();\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Initialize the model.\n")
            f.write("       **/ \n")
            f.write("       void initialize();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Terminate the model.\n")
            f.write("       **/ \n")
            f.write("       void terminate();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Terminate the model.\n")
            f.write("       **/ \n")
            f.write("       void download_mc();\n")

            f.write("       /*\n")
            f.write("        * @brief Notify property has been changed.\n")
            f.write("        * @param property_name     The property has been changed\n")
            f.write("       **/ \n")
            f.write("      OVERRIDE\n")
            f.write("      void on_property_changed(DEVICE_INTERFACE * model,const ZOO_UINT32 property_name);\n\n")

            f.write("    private:\n")
            f.write("       /*\n")
            f.write("        * @brief The model hardware service.\n")
            f.write("       **/ \n")
            f.write("       boost::shared_ptr<"+self._hardware_service_interface+"> m_hardware_service;\n\n")

            f.write("    };\n")
            f.write("} //namespace " + self.comp + "\n\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_cpp.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \""+self._class_name +".h\"\n")
            f.write("#include \""+self._hardware_service_class +".h\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    "+self._class_name +"::"+self._class_name +"()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    "+self._class_name +"::~"+self._class_name +"()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("      * @brief Initialize the model.\n")
            f.write("    **/ \n")
            f.write("    void "+self._class_name +"::initialize()\n")
            f.write("    {\n")
            f.write("        if(nullptr == this->m_hardware_service))\n")
            f.write("        {\n")
            f.write("            if(ZOO_TRUE == TR4A_check_sim_mode("+ self.comp + "4I_COMPONET_ID" + ",ZOO_SIM_DISABLE))\n")
            f.write("            {\n")
            f.write("                this->m_hardware_service.reset(new "+self._hardware_service_class+"());\n")
            f.write("            }\n")
            f.write("            else\n")
            f.write("            {\n")
            f.write("                this->m_hardware_service.reset(new "+self._HARDWARE_MOCKER_CLASS+"());\n")
            f.write("            }\n")
            f.write("        }\n")
            f.write("        this->m_hardware_service->terminate();\n")
            f.write("        this->m_hardware_service->initialize();\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Terminate the model.\n")
            f.write("    **/ \n")
            f.write("    void "+self._class_name +"::terminate()\n")
            f.write("    {\n")
            f.write("        if(nullptr != this->m_hardware_service)\n")
            f.write("            this->m_hardware_service->terminate();\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("      * @brief Terminate the model.\n")
            f.write("    **/ \n")
            f.write("    void "+self._class_name +"::download_mc()\n")
            f.write("    {\n")
            f.write("        if(nullptr != this->m_hardware_service)\n")
            f.write("            this->m_hardware_service->terminate();\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Notify property has been changed\n")
            f.write("     * @property_name     The property has been changed\n")
            f.write("    **/ \n")
            f.write("    void "+self._class_name +"::on_property_changed(DEVICE_INTERFACE* model,const ZOO_UINT32 property_name)\n")
            f.write("    {\n")
            f.write("        //example : ...\n")
            f.write("    }\n")

            f.write("}//namespace " + self.comp + "\n")

class HARDWARE_ABSTRACT_CLASS(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h_interface = dir + '/' + comp +"_HARDWARE_ABSTRACT_CLASS.h"
        self.file_h = dir + '/'  + comp +"_HARDWARE_ABSTRACT_CLASS.h"
        self.file_cpp = dir + '/'+ comp +"_HARDWARE_ABSTRACT_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,comp +"_HARDWARE_ABSTRACT_CLASS.h")
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO',comp,comp +"_HARDWARE_ABSTRACT_CLASS.cpp")
        self._file_name =  comp +"_HARDWARE_ABSTRACT_CLASS.h"
        self._class_name = comp +"_HARDWARE_ABSTRACT_CLASS"
        self._interface_class_name = comp +"_HARDWARE_SERVICE_INTERFACE"
        self._func_init = "initialize()"
        self._create_model = "create_models(IN ZOO_INT32 type)"
    def generate_h(self):
        with open(self.file_h_interface, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("}\n")
            f.write("#include \"" +self.comp + "_COMMON_MACRO_DEFINE.h\"\n")
            f.write("#include \"MARKING_MODEL_INTERFACE.hpp\"\n")
            f.write("#include \"" + self._interface_class_name + ".h\"\n")
            f.write("#include <boost/shared_ptr.hpp>\n\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class "+self._class_name +": public virtual " + self._interface_class_name + "\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       "+self._class_name +"();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~"+self._class_name +"();\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief brief Add observer will be notified when property changed\n")
            f.write("        * @param observer  Property changed observer\n")
            f.write("       **/ \n")
            f.write("       void add_observer(IN PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>* observer);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Add observer will be notified when property changed\n")
            f.write("        * @param observer  Property changed observer\n")
            f.write("       **/ \n")
            f.write("       void remove_observer(IN PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>* observer);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Clean\n")
            f.write("       **/ \n")
            f.write("       virtual void clean();\n\n")

            f.write("      /*\n")
            f.write("       * @brief This method is executed when property changed value\n")
            f.write("       * @param model The source object contains property changed\n")
            f.write("       * @param property_name The property has been changed value\n")
            f.write("       **/ \n")
            f.write( "      void notify_of_property_changed(IN const ZOO_UINT32 property_name);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Initialize the hardware.\n")
            f.write("       **/ \n")
            f.write("       virtual void initialize();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Terminate the hardware.\n")
            f.write("       **/ \n")
            f.write("       virtual void terminate();\n\n")

            f.write("    private:\n")
            f.write("       /*\n")
            f.write("        * @brief The list of observer instances will be notified when property has been changed\n")
            f.write("       **/ \n")
            f.write("       std::vector<PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>*> m_observers;\n\n")

            f.write("    };\n")
            f.write("}// namespace " + self.comp + "\n\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_cpp.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \""+self._class_name +".h\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    "+self._class_name +"::"+self._class_name +"()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    "+self._class_name +"::~"+self._class_name +"()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief brief Add observer will be notified when property changed\n")
            f.write("     * @param observer  Property changed observer\n")
            f.write("    **/ \n")
            f.write(
                "    void " + self._class_name + "::add_observer(IN PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>* observer)\n")
            f.write("    {\n")
            f.write("        this->m_observers.push_back(observer);\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Add observer will be notified when property changed\n")
            f.write("     * @param observer  Property changed observer\n")
            f.write("    **/ \n")
            f.write("    void " + self._class_name + "::remove_observer(IN PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>* observer)\n")
            f.write("    {\n")
            f.write("        // TODO: implement clean up later\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Clean.\n")
            f.write("    **/ \n")
            f.write("    void " + self._class_name + "::clean()\n")
            f.write("    {\n")
            f.write("        // TODO: implement clean up later\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief This method is executed when property changed value\n")
            f.write("     * @param model The source object contains property changed\n")
            f.write("     * @param property_name The property has been changed value\n")
            f.write("    **/ \n")
            f.write("    void " + self._class_name + "::notify_of_property_changed(IN const ZOO_UINT32 property_name)\n")
            f.write("    {\n")
            f.write("        std::vector<PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>*>::iterator observer_itr =\n")
            f.write("            this->m_observers.begin();\n")
            f.write("        while (observer_itr != this->m_observers.end())\n")
            f.write("        {\n")
            f.write("            PROPERTY_CHANGED_OBSERVER_INTERFACE<MARKING_MODEL_INTERFACE>* observer = *observer_itr;\n")
            f.write("            observer->on_property_changed(this, property_name);\n")
            f.write("            observer_itr ++;\n")
            f.write("        }\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief initialize.\n")
            f.write("    **/ \n")
            f.write("    void " + self._class_name + "::initialize()\n")
            f.write("    {\n")
            f.write("        // TODO: Implemented in an inheritance model\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief terminate.\n")
            f.write("    **/ \n")
            f.write("    void " + self._class_name + "::terminate()\n")
            f.write("    {\n")
            f.write("        // TODO: Implemented in an inheritance model\n")
            f.write("    }\n\n")

            f.write("} //namespace " + self.comp + "\n\n")

class PARAMETER_VALIDATOR_CLASS(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  +  "PARAMETER_VALIDATOR_CLASS.h"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,"PARAMETER_VALIDATOR_CLASS.h")
        self._file_name =  "PARAMETER_VALIDATOR_CLASS.h"
        self._class_name =  "PARAMETER_VALIDATOR_CLASS"
        self._func_not_null = "not(void value)"
        self._func_in = "in(double min,double max)"
        self._func_out = "out(double min,double max)"
        self._func_equal = "equal(ZOO_INT32 value)"
        self._func_less_than = "less_than(ZOO_INT32 value)"
        self._func_less_equal = "less_equal(ZOO_INT32 value)"
        self._func_more_than = "more_than(ZOO_INT32 value)"
        self._func_more_equal = "more_equal(ZOO_INT32 value)"
    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("}\n")
            f.write("#include <string>\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class " + self._class_name +"\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       " + self._class_name +"(){}\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~" + self._class_name +"(){}\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief reload mock data.\n")
            f.write("       **/ \n")
            f.write("       void (int type,int count,);\n\n")
            f.write("    };\n")
            f.write("}// namespace " + self.comp + "\n")
            f.write("#endif\n")

class XX_HARDWARE_MOCK(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h_interface = dir + '/' + comp  + "_HARDWARE_MOCKER_CLASS.h"
        self.file_h = dir + '/'  + comp + "_HARDWARE_MOCKER_CLASS.h"
        self.file_cpp = dir + '/' + comp + "_HARDWARE_MOCKER_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,comp + "_HARDWARE_MOCKER_CLASS.h")
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO',comp,comp + "_HARDWARE_MOCKER_CLASS.cpp")
        self._file_name =  comp + "_HARDWARE_MOCKER_CLASS.h"
        self._class_name = comp + "_HARDWARE_MOCKER_CLASS"
        self._func_init = "reload()"
        self._get_mock_data = "get_mock_data(IN std::string section_name)"
        self._configure_class = self.comp +"_CONFIGURE"
        self._hardware_interface = comp + "_HARDWARE_SERVICE_INTERFACE"
        self._hardware_abstract_class = comp + "_HARDWARE_ABSTRACT_CLASS"
    def generate_h(self):
        with open(self.file_h_interface, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("}\n")
            f.write("#include \"MOCK_DATA_PARSER_CLASS.h\"\n")
            f.write("#include \""+ self.comp +"_CONFIGURE.h\"\n")
            f.write("#include \""+ self._hardware_interface +".h\"\n")
            f.write("#include \""+ self._hardware_abstract_class +".h\"\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class " + self._class_name +": public virtual "+ self._hardware_interface +",public virtual "+self._hardware_abstract_class+"\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       " + self._class_name +"();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~" + self._class_name +"();\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief reload mock data.\n")
            f.write("       **/ \n")
            f.write("       void intialize();\n\n")

            f.write("       /*\n")
            f.write("        * @brief terminate the hardware mock.\n")
            f.write("       **/ \n")
            f.write("       void terminate();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Get mock data.\n")
            f.write("        * @param section_name       the section name\n")
            f.write("        * @return mock data\n")
            f.write("        **/ \n")
            f.write("       boost::shared_ptr<MOCK_DATA_CLASS> "+ self._get_mock_data +";\n")

            f.write("    private:\n")
            f.write("       /*\n")
            f.write("        * @brief Mock data map attribute.\n")
            f.write("       **/ \n")
            f.write("       std::map<std::string,boost::shared_ptr<MOCK_DATA_CLASS> > m_mock_datas;\n")
            f.write("    };\n")

            f.write("}// namespace " + self.comp + "\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_cpp.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \""+self._class_name +".h\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    "+self._class_name +"::"+self._class_name +"()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    "+self._class_name +"::~"+self._class_name +"()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief reload mock data.\n")
            f.write("    **/ \n")
            f.write("    void "+self._class_name +"::intialize()\n")
            f.write("    {\n")
            f.write("        this->m_mock_datas.clear();\n")
            f.write("        boost::shared_ptr<MOCK_DATA_PARSER_CLASS> data_parser = boost::make_shared<MOCK_DATA_PARSER_CLASS>();\n")
            f.write("        std::string mock_file = "+self._configure_class+"::get_instance()->get_mock_file();\n")
            f.write("        this->m_mock_datas = data_parser->parse_mock_data(mock_file);\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief terminate the hardware mock.\n")
            f.write("    **/ \n")
            f.write("    void "+self._class_name +"::terminate()\n")
            f.write("    {\n")
            f.write("        this->m_mock_datas.clear();\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Get mock data.\n")
            f.write("     * @param section_name       the section name\n")
            f.write("     * @return mock data\n")
            f.write("     **/ \n")
            f.write("    boost::shared_ptr<MOCK_DATA_CLASS> "+self._class_name + "::" + self._get_mock_data + "\n")
            f.write("    {\n")
            f.write("        boost::shared_ptr<MOCK_DATA_CLASS> mock_data_model;\n")
            f.write("        std::map<std::string,boost::shared_ptr<MOCK_DATA_CLASS> >::iterator ite = this->m_mock_datas.begin();\n")
            f.write("        while(ite != this->m_mock_datas.end())\n")
            f.write("        {\n")
            f.write("            if(ite->first == section_name)\n")
            f.write("            {\n")
            f.write("                mock_data_model = ite->second;\n")
            f.write("                break;\n")
            f.write("            }\n")
            f.write("            ite++;\n")
            f.write("        }\n")
            f.write("        return mock_data_model;\n")
            f.write("    }\n")
            f.write("} //namespace " + self.comp + "\n")

class XX_HARDWARE_SERVICE(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h_interface = dir + '/' + comp  + "_HARDWARE_SERVICE_INTERFACE.h"
        self.file_h = dir + '/'  + comp + "_HARDWARE_SERVICE_CLASS.h"
        self.file_cpp = dir + '/' + comp + "_HARDWARE_SERVICE_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,comp + "_HARDWARE_SERVICE_CLASS.h")
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO',comp,comp + "_HARDWARE_SERVICE_CLASS.cpp")
        self._file_name =  comp + "_HARDWARE_SERVICE_CLASS.h"
        self._class_name = comp + "_HARDWARE_SERVICE_CLASS"
        self._class_interface = comp + "_HARDWARE_SERVICE_INTERFACE"
        self._func_init = "initialize()"
        self._create_model = "create_models(IN ZOO_INT32 type)"
        self._file_name_interface = comp + "_HARDWARE_SERVICE_INTERFACE.h"

    def generate_h(self):
        with open(self.file_h_interface, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name_interface))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("    #include <" + self.comp + "4A_type.h>\n")
            f.write("}\n")
            f.write("#include \"" +self.comp + "_COMMON_MACRO_DEFINE.h\"\n")
            f.write("#include \"MARKING_MODEL_INTERFACE.hpp\"\n")
            f.write("#include <boost/shared_ptr.hpp>\n\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class "+self._class_interface +": public virtual MARKING_MODEL_INTERFACE, public virtual NOTIFY_PROPERTY_CHANGED_INTERFACE<MARKING_MODEL_INTERFACE>\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       "+self._class_interface +"(){}\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~"+self._class_interface +"(){}\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Initialize the hardware.\n")
            f.write("       **/ \n")
            f.write("       virtual void initialize() = 0;\n\n")

            f.write("       /*\n")
            f.write("        * @brief Terminate the hardware.\n")
            f.write("       **/ \n")
            f.write("       virtual void terminate() = 0;\n\n")
            f.write("    };\n")
            f.write("}// namespace " + self.comp + "\n\n")
            f.write("#endif\n")

        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("#include \""+self._file_name_interface+"\"\n")
            f.write("#include \"" + self.comp + "_HARDWARE_ABSTRACT_CLASS.h\"\n\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class "+self._class_name +" : public virtual "+self._class_interface +",public virtual " +self.comp + "_HARDWARE_ABSTRACT_CLASS \n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       "+self._class_name +"();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~"+self._class_name +"();\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Initialize the hardware.\n")
            f.write("       **/ \n")
            f.write("       void initialize();\n\n")

            f.write("       /*\n")
            f.write("        * @brief Terminate the hardware.\n")
            f.write("       **/ \n")
            f.write("       void terminate();\n\n")

            f.write("    };\n")
            f.write("} //namespace " + self.comp + "\n\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_cpp.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \""+self._class_name +".h\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    "+self._class_name +"::"+self._class_name +"()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    "+self._class_name +"::~"+self._class_name +"()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Initialize the hardware.\n")
            f.write("    **/ \n")
            f.write("    void "+self._class_name +"::initialize()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Terminate the hardware.\n")
            f.write("    **/ \n")
            f.write("    void "+self._class_name +"::terminate()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")
            
            f.write("} //namespace " + self.comp + "\n\n")

class PROPERTY_CHANGED_OBSERVER_INTERFACE(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  +  "PROPERTY_CHANGED_OBSERVER_INTERFACE.h"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,"PROPERTY_CHANGED_OBSERVER_INTERFACE.h")
        self._file_name =  "PROPERTY_CHANGED_OBSERVER_INTERFACE.h"
        self._class_name = "PROPERTY_CHANGED_OBSERVER_INTERFACE"
        self._on_property_changed = "on_property_changed(T* model,const ZOO_UINT32 property_name)"

    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("}\n")
            f.write("#include <vector>\n")
            f.write("#include <boost/any.hpp>\n")
            f.write("#include <boost/shared_ptr.hpp>\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    template <typename T>\n")
            f.write("    class "+ self._class_name +"\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       "+ self._class_name +"(){}\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~"+ self._class_name +"(){}\n")
            f.write("    public:\n")

            f.write("        /*\n")
            f.write("         * @brief This method is executed when property changed value\n")
            f.write("         * @param model             The model type\n")
            f.write("         * @param property_name     The property has been changed value\n")
            f.write("        **/\n")
            f.write("        virtual void " + self._on_property_changed + " = 0;\n")
            f.write("\n")

            f.write("    };\n")
            f.write("} //namespace " + self.comp + "\n")
            f.write("#endif\n")

class NOTIFY_PROPERTY_CHANGED_INTERFACE(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  +  "NOTIFY_PROPERTY_CHANGED_INTERFACE.h"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,"NOTIFY_PROPERTY_CHANGED_INTERFACE.h")
        self._file_name =  "NOTIFY_PROPERTY_CHANGED_INTERFACE.h"
        self._class_name = "NOTIFY_PROPERTY_CHANGED_INTERFACE"
        self.add_observer = "add_observer(PROPERTY_CHANGED_OBSERVER_INTERFACE<T>* observer)"
        self.remove_observer = "remove_observer(PROPERTY_CHANGED_OBSERVER_INTERFACE<T>* observer)"
        self.clean = "clean()"
        self.notify_of_property_changed = "notify_of_property_changed(const ZOO_UINT32 property_name)"

    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("extern \"C\" \n")
            f.write("{\n")
            f.write("    #include <ZOO.h>\n")
            f.write("}\n")
            f.write("#include <vector>\n")
            f.write("#include <boost/any.hpp>\n")
            f.write("#include \"PROPERTY_CHANGED_OBSERVER_INTERFACE.h\"\n")
            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    template <typename T>\n")
            f.write("    class "+ self._class_name +"\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       "+ self._class_name +"(){}\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~"+ self._class_name +"(){}\n")
            f.write("    public:\n")

            f.write("        /*\n")
            f.write("         * @brief Add observer will be notified when property changed\n")
            f.write("         * @param observer  Property changed observer\n")
            f.write("        **/\n")
            f.write("        virtual void " + self.add_observer + " = 0;\n")
            f.write("\n")

            f.write("        /*\n")
            f.write("         * @brief Remove observer from subscribe list\n")
            f.write("        **/\n")
            f.write("        virtual void " + self.remove_observer + " = 0;\n")
            f.write("\n")

            f.write("        /*\n")
            f.write("         * @brief Remove observer from subscribe listd\n")
            f.write("        **/\n")
            f.write("        virtual void " + self.clean + " = 0;\n")
            f.write("\n")

            f.write("        /*\n")
            f.write("         * @brief Notify property has been changed\n")
            f.write("         * @param property_name     The property has been changed\n")
            f.write("        **/\n")
            f.write("        virtual void " + self.notify_of_property_changed + " = 0;\n")
            f.write("\n")

            f.write("    };\n")
            f.write("} //namespace " + self.comp + "\n")
            f.write("#endif\n")

class PROPERTY_CHANGE_KEY_DEFINE(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  +  "PROPERTY_CHANGE_KEY_DEFINE.h"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,"PROPERTY_CHANGE_KEY_DEFINE.h")
        self._file_name =  "PROPERTY_CHANGE_KEY_DEFINE.h"

    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("#include <ZOO.h>\n\n")
            f.write("/******************************************************************\n")
            f.write("* Define property key \n")
            f.write("*****************************************************************/\n")
            f.write("#define PROPERTY_CHANGE_KEY_1   (0) \n")
            f.write("#define PROPERTY_CHANGE_KEY_2   (1) \n")
            f.write("#define PROPERTY_CHANGE_KEY_3   (2) \n")
            f.write("#define PROPERTY_CHANGE_KEY_4   (3) \n")
            f.write("#define PROPERTY_CHANGE_KEY_5   (4) \n")
            f.write("#define PROPERTY_CHANGE_KEY_6   (5) \n")
            f.write("#define PROPERTY_CHANGE_KEY_7   (6) \n")
            f.write("#define PROPERTY_CHANGE_KEY_8   (7) \n")
            f.write("#endif\n")

class XX_CONFIGUE(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  + comp + "_CONFIGURE.h"
        self.file_cpp = dir + '/' + comp + "_CONFIGURE.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,comp + "_CONFIGURE.h")
        self._header_comment_cpp = FILE_HEADER_COMMENT_CLASS('ZOO',comp,comp + "_CONFIGURE.cpp")
        self._file_name =  comp + "_CONFIGURE.h"
        self._class_name = comp + "_CONFIGURE"
        self._func_init = "initialize()"
        self._func_reload = "reload()"
        self._func_get_execute_path = "get_execute_path()"
        self._func_instance = "get_instance()"
        self._get_simulation_file = "get_mock_file()"

    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("\n")
            f.write("#include <string>\n")
            f.write("#include <boost/shared_ptr.hpp>\n")
            f.write("#include <boost/filesystem.hpp>\n")
            f.write("#include <utils/ENVIRONMENT_UTILITY_CLASS.h>\n\n")

            f.write("namespace " + self.comp +"\n")
            f.write("{\n")
            f.write("    class "+ self._class_name +"\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       "+ self._class_name +"();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~"+ self._class_name +"();\n")
            f.write("    public:\n")

            f.write("        /*\n")
            f.write("         * @brief Get instance\n")
            f.write("        **/\n")
            f.write("        static boost::shared_ptr<" + self._class_name + "> "+ self._func_instance + ";\n")
            f.write("\n")

            f.write("        /*\n")
            f.write("         * @brief Initialize\n")
            f.write("        **/\n")
            f.write("        void " + self._func_init + ";\n")
            f.write("\n")

            f.write("        /*\n")
            f.write("         * @brief Reload configurations\n")
            f.write("        **/\n")
            f.write("        void " + self._func_reload + ";\n")
            f.write("\n")

            f.write("        /*\n")
            f.write("         * @brief Get execute path.\n")
            f.write("        **/\n")
            f.write("        std::string " + self._func_get_execute_path + ";\n")
            f.write("\n")

            f.write("        /*\n")
            f.write("         * @brief Get simulation file path.\n")
            f.write("        **/\n")
            f.write("        std::string " + self._get_simulation_file + ";\n")
            f.write("\n")

            f.write("    private:\n")
            f.write("        /*\n")
            f.write("         * @brief The instance\n")
            f.write("        **/\n")
            f.write("        static boost::shared_ptr<"+self._class_name+"> m_instance;\n\n")
            f.write("        /*\n")
            f.write("         * @brief Execute base path\n")
            f.write("        **/\n")
            f.write("        std::string m_execute_path;\n\n")
            f.write("        /*\n")
            f.write("         * @brief Simulation data file path\n")
            f.write("        **/\n")
            f.write("        std::string m_simulation_file_path;\n")
            f.write("\n")

            f.write("    };\n")
            f.write("} //namespace " + self.comp + "\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_cpp.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \""+self._file_name +"\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Define base relative path.\n")
            f.write("    **/ \n")
            f.write("    static const char * CFG_RELATIVE_PATH = \"config\";\n\n")

            f.write("    /*\n")
            f.write("     * @brief Number level forward back from execute base to relative path.\n")
            f.write("    **/ \n")
            f.write("    static const ZOO_INT32 NUMBER_LEVEL = 3;\n\n")

            f.write("    /*\n")
            f.write("     * @brief Define base relative path.\n")
            f.write("    **/ \n")
            f.write("    static const char * SLASH = \"/\";\n\n")

            f.write("    /*\n")
            f.write("     * @brief Define base relative path.\n")
            f.write("    **/ \n")
            f.write("    static const char * SIMULATE_DATA_FILE = \""+ self.comp + "/mock_data/"+ self.comp + "_mock_data.ini\";\n\n")

            f.write("    /*\n")
            f.write("     * @brief The instance\n")
            f.write("    **/\n")
            f.write("    boost::shared_ptr<" + self._class_name + "> "+ self._class_name + "::m_instance = NULL;\n\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    " + self._class_name + "::" + self._class_name + "()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Destructor\n")
            f.write("    **/ \n")
            f.write("    " + self._class_name + "::~" + self._class_name + "()\n")
            f.write("    {\n\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Get instance\n")
            f.write("    **/\n")
            f.write("    boost::shared_ptr<" + self._class_name + "> " + self._class_name + "::"+ self._func_instance + "\n")
            f.write("    {\n")
            f.write("        if(" + self._class_name + "::m_instance == nullptr)\n")
            f.write("        {\n")
            f.write("            " + self._class_name + "::m_instance.reset(new " + self._class_name + "());\n")
            f.write("        }\n")
            f.write("        return " + self._class_name + "::m_instance;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Initialize\n")
            f.write("    **/\n")
            f.write("    void " + self._class_name + "::" + self._func_init + "\n")
            f.write("    {\n")
            f.write("        " + self._class_name + "::m_instance->reload();\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Get execute path\n")
            f.write("    **/\n")
            f.write("    std::string " + self._class_name + "::" + self._func_get_execute_path + "\n")
            f.write("    {\n")
            f.write("        return this->m_execute_path;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Get simulation file path\n")
            f.write("    **/\n")
            f.write("    std::string " + self._class_name + "::" + self._get_simulation_file + "\n")
            f.write("    {\n")
            f.write("        return this->m_simulation_file_path;\n")
            f.write("    }\n\n")

            f.write("    /*\n")
            f.write("     * @brief Reload configurations\n")
            f.write("    **/\n")
            f.write("    void " + self._class_name + "::"+ self._func_reload + "\n")
            f.write("    {\n")
            f.write("        this->m_execute_path = ZOO_COMMON::ENVIRONMENT_UTILITY_CLASS::get_execute_path();\n")
            f.write("        std::string configure_base = \n")
            f.write("            ZOO_COMMON::ENVIRONMENT_UTILITY_CLASS::get_parent_dir(this->m_execute_path,NUMBER_LEVEL);\n")
            f.write("        this->m_simulation_file_path = \n")
            f.write("            ZOO_COMMON::ENVIRONMENT_UTILITY_CLASS::combine_path(configure_base,std::string(CFG_RELATIVE_PATH) + SLASH + SIMULATE_DATA_FILE);\n")
            f.write("    }\n")

            f.write("} //namespace " + self.comp + "\n\n")

class COMMON_MACRO_DEFINE(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  + comp + "_COMMON_MACRO_DEFINE.h"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,comp + "_COMMON_MACRO_DEFINE.h")
        self._file_name =  comp + "_COMMON_MACRO_DEFINE.h"
    def generate(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("#include \"ZOO_if.hpp\"\n")
            f.write("#include <exceptions/PARAMETER_EXCEPTION_CLASS.h>\n\n")

            f.write("/*\n")
            f.write(" * @brief Wrapper try\n")
            f.write(" **/\n")
            f.write("#define __"+ self.comp+"_TRY try\n\n")

            f.write("/*\n")
            f.write("* @brief Define a macro to throw "+ self.comp+" exception\n")
            f.write("* @param error_code        The error code\n")
            f.write("* @param error_message     The error message\n")
            f.write("* @param inner_exception   The inner exception,& std::exception\n")
            f.write("**/\n")
            f.write("#define __THROW_"+ self.comp+"_EXCEPTION(error_code,error_message,inner_exception) \\\n")
            f.write("ZOO_slog(ZOO_SEVERITY_LEVEL_WARNING,error_message,NULL); \\\n")
            f.write("throw ZOO_COMMON::PARAMETER_EXCEPTION_CLASS(error_code, error_message, inner_exception)\n\n")

            f.write("/*\n")
            f.write("* @brief Define a macro catch model exception\n")
            f.write("* @param continue        continue throw exception\n")
            f.write("**/\n")
            f.write("#define __"+ self.comp+"_CATCH(continue) catch(ZOO_COMMON::PARAMETER_EXCEPTION_CLASS & e) \\\n")
            f.write("{\\\n")
            f.write("    if(continue) throw ZOO_COMMON::PARAMETER_EXCEPTION_CLASS(e.get_error_code(), e.get_error_message(),NULL);\\\n")
            f.write("}\n\n")

            f.write("/*\n")
            f.write("* @brief Define a macro to catch all exception\n")
            f.write("* @param result\n")
            f.write("**/\n")
            f.write("#define __"+ self.comp+"_CATCH_ALL(result) catch(ZOO_COMMON::PARAMETER_EXCEPTION_CLASS & e) \\\n")
            f.write("{\\\n")
            f.write("    result = e.get_error_code();\\\n")
            f.write("}\\\n")
            f.write("catch(...){}\n\n")
            f.write("#endif\n")


class MARKING_MODEL_INTERFACE(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  +  "MARKING_MODEL_INTERFACE.hpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,"MARKING_MODEL_INTERFACE.hpp")
        self._file_name =  "MARKING_MODEL_INTERFACE.hpp"
        self._class_name = "MARKING_MODEL_INTERFACE"
        self.get_marking_code = "get_marking_code()"
        self.set_marking_code = "set_marking_code(std::string marking_code)"
        self._marking_code = "m_marking_code"
        self._common_marco_header = comp +"_COMMON_MACRO_DEFINE.h"

    def generate(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("#include \"NOTIFY_PROPERTY_CHANGED_INTERFACE.h\"\n")
            f.write("#include \"PROPERTY_CHANGED_OBSERVER_INTERFACE.h\"\n")
            f.write("#include \""+self._common_marco_header+"\"\n")
            f.write("#include <boost/shared_ptr.hpp>\n\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    class " + self._class_name + "\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       " + self._class_name + "(){}\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~" + self._class_name + "(){}\n")
            f.write("    public:\n")

            f.write("        /*\n")
            f.write("         * @brief Get marking code\n")
            f.write("         * @return marking code\n")
            f.write("        **/\n")
            f.write("        std::string " + self.get_marking_code + "\n")
            f.write("        {\n")
            f.write("            return this->m_marking_code;\n")
            f.write("        }\n")
            f.write("\n")

            f.write("        /*\n")
            f.write("         * @brief Set marking code\n")
            f.write("         * @return marking code\n")
            f.write("        **/\n")
            f.write("        void " + self.set_marking_code + "\n")
            f.write("        {\n")
            f.write("            this->m_marking_code = marking_code;\n")
            f.write("        }\n")
            f.write("\n")

            f.write("        /*\n")
            f.write("         * @brief Get pointer\n")
            f.write("         * @return pointer\n")
            f.write("        **/\n")
            f.write("        template<typename T>\n")
            f.write("        boost::shared_ptr<T> get_pointer()\n")
            f.write("        {\n")
            f.write("            if (NULL == this->m_pointer)\n")
            f.write("            {\n")
            f.write("                this->m_pointer.reset(this);\n")
            f.write("            }\n")
            f.write("            return boost::dynamic_pointer_cast<T>(this->m_pointer);\n")
            f.write("        }\n")
            f.write("\n")

            f.write("        /*\n")
            f.write("         * @brief Get pointer\n")
            f.write("         * @return pointer\n")
            f.write("        **/\n")
            f.write("        template<typename T>\n")
            f.write("        static boost::shared_ptr<T> get_pointer(MARKING_MODEL_INTERFACE* marking_model)\n")
            f.write("        {\n")
            f.write("            return boost::dynamic_pointer_cast<T>(marking_model->get_pointer<T>());\n")
            f.write("        }\n")
            f.write("\n")
            f.write("    protected:\n")
            f.write("        /*\n")
            f.write("         * @brief The marking_code attribute.\n")
            f.write("        **/\n")
            f.write("        std::string m_marking_code;\n")
            f.write("\n")
            f.write("        /*\n")
            f.write("         * @brief Current pointer instance.\n")
            f.write("        **/\n")
            f.write("         boost::shared_ptr<MARKING_MODEL_INTERFACE> m_pointer;\n")
            f.write("\n")
            f.write("    };\n")
            f.write("}\n")
            f.write("#endif\n")


class DEVICE_MODEL_ABSTRCT_CLASS(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  +  "DEVICE_MODEL_ABSTRCT_CLASS.h"
        self.file_cpp = dir + '/'  +  "DEVICE_MODEL_ABSTRCT_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,"DEVICE_MODEL_ABSTRCT_CLASS.h")
        self._file_name =  "DEVICE_MODEL_ABSTRCT_CLASS.h"
        self._class_name = "DEVICE_MODEL_ABSTRCT_CLASS"
        self.interface = comp + "_MODEL_INTERFACE"
        self.set_marking_code = "set_marking_code(std::string marking_code)"
        self._marking_code = "m_marking_code"
        self._common_marco_header = comp +"_COMMON_MACRO_DEFINE.h"
    
    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("#include \""+self.interface+".h\"\n")
            f.write("#include \""+self._common_marco_header+"\"\n")
            f.write("#include <boost/shared_ptr.hpp>\n\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    class " + self._class_name + "\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       " + self._class_name + "();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~" + self._class_name + "();\n")
            f.write("    public:\n")
            f.write("    protected:\n")
            f.write("    };\n")
            f.write("}\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \""+self._class_name+".h\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("     **/ \n")
            f.write("    " + self._class_name + "::" + self._class_name + "()\n")
            f.write("    {\n")
            f.write("    }\n")
            f.write("    /*\n")
            f.write("     * @brief Destructor\n")
            f.write("     **/ \n")
            f.write("    " + self._class_name + "::~" + self._class_name + "()\n")
            f.write("    {\n")
            f.write("    }\n")
            f.write("}\n")

class MOCK_DATA_CLASS(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  +  "MOCK_DATA_CLASS.h"
        self.file_cpp = dir + '/'  +  "MOCK_DATA_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,"MOCK_DATA_CLASS.h")
        self._file_name =  "MOCK_DATA_CLASS.h"
        self._class_name = "MOCK_DATA_CLASS"
        self._common_macro_file = self.comp + "_COMMON_MACRO_DEFINE.h"
    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("#include \""+self._common_macro_file + "\"\n")
            f.write("#include <map>\n")
            f.write("#include <string>\n")
            f.write("#include <boost/shared_ptr.hpp>\n\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    class " + self._class_name + "\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       " + self._class_name + "();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~" + self._class_name + "();\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Add data\n")
            f.write("        * @param name\n")
            f.write("        * @param value\n")
            f.write("       **/\n")
            f.write("       void add_data(std::string name,std::string value);\n\n")
            f.write("       /*\n")
            f.write("        * @brief Get data\n")
            f.write("        * @param name\n")
            f.write("       **/\n")
            f.write("       std::string get_data(std::string name);\n\n")
            f.write("    private:\n")
            f.write("       /*\n")
            f.write("        * @brief Test data map\n")
            f.write("       **/\n")
            f.write("       std::map<std::string,std::string> m_data_map;\n")
            f.write("    };\n")
            f.write("}\n")
            f.write("#endif\n")
    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \"MOCK_DATA_PARSER_CLASS.h\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("   /*\n")
            f.write("    * @brief Constructor\n")
            f.write("    **/ \n")
            f.write("    " + self._class_name + "::"  + self._class_name + "()\n\n")
            f.write("    {\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Destructor\n")
            f.write("    **/ \n")
            f.write("    " + self._class_name + "::~" + self._class_name + "()\n")
            f.write("    {\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Add data\n")
            f.write("     * @param name\n")
            f.write("     * @param value\n")
            f.write("     **/\n")
            f.write("    void " + self._class_name + "::add_data(std::string name,std::string value)\n")
            f.write("    {\n")
            f.write("        this->m_data_map[name] = value;\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Get data\n")
            f.write("     * @param name\n")
            f.write("     **/\n")
            f.write("    std::string " + self._class_name + "::get_data(std::string name)\n")
            f.write("    {\n")
            f.write("        std::map<std::string,std::string>::iterator ite = this->m_data_map.begin();\n")
            f.write("        while( ite != this->m_data_map.end())\n")
            f.write("        {\n")
            f.write("            if(ite->first == name)\n")
            f.write("            {\n")
            f.write("                return ite->second;\n")
            f.write("            }\n")
            f.write("            ite ++;\n")
            f.write("        }\n")
            f.write("        return \"\";\n")
            f.write("    }\n")
            f.write("}\n")

class INI_PARSER_ABSTRACT_CLASS(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  +  "INI_PARSER_ABSTRACT_CLASS.h"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,"INI_PARSER_ABSTRACT_CLASS.h")
        self._file_name =  "INI_PARSER_ABSTRACT_CLASS.h"
        self._class_name = "INI_PARSER_ABSTRACT_CLASS"
    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))

            f.write("extern \"C\" \n{\n")
            f.write("    #include \"ZOO.h\"\n")
            f.write("    #include \"ZOO_if.h\"\n")
            f.write("}\n\n")

            f.write("#include <boost/property_tree/ptree.hpp>\n")
            f.write("#include <boost/property_tree/ini_parser.hpp>\n")
            f.write("#include <boost/foreach.hpp>\n")
            f.write("#include <boost/shared_ptr.hpp>\n")
            f.write("#include <map>\n")
            f.write("#include <string>\n\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    typedef std::string SECTION_TYPE;\n")
            f.write("    class " + self._class_name + "\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       " + self._class_name + "(){}\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~" + self._class_name + "(){}\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Parse data from config file\n")
            f.write("       **/\n")
            f.write("       template<typename T>\n")
            f.write("       T parse_data(IN std::string file,IN std::string section,IN std::string field_name)\n")
            f.write("       {\n")
            f.write("           boost::property_tree::ptree pt;\n")
            f.write("           boost::property_tree::ini_parser::read_ini(file, pt);\n")
            f.write("           return pt.get<T>(section.append(\".\") + field_name);\n")
            f.write("       }\n\n")
            f.write("       /*\n")
            f.write("        * @brief Parse section from config file\n")
            f.write("       **/\n")
            f.write("       std::map<std::string,std::string> parse_section(IN std::string file,IN std::string section)\n")
            f.write("       {\n")
            f.write("           std::map<std::string,std::string> result;\n")
            f.write("           boost::property_tree::ptree pt;\n")
            f.write("           boost::property_tree::ini_parser::read_ini(file, pt);\n")
            f.write("           BOOST_FOREACH(const boost::property_tree::ptree::value_type & v, pt.get_child(section))\n")
            f.write("           {\n")
            f.write("               result[v.first] = v.second.get_value<std::string>();\n")
            f.write("           }\n")
            f.write("           return result;\n")
            f.write("       }\n")
            f.write("    };\n")
            f.write("}\n")
            f.write("#endif\n")

class MOCK_DATA_PARSER_CLASS(object):
    def __init__(self,comp = '',dir = ''):
        self.comp = comp
        self.file_h = dir + '/'  +  "MOCK_DATA_PARSER_CLASS.h"
        self.file_cpp = dir + '/'  +  "MOCK_DATA_PARSER_CLASS.cpp"
        self._header_comment_h = FILE_HEADER_COMMENT_CLASS('ZOO',comp,"MOCK_DATA_PARSER_CLASS.h")
        self._file_name =  "MOCK_DATA_PARSER_CLASS.h"
        self._class_name = "MOCK_DATA_PARSER_CLASS"
        self._simulation_class_name = "MOCK_DATA_CLASS"
    def generate_h(self):
        with open(self.file_h, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write(get_ifndef(self._file_name))
            f.write("#include \"INI_PARSER_ABSTRACT_CLASS.h\"\n")
            f.write("#include \"MOCK_DATA_CLASS.h\"\n")
            f.write("#include <map>\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    class " + self._class_name + ": public virtual INI_PARSER_ABSTRACT_CLASS\n")
            f.write("    {\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Constructor\n")
            f.write("       **/ \n")
            f.write("       " + self._class_name + "();\n\n")
            f.write("       /*\n")
            f.write("        * @brief Destructor\n")
            f.write("       **/ \n")
            f.write("       virtual ~" + self._class_name + "();\n")
            f.write("    public:\n")
            f.write("       /*\n")
            f.write("        * @brief Parse mock data from config file\n")
            f.write("        * @param file   the ini file location\n")
            f.write("       **/\n")
            f.write("       std::map<SECTION_TYPE,boost::shared_ptr<MOCK_DATA_CLASS> > parse_mock_data(IN std::string file);\n\n")

            f.write("       /*\n")
            f.write("        * @brief add section name\n")
            f.write("        * @param name   section_name\n")
            f.write("       **/\n")
            f.write("       void add_section_name(IN std::string name);\n\n")

            f.write("       /*\n")
            f.write("        * @brief Get default mock data file\n")
            f.write("        * @param file   \n")
            f.write("       **/\n")
            f.write("       const std::string & get_mock_file();\n\n")
            
            f.write("    private:\n")
            f.write("       /*\n")
            f.write("        * @brief Section names \n")
            f.write("       **/\n")
            f.write("       std::vector<std::string> m_section_names;\n\n")
            f.write("       /*\n")
            f.write("        * @brief mock file\n")
            f.write("       **/\n")
            f.write("       std::string m_mock_file;\n")
            f.write("    };\n")
            f.write("}\n")
            f.write("#endif\n")

    def generate_cpp(self):
        with open(self.file_cpp, 'w+') as f:
            for c in self._header_comment_h.get_list():
                f.write(c)
                f.write("\n")
            f.write("#include \""+self._class_name+".h\"\n")
            f.write("namespace " + self.comp + "\n")
            f.write("{\n")
            f.write("    /*\n")
            f.write("     * @brief Constructor\n")
            f.write("     **/ \n")
            f.write("    " + self._class_name + "::" + self._class_name + "()\n")
            f.write("    {\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Destructor\n")
            f.write("     **/ \n")
            f.write("    " + self._class_name + "::~" + self._class_name + "()\n")
            f.write("    {\n")
            f.write("    }\n\n")
            f.write("    /*\n")
            f.write("     * @brief Parse mock data from config file\n")
            f.write("     * @param file   the ini file location\n")
            f.write("     **/ \n")
            f.write("    std::map<SECTION_TYPE,boost::shared_ptr<MOCK_DATA_CLASS> > " + self._class_name + "::parse_mock_data(IN std::string file)\n")
            f.write("    {\n")
            f.write("        std::map<SECTION_TYPE,boost::shared_ptr<MOCK_DATA_CLASS> > sections;\n")
            f.write("        // TODO: parse field value \n")
            f.write("        for(auto & section_name: this->m_section_names)\n")
            f.write("        {\n")
            f.write("           boost::shared_ptr<MOCK_DATA_CLASS> mock_data_model = boost::make_shared<MOCK_DATA_CLASS>();\n")
            f.write("           std::map<std::string,std::string> section = this->parse_section(file,section_name);\n")
            f.write("           std::for_each(section.begin(),section.end(),[mock_data_model](auto & v)\n")
            f.write("           {\n")
            f.write("               mock_data_model->add_data(v.first,v.second);\n")
            f.write("           });\n")
            f.write("           sections[section_name] = mock_data_model;\n")
            f.write("        }\n")
            f.write("        return sections;\n")
            f.write("    }\n")
            f.write("    /*\n")
            f.write("     * @brief add section name \n")
            f.write("     * @param name   \n")
            f.write("     **/ \n")
            f.write("    void " + self._class_name + "::add_section_name(IN std::string name)\n")
            f.write("    {\n")
            f.write("        this->m_section_name.push_back(name);\n")
            f.write("    }\n")
            f.write("    /*\n")
            f.write("     * @brief Get mock file \n")
            f.write("     * @return file    \n")
            f.write("     **/ \n")
            f.write("    const std::string & " + self._class_name + "::get_mock_file()\n")
            f.write("    {\n")
            f.write("        std::string exe_dir = ZOO_get_current_exec_path();\n")
            f.write("        std::string config_dir = ZOO_get_parent_dir(exe_dir.data(),3);\n")
            f.write("        this->m_mock_file = config_dir + \"/config/\" + \"mock_data\" +\"/\" + \"HTTP_mock_data.ini\"\n")
            f.write("        return this->m_mock_file;\n")
            f.write("    }\n")
            f.write("}\n")

class Componet(object):
    def __init__(self, if_h = '',type_h = '',t_if_f = ''):
        self._4aif_file = if_h
        self._type_file = type_h
        self._4tif_file = t_if_f
    def get_if_file(self):
        return self._4aif_file

    def set_4aif_file(self,_4a_if):
        self._4aif_file = _4a_if

    def get_4tif_file(self):
        return self._4tif_file

    def set_4tif_file(self,_t_if):
        self._4tif_file = _t_if

    def get_type_file(self):
        return self._type_file

    def set_type_file(self,type_file):
        self._type_file = type_file

    def get_id(self):
        return parse_compoent_id(self._4aif_file)

def parse_compoent_id(file=''):
    print("intput fileName = " + file)
    patten = re.compile(r'(\w*)4[AT]_[^.]')
    id = patten.findall(file)
    print("compoent_id: " + id[0])
    return id[0]

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

# **
# @ search interface header file
# @ return 1 found else fail
# **
def check_is_4t_interface_header_file(file_name=''):
    # print("intput fileName = " + file_name)
    result = file_name.find("4T_if.h")
    if result > -1:
        # print("find XX4A_if file: true")
        return 1  # find = true
    else:
        # print("find XX4A_if file: false")
        return 0  # find = true
# **
# @ search interface header file
# @ return 1 found else fail
# **
def check_is_type_header_file(file_name=''):
    #print("intput fileName = " + file_name)
    result = file_name.find("4A_type.h")
    # print(result)
    if result > -1:
        # print("find XX4A_type.h file: true")
        return 1  # find = true
    else:
        # print("find XX4A_type.h file: failed")
        return 0  # find = true

def search_header_file(dir=''):
    path = os.listdir(dir)
    print("current dir :" + dir)
    file_list = []
    for p in path:
        if os.path.isfile(p):
            if check_is_interface_header_file(p) == 1:
                print("found if file: " + p)
                tp_f = "4A_type"
                if_f = "4A_if"
                type_file = p.replace(if_f,tp_f)
                t_if = p.replace(if_f,"4T_if")
                print("found type file: " + type_file)
                c = Componet(p,type_file,t_if)
                file_list.append(c)
    return file_list

def CopyFile(srcfile, dstfile):
    #print(srcfile)
    if not os.path.isfile(srcfile):
        print(srcfile)
    else:
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径
        shutil.copyfile(srcfile, dstfile)  # 复制文件


def CopyHeaderFile(file):
    compoent_id = parse_compoent_id(file)
    #print("copy files" )
    #print("compoent_id: " + compoent_id)
    XX_DIR_GENERATOR(compoent_id)
    src_dir = os.getcwd() + "/" + file
    dst_dir = os.getcwd() + "/" + compoent_id + '/inc/' + file
    #print("src file: " + src_dir)
    #print("dst file: " + dst_dir)
    CopyFile(src_dir, dst_dir)

def FileGenenrator(XX4A_if='', XX4A_type='',compoent= '',XX4T_if=''):
    compoent_id = compoent
    xx_dir = XX_DIR_GENERATOR(compoent_id)
    inc_dir = xx_dir.get_inc_path()
    lib_dir = xx_dir.get_lib_path()
    com_dir = xx_dir.get_com_path()
    bin_dir = xx_dir.get_bin_path()
    test_dir = xx_dir.get_test_path()
    xx4a_if_h = XX4A_IF_HEADER_CLASS(os.getcwd() + "/" + XX4A_if)
    xx4a_type_h = XX4A_TYPE_HEADER_CLASS(os.getcwd() + "/" + XX4A_type)
    t_function_list = []
    t_cb_func_list = []

    a_function_list = xx4a_if_h.get_function_list(0)
    a_cb_func_list = xx4a_if_h.get_callback_list()
    function_list = a_function_list
    callback_list = a_cb_func_list

    product = xx4a_if_h.get_product()
    if os.path.exists(XX4T_if):
        xx4t_if_h =  XX4A_IF_HEADER_CLASS(os.getcwd() + "/" + XX4T_if)
        t_function_list = xx4t_if_h.get_function_list(len(a_function_list) - 1)
        t_cb_func_list = xx4t_if_h.get_callback_list()
        for f in t_function_list:
            function_list.append(f)
        for f in t_cb_func_list:
            callback_list.append(f)

    XX4I_type_h(compoent_id, function_list, callback_list, inc_dir).generate()
    XX4A_c(compoent_id, function_list, callback_list, lib_dir).generate()

    if os.path.exists(XX4T_if):
        XX4T_c(compoent_id, t_function_list, t_cb_func_list, lib_dir).generate()

    XX4I_if_h(compoent_id,inc_dir).generate()
    XX4I_c(compoent_id, function_list, lib_dir).generate()
    XX4A_event_h(compoent_id, function_list, com_dir, callback_list).generate()
    XX4A_event_c(compoent_id, function_list, bin_dir, callback_list).generate()
    XX4A_implement_h(compoent_id, function_list, com_dir).generate()
    XX4A_implement_c(compoent_id, function_list, bin_dir).generate()
    XX4A_dispatch_h(compoent_id, function_list, com_dir).generate()
    XX4A_dispatch_c(compoent_id, function_list, bin_dir).generate()
    EXECUTOR_WRAPPER_h(compoent_id,com_dir).generate()
    EXECUTOR_WRAPPER_c(compoent_id,bin_dir).generate()
    XX4A_main_c(compoent_id, function_list, bin_dir).generate()
    FLOW_FACADE_WRAPPER(function_list,compoent_id,com_dir).generate_h()
    FLOW_FACADE_WRAPPER(function_list,compoent_id,bin_dir).generate_cpp()
    PROCESSING_FLOW_FACADE(function_list,compoent_id,com_dir).generate_h()
    PROCESSING_FLOW_FACADE(function_list,compoent_id,bin_dir).generate_cpp()
    COMMON_FLOW_FACADE_CLASS(compoent_id,com_dir).generate_h()
    COMMON_FLOW_FACADE_CLASS(compoent_id,bin_dir).generate_cpp()
    MARKING_MODEL_INTERFACE(compoent_id, com_dir).generate()
    XX_CONFIGUE(compoent_id,com_dir).generate_h()
    XX_CONFIGUE(compoent_id,bin_dir).generate_cpp()
    CONTROLLER_ABSTRACT_CLASS(compoent_id, com_dir).generate_h()
    CONTROLLER_ABSTRACT_CLASS(compoent_id, bin_dir).generate_cpp()
    DEVICE_CONTROLLER_CLASS(compoent_id, com_dir).generate_h()
    DEVICE_CONTROLLER_CLASS(compoent_id, bin_dir).generate_cpp()
    DEVICE_INTERFACE(compoent_id,com_dir).generate_h()
    DEVICE_INTERFACE(compoent_id, bin_dir).generate_cpp()
    DEVICE_MODEL_CLASS(compoent_id, com_dir).generate_h()
    DEVICE_MODEL_CLASS(compoent_id, bin_dir).generate_cpp()
    HARDWARE_ABSTRACT_CLASS(compoent_id,com_dir).generate_h()
    HARDWARE_ABSTRACT_CLASS(compoent_id,bin_dir).generate_cpp()

    XX_HARDWARE_SERVICE(compoent_id,com_dir).generate_h()
    XX_HARDWARE_SERVICE(compoent_id,bin_dir).generate_cpp()
    STATE_MANAGER_CLASS(compoent_id,com_dir).generate_h()
    STATE_MANAGER_CLASS(compoent_id,bin_dir).generate_cpp()
    FLOW_FACADE_INTERFACE(compoent_id,com_dir).generate_h()
    FLOW_FACADE_ABSTRACT_CLASS(compoent_id,com_dir).generate_h()
    FLOW_FACADE_ABSTRACT_CLASS(compoent_id,bin_dir).generate_cpp()
    COMMON_MACRO_DEFINE(compoent_id,com_dir).generate()
    PROPERTY_CHANGED_OBSERVER_INTERFACE(compoent_id,com_dir).generate_h()
    NOTIFY_PROPERTY_CHANGED_INTERFACE(compoent_id,com_dir).generate_h()
    PROPERTY_CHANGE_KEY_DEFINE(compoent_id,com_dir).generate_h()
    EVENT_PUBLISHER_CLASS(compoent_id,com_dir,function_list,callback_list).generate_h()
    EVENT_PUBLISHER_CLASS(compoent_id,bin_dir,function_list,callback_list).generate_cpp()
    ENUM_CONVERTER_CLASS(compoent_id,com_dir).generate_h()
    DEVICE_MODEL_ABSTRCT_CLASS(compoent_id,com_dir).generate_h()
    DEVICE_MODEL_ABSTRCT_CLASS(compoent_id,bin_dir).generate_cpp()
    MOCK_DATA_CLASS(compoent_id,com_dir).generate_h()
    MOCK_DATA_CLASS(compoent_id,bin_dir).generate_cpp()
    INI_PARSER_ABSTRACT_CLASS(compoent_id,com_dir).generate_h()
    MOCK_DATA_PARSER_CLASS(compoent_id,com_dir).generate_h()
    MOCK_DATA_PARSER_CLASS(compoent_id,bin_dir).generate_cpp()
    XX_HARDWARE_MOCK(compoent_id,com_dir).generate_h()
    XX_HARDWARE_MOCK(compoent_id,bin_dir).generate_cpp()
    CopyHeaderFile(XX4A_if)
    CopyHeaderFile(XX4A_type)
    if os.path.exists(XX4T_if):
        CopyHeaderFile(XX4T_if)
    Makefile(compoent_id, os.getcwd() + "/" + compoent_id).generate_makefile()
    UNIT_TEST(compoent_id,test_dir,function_list).generate()
    return


def ComponentGenerator():
    root_dir = os.getcwd()
    componet_file_list = search_header_file(root_dir)
    for comp in componet_file_list:
        print("if file:" + comp.get_if_file())
        FileGenenrator(comp.get_if_file(), comp.get_type_file(),comp.get_id(),comp.get_4tif_file())
    return


if __name__ == '__main__':
    ComponentGenerator()
