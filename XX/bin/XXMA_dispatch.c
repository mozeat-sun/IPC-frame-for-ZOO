/***********************************************************
 * Copyright (C) 2018, shanghai NIO CO. ,LTD
 * All rights reserved.
 * Product        : ZOO
 * Component id   : XX
 * File Name      : XXMA_dispatch.c
 * Description    : {Summary Description}
 * History        : 
 * Version        date          auther         context 
 * V1.0.0         2018-08-27    Generator      created
*************************************************************/

#include <EH4A_if.h>
#include <TR4A_if.h>
#include "XXMA_dispatch.h"
#include "XXMA_implement.h"

/**
 *@brief XXMA_local_4A_initialize
 *@param device_id
**/
static void XXMA_local_4A_initialize(const MQ4A_SERV_ADDR server,XX4I_REQUEST_STRUCT * request,XX4I_REPLY_STRUCT * reply)
{ 
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 rtn = OK;
    if(request == NULL)
    {
        EH4A_show_exception(COMPONENT_ID_XX,__FILE__,__ZOO_FUNC__,__LINE__,XX4A_PARAMETER_ERR,"request pointer is NULL ...ERROR");
    }

    if(OK == rtn)
    {
        reply->reply_header.function_code = request->request_header.function_code;
        rtn = XXMA_implement_4A_initialize(request->request_body.initialize_req_msg.device_id,
                                           reply);
    }
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ... ");
    return ;
}

/**
 *@brief XXMA_local_4A_get_status
 *@param device_id
 *@param status
**/
static void XXMA_local_4A_get_status(const MQ4A_SERV_ADDR server,XX4I_REQUEST_STRUCT * request,XX4I_REPLY_STRUCT * reply)
{ 
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 rtn = OK;
    if(request == NULL)
    {
        EH4A_show_exception(COMPONENT_ID_XX,__FILE__,__ZOO_FUNC__,__LINE__,XX4A_PARAMETER_ERR,"request pointer is NULL ...ERROR");
    }

    if(OK == rtn)
    {
        reply->reply_header.function_code = request->request_header.function_code;
        rtn = XXMA_implement_4A_get_status(request->request_body.get_status_req_msg.device_id,
                                           reply);
    }
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ... ");
    return ;
}

/**
 *@brief XXMA_local_4A_set_const_name
 *@param name
 *@param p[64]
**/
static void XXMA_local_4A_set_const_name(const MQ4A_SERV_ADDR server,XX4I_REQUEST_STRUCT * request,XX4I_REPLY_STRUCT * reply)
{ 
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 rtn = OK;
    if(request == NULL)
    {
        EH4A_show_exception(COMPONENT_ID_XX,__FILE__,__ZOO_FUNC__,__LINE__,XX4A_PARAMETER_ERR,"request pointer is NULL ...ERROR");
    }

    if(OK == rtn)
    {
        reply->reply_header.function_code = request->request_header.function_code;
        rtn = XXMA_implement_4A_set_const_name(request->request_body.set_const_name_req_msg.name,
                                           reply);
    }
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ... ");
    return ;
}

/**
 *@brief XXMA_local_4A_get_name
 *@param name[16][8]
**/
static void XXMA_local_4A_get_name(const MQ4A_SERV_ADDR server,XX4I_REQUEST_STRUCT * request,XX4I_REPLY_STRUCT * reply)
{ 
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 rtn = OK;
    if(request == NULL)
    {
        EH4A_show_exception(COMPONENT_ID_XX,__FILE__,__ZOO_FUNC__,__LINE__,XX4A_PARAMETER_ERR,"request pointer is NULL ...ERROR");
    }

    if(OK == rtn)
    {
        reply->reply_header.function_code = request->request_header.function_code;
        rtn = XXMA_implement_4A_get_name(reply);
    }
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ... ");
    return ;
}

