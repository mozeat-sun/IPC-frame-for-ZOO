/***********************************************************
 * Copyright (C) 2018, shanghai NIO CO. ,LTD
 * All rights reserved.
 * Product        : ZOO
 * Component id   : XX
 * File Name      : XX4I_type.h
 * Description    : {Summary Description}
 * History        : 
 * Version        date          auther         context 
 * V1.0.0         2018-08-27    Generator      created
*************************************************************/
#ifndef XX4I_TYPE_H
#define XX4I_TYPE_H
#include <MQ4A_type.h>
#include "XX4A_type.h"
#include "XX4A_if.h"

/**
 *@brief Mirco Defnition
**/
#define COMPONENT_ID_XX "XX"
#define XX4A_SERVER     "XX4A_SERVER"
#define XX4I_BUFFER_LENGTH    256
#define XX4I_RETRY_INTERVAL   3

/**
 *@brief Function Code Definitions
**/
#define XX4A_INITIALIZE_CODE 0x5858ff00
#define XX4A_GET_STATUS_CODE 0x5858ff03
#define XX4A_STATUS_INFO_SUBSCRIBE_CODE 0x5858ff06
#define XX4A_SET_CONST_NAME_CODE 0x5858ff08
#define XX4A_GET_NAME_CODE 0x5858ff09
#define XX4A_SET_NAME_CODE 0x5858ff0a
#define XX4A_START_SIG_CODE 0x5858ff0b

/*Request and reply header struct*/
typedef struct
{
    MQ4A_SERV_ADDR repl_addr;
    ZOO_INT32 msg_id;
    ZOO_BOOL reply_wanted;
    ZOO_INT32 func_id;
}XX4I_REPLY_HANDLER_STRUCT;

/*Request message header struct*/
typedef struct
{
    ZOO_INT32 function_code;
    ZOO_BOOL need_reply;
}XX4I_REQUEST_HEADER_STRUCT;

/*Reply message header struct*/
typedef struct
{
    ZOO_INT32 function_code;
    ZOO_BOOL execute_result;
}XX4I_REPLY_HEADER_STRUCT;

/**
*@brief XX4I_INITIALIZE_CODE_REQ_STRUCT
**/
typedef struct 
{
    XX4A_DEVICD_ID_ENUM device_id;
    ZOO_CHAR filler[4];
}XX4I_INITIALIZE_CODE_REQ_STRUCT;

/**
*@brief XX4I_GET_STATUS_CODE_REQ_STRUCT
**/
typedef struct 
{
    XX4A_DEVICD_ID_ENUM device_id;
    ZOO_CHAR filler[4];
}XX4I_GET_STATUS_CODE_REQ_STRUCT;

/**
*@brief XX4I_SET_CONST_NAME_CODE_REQ_STRUCT
**/
typedef struct 
{
    ZOO_CHAR  name[XX4I_BUFFER_LENGTH];
}XX4I_SET_CONST_NAME_CODE_REQ_STRUCT;

/**
*@brief XX4I_GET_NAME_CODE_REQ_STRUCT
**/
typedef struct 
{
    ZOO_CHAR filler[8];
}XX4I_GET_NAME_CODE_REQ_STRUCT;

/**
*@brief XX4I_SET_NAME_CODE_REQ_STRUCT
**/
typedef struct 
{
    ZOO_CHAR name[16];
}XX4I_SET_NAME_CODE_REQ_STRUCT;

/**
*@brief XX4I_START_SIG_CODE_REQ_STRUCT
**/
typedef struct 
{
    ZOO_CHAR name[16];
}XX4I_START_SIG_CODE_REQ_STRUCT;

/**
*@brief XX4I_INITIALIZE_CODE_REP_STRUCT
**/
typedef struct 
{
    ZOO_CHAR filler[8];
}XX4I_INITIALIZE_CODE_REP_STRUCT;

/**
*@brief XX4I_GET_STATUS_CODE_REP_STRUCT
**/
typedef struct 
{
    XX4A_STATUS_STRUCT status[XX4I_BUFFER_LENGTH];
}XX4I_GET_STATUS_CODE_REP_STRUCT;

/**
*@brief XX4I_STATUS_INFO_SUBSCRIBE_CODE_REP_STRUCT
**/
typedef struct 
{
    XX4A_STATUS_STRUCT status;
    ZOO_CHAR filler[8];
}XX4I_STATUS_INFO_SUBSCRIBE_CODE_REP_STRUCT;

/**
*@brief XX4I_SET_CONST_NAME_CODE_REP_STRUCT
**/
typedef struct 
{
    char p[64];
}XX4I_SET_CONST_NAME_CODE_REP_STRUCT;

/**
*@brief XX4I_GET_NAME_CODE_REP_STRUCT
**/
typedef struct 
{
    ZOO_CHAR name[16][8];
}XX4I_GET_NAME_CODE_REP_STRUCT;

/**
*@brief XX4I_SET_NAME_CODE_REP_STRUCT
**/
typedef struct 
{
    ZOO_CHAR filler[8];
}XX4I_SET_NAME_CODE_REP_STRUCT;

/**
*@brief XX4I_START_SIG_CODE_REP_STRUCT
**/
typedef struct 
{
    ZOO_CHAR filler[8];
}XX4I_START_SIG_CODE_REP_STRUCT;

typedef struct
{
    XX4I_REQUEST_HEADER_STRUCT request_header;
    union
    {
        XX4I_INITIALIZE_CODE_REQ_STRUCT initialize_req_msg;
        XX4I_GET_STATUS_CODE_REQ_STRUCT get_status_req_msg;
        XX4I_SET_CONST_NAME_CODE_REQ_STRUCT set_const_name_req_msg;
        XX4I_GET_NAME_CODE_REQ_STRUCT get_name_req_msg;
        XX4I_SET_NAME_CODE_REQ_STRUCT set_name_req_msg;
        XX4I_START_SIG_CODE_REQ_STRUCT start_sig_req_msg;
     }request_body;
}XX4I_REQUEST_STRUCT;


typedef struct
{
    XX4I_REPLY_HEADER_STRUCT reply_header;
    union
    {
        XX4I_INITIALIZE_CODE_REP_STRUCT initialize_rep_msg;
        XX4I_GET_STATUS_CODE_REP_STRUCT get_status_rep_msg;
        XX4I_SET_CONST_NAME_CODE_REP_STRUCT set_const_name_rep_msg;
        XX4I_GET_NAME_CODE_REP_STRUCT get_name_rep_msg;
        XX4I_SET_NAME_CODE_REP_STRUCT set_name_rep_msg;
        XX4I_START_SIG_CODE_REP_STRUCT start_sig_rep_msg;
        XX4I_STATUS_INFO_SUBSCRIBE_CODE_REP_STRUCT status_info_subscribe_code_rep_msg;
    }reply_body;
}XX4I_REPLY_STRUCT;


/**
*@brief XX4I_STATUS_INFO_SUBSCRIBE_CODE_CALLBACK_STRUCT
**/
typedef struct 
{
    XX4A_STATUS_CALLBACK_FUNCTION *callback_function;
    void * parameter;
}XX4I_STATUS_INFO_SUBSCRIBE_CODE_CALLBACK_STRUCT;

#endif //XX4I_type.h