/**
 *@brief XXMA_local_4A_set_name
 *@param name[16]
**/
static void XXMA_local_4A_set_name(const MQ4A_SERV_ADDR server,XX4I_REQUEST_STRUCT * request,XX4I_REPLY_STRUCT * reply)
{ 
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 rtn = OK;
    if(request == NULL)
    {
        EH4A_show_exception(COMPONENT_ID_XX,__FILE__,__ZOO_FUNC__,__LINE__,XX4A_PARAMETER_ERR,"request pointer is NULL ...ERROR");
    }

    if(OK == rtn)
    {
        reply->reply_header.function_code = request->request_header.function_code;
        rtn = XXMA_implement_4A_set_name(request->request_body.set_name_req_msg.name,
                                           reply);
    }
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ... ");
    return ;
}

/**
 *@brief XXMA_local_4A_start_sig
 *@param name[16]
**/
static void XXMA_local_4A_start_sig(const MQ4A_SERV_ADDR server,XX4I_REQUEST_STRUCT * request,XX4I_REPLY_STRUCT * reply)
{ 
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 rtn = OK;
    if(request == NULL)
    {
        EH4A_show_exception(COMPONENT_ID_XX,__FILE__,__ZOO_FUNC__,__LINE__,XX4A_PARAMETER_ERR,"request pointer is NULL ...ERROR");
    }

    if(OK == rtn)
    {
        reply->reply_header.function_code = request->request_header.function_code;
        rtn = XXMA_implement_4A_start_sig(request->request_body.start_sig_req_msg.name,
                                           reply);
    }
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ... ");
    return ;
}

/**
*@brief dispatch message from client to server internal interface
*@param context        
*@param server        address
*@param msg           request message to server
*@param len           request message length
*@param reply_msg     reply message length to caller
*@param reply_msg_len reply message length
**/
void XXMA_callback_handler(void * context,const MQ4A_SERV_ADDR server,void * msg,ZOO_INT32 len,void ** reply_msg,ZOO_INT32 * reply_msg_len)
{
    XX4I_REQUEST_STRUCT *request = (XX4I_REQUEST_STRUCT*)msg;
    *reply_msg_len = sizeof(XX4I_REPLY_STRUCT);
    XX4I_REPLY_STRUCT * reply = (XX4I_REPLY_STRUCT *) MM4A_malloc(sizeof(XX4I_REPLY_STRUCT));
    *reply_msg = reply;
    if(request == NULL)
    {
        EH4A_show_exception(COMPONENT_ID_XX,__FILE__,__ZOO_FUNC__,__LINE__,XX4A_PARAMETER_ERR,"request_message pointer is NULL ...ERROR");
        return;
    }

    if(reply_msg == NULL)
    {
        EH4A_show_exception(COMPONENT_ID_XX,__FILE__,__ZOO_FUNC__,__LINE__,XX4A_PARAMETER_ERR,"reply_message pointer is NULL ...ERROR");
        return;
    }

    switch(request->request_header.function_code)
    {
        case XX4A_INITIALIZE_CODE:
            XXMA_local_4A_initialize(server,request,reply);
            break;
        case XX4A_GET_STATUS_CODE:
            XXMA_local_4A_get_status(server,request,reply);
            break;
        case XX4A_SET_CONST_NAME_CODE:
            XXMA_local_4A_set_const_name(server,request,reply);
            break;
        case XX4A_GET_NAME_CODE:
            XXMA_local_4A_get_name(server,request,reply);
            break;
        case XX4A_SET_NAME_CODE:
            XXMA_local_4A_set_name(server,request,reply);
            break;
        case XX4A_START_SIG_CODE:
            XXMA_local_4A_start_sig(server,request,reply);
            break;
        default:
            EH4A_show_exception(COMPONENT_ID_XX,__FILE__,__ZOO_FUNC__,__LINE__,XX4A_PARAMETER_ERR,"invalid function code ...ERROR");
            break;
     }
}

