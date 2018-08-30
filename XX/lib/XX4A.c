/***********************************************************
 * Copyright (C) 2018, shanghai NIO CO. ,LTD
 * All rights reserved.
 * Product        : ZOO
 * Component id   : XX
 * File Name      : XX4A.c
 * Description    : {Summary Description}
 * History        : 
 * Version        date          auther         context 
 * V1.0.0         2018-08-27    Generator      created
*************************************************************/

#include <ZOO.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <MQ4A_if.h>
#include <MQ4A_type.h>
#include <MM4A_if.h>
#include <EH4A_if.h>
#include <TR4A_if.h>
#include "XX4I_type.h"
#include "XX4A_type.h"
#include "XX4I_if.h"
/**
 *@brief XX4A_initialize
 *@param device_id
**/
ZOO_INT32 XX4A_initialize(IN XX4A_DEVICD_ID_ENUM device_id)
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 result = OK;
    XX4I_REQUEST_STRUCT *request_message = NULL;/* 消息发送参数*/ 
    XX4I_REPLY_STRUCT *reply_message = NULL;	/* 接收参数*/
    ZOO_INT32 ZOO_timeout = 60;
    ZOO_INT32 request_length = 0;/*发送消息长度*/
    ZOO_INT32 reply_length = 0;/*应该接收消息长度*/
    ZOO_INT32 func_code = XX4A_INITIALIZE_CODE;
    result = XX4I_get_request_message_length(func_code, &request_length);
    if(OK == result)
    {
        request_message = (XX4I_REQUEST_STRUCT *)MM4A_malloc(request_length);
    }

    if(OK == result)
    {
        if(request_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        result = XX4I_get_reply_message_length(func_code, &reply_length);
    }

    if(OK == result)
    {
        reply_message = (XX4I_REPLY_STRUCT *)MM4A_malloc(reply_length);
    }

    if(OK == result)
    {
        if(reply_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        request_message->request_header.function_code = func_code;
        reply_message->reply_header.function_code = func_code;
        request_message->request_header.need_reply = ZOO_TRUE;
        memcpy((void *)(&request_message->request_body.initialize_req_msg.device_id),&device_id,sizeof(XX4A_DEVICD_ID_ENUM));
    }

    if(OK == result)
    {
        result = XX4I_send_request_and_reply(XX4A_SERVER,request_message,reply_message,ZOO_timeout);
    }

    if(OK == result)
    {
        result = reply_message->reply_header.execute_result;
    }

    MM4A_free(request_message);
    MM4A_free(reply_message);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ..." );
    return result;
}

/**
 *@brief XX4A_initialize_req
 *@param device_id
**/
ZOO_INT32 XX4A_initialize_req(IN XX4A_DEVICD_ID_ENUM device_id)
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 result = OK;
    XX4I_REQUEST_STRUCT *request_message = NULL;/* 消息发送参数*/ 
    ZOO_INT32 req_length = 0;/*发送消息长度*/
    ZOO_INT32 func_code = XX4A_INITIALIZE_CODE;
    result = XX4I_get_request_message_length(func_code, &req_length);
    if(OK == result)
    {
        request_message = (XX4I_REQUEST_STRUCT *)MM4A_malloc(req_length);
    }

    if(OK == result)
    {
        if(request_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        request_message->request_header.function_code = func_code;
        request_message->request_header.need_reply = ZOO_TRUE;
        memcpy((void *)(&request_message->request_body.initialize_req_msg.device_id),&device_id,sizeof(XX4A_DEVICD_ID_ENUM));
    }

    if(OK == result)
    {
        result = XX4I_send_request_message(XX4A_SERVER,request_message);
    }

    MM4A_free(request_message);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ..." );
    return result;
}

/**
 *@brief XX4A_initialize_wait
 *@param timeout
**/
ZOO_INT32 XX4A_initialize_wait(IN ZOO_INT32 timeout)
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 result = OK;
    XX4I_REPLY_STRUCT *reply_message = NULL;	/* 接收参数*/
    ZOO_INT32 ZOO_timeout = 60;
    ZOO_INT32 reply_length = 0;/*应该接收消息长度*/
    ZOO_INT32 func_code = XX4A_INITIALIZE_CODE;
    if(OK == result)
    {
        result = XX4I_get_reply_message_length(func_code, &reply_length);
    }

    if(OK == result)
    {
        reply_message = (XX4I_REPLY_STRUCT *)MM4A_malloc(reply_length);
    }

    if(OK == result)
    {
        if(reply_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        result = XX4I_receive_reply_message(XX4A_SERVER,func_code,reply_message,ZOO_timeout);
    }

    if(OK == result)
    {
        result = reply_message->reply_header.execute_result;
    }

    MM4A_free(reply_message);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ..." );
    return result;
}

/**
 *@brief XX4A_get_status
 *@param device_id
 *@param status
**/
ZOO_INT32 XX4A_get_status(IN XX4A_DEVICD_ID_ENUM device_id,INOUT XX4A_STATUS_STRUCT *status)
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 result = OK;
    XX4I_REQUEST_STRUCT *request_message = NULL;/* 消息发送参数*/ 
    XX4I_REPLY_STRUCT *reply_message = NULL;	/* 接收参数*/
    ZOO_INT32 ZOO_timeout = 60;
    ZOO_INT32 request_length = 0;/*发送消息长度*/
    ZOO_INT32 reply_length = 0;/*应该接收消息长度*/
    ZOO_INT32 func_code = XX4A_GET_STATUS_CODE;
    result = XX4I_get_request_message_length(func_code, &request_length);
    if(OK == result)
    {
        request_message = (XX4I_REQUEST_STRUCT *)MM4A_malloc(request_length);
    }

    if(OK == result)
    {
        if(request_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        result = XX4I_get_reply_message_length(func_code, &reply_length);
    }

    if(OK == result)
    {
        reply_message = (XX4I_REPLY_STRUCT *)MM4A_malloc(reply_length);
    }

    if(OK == result)
    {
        if(reply_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        request_message->request_header.function_code = func_code;
        reply_message->reply_header.function_code = func_code;
        request_message->request_header.need_reply = ZOO_TRUE;
        memcpy((void *)(&request_message->request_body.get_status_req_msg.device_id),&device_id,sizeof(XX4A_DEVICD_ID_ENUM));
    }

    if(OK == result)
    {
        result = XX4I_send_request_and_reply(XX4A_SERVER,request_message,reply_message,ZOO_timeout);
    }

    if(OK == result)
    {
        result = reply_message->reply_header.execute_result;
        memcpy(status,&reply_message->reply_body.get_status_rep_msg.status,sizeof(XX4A_STATUS_STRUCT));
    }

    MM4A_free(request_message);
    MM4A_free(reply_message);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ..." );
    return result;
}

/**
 *@brief XX4A_get_status_req
 *@param device_id
**/
ZOO_INT32 XX4A_get_status_req(IN XX4A_DEVICD_ID_ENUM device_id)
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 result = OK;
    XX4I_REQUEST_STRUCT *request_message = NULL;/* 消息发送参数*/ 
    ZOO_INT32 req_length = 0;/*发送消息长度*/
    ZOO_INT32 func_code = XX4A_GET_STATUS_CODE;
    result = XX4I_get_request_message_length(func_code, &req_length);
    if(OK == result)
    {
        request_message = (XX4I_REQUEST_STRUCT *)MM4A_malloc(req_length);
    }

    if(OK == result)
    {
        if(request_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        request_message->request_header.function_code = func_code;
        request_message->request_header.need_reply = ZOO_TRUE;
        memcpy((void *)(&request_message->request_body.get_status_req_msg.device_id),&device_id,sizeof(XX4A_DEVICD_ID_ENUM));
    }

    if(OK == result)
    {
        result = XX4I_send_request_message(XX4A_SERVER,request_message);
    }

    MM4A_free(request_message);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ..." );
    return result;
}

/**
 *@brief XX4A_get_status_wait
 *@param timeout
 *@param status
**/
ZOO_INT32 XX4A_get_status_wait(INOUT XX4A_STATUS_STRUCT *status,
											IN ZOO_INT32 timeout)
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 result = OK;
    XX4I_REPLY_STRUCT *reply_message = NULL;	/* 接收参数*/
    ZOO_INT32 ZOO_timeout = 60;
    ZOO_INT32 reply_length = 0;/*应该接收消息长度*/
    ZOO_INT32 func_code = XX4A_GET_STATUS_CODE;
    if(OK == result)
    {
        result = XX4I_get_reply_message_length(func_code, &reply_length);
    }

    if(OK == result)
    {
        reply_message = (XX4I_REPLY_STRUCT *)MM4A_malloc(reply_length);
    }

    if(OK == result)
    {
        if(reply_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        result = XX4I_receive_reply_message(XX4A_SERVER,func_code,reply_message,ZOO_timeout);
    }

    if(OK == result)
    {
        result = reply_message->reply_header.execute_result;
        memcpy(status,&reply_message->reply_body.get_status_rep_msg.status,sizeof(XX4A_STATUS_STRUCT));
    }

    MM4A_free(reply_message);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ..." );
    return result;
}

static void XX4A_status_info_callback(void *context_p, MQ4A_CALLBACK_STRUCT *local_proc, void *msg)
{
    ZOO_INT32 result = OK;
    ZOO_INT32 error_code = OK;
    XX4I_REPLY_STRUCT *reply_msg = NULL;
    XX4I_STATUS_INFO_SUBSCRIBE_CODE_CALLBACK_STRUCT * callback_struct = NULL;
    ZOO_INT32 rep_length = 0;
    XX4A_STATUS_STRUCT status;
    if(msg == NULL)
    {
        result = XX4A_PARAMETER_ERR;
        EH4A_show_exception(COMPONENT_ID_XX, __FILE__, __ZOO_FUNC__, __LINE__,result,"msg is NULL.");
    }

    if(OK == result)
    {
        result = XX4I_get_reply_message_length(XX4A_STATUS_INFO_SUBSCRIBE_CODE, &rep_length);
        if(OK != result)
        {
            result = XX4A_PARAMETER_ERR;
            EH4A_show_exception(COMPONENT_ID_XX, __FILE__, __ZOO_FUNC__, __LINE__,result,"get_reply_messge_length failed.");
        }
    }

    if(OK == result)
    {
        reply_msg = (XX4I_REPLY_STRUCT * )MM4A_malloc(rep_length);
        if(OK != result)
        {
            result = XX4A_PARAMETER_ERR;
            EH4A_show_exception(COMPONENT_ID_XX, __FILE__, __ZOO_FUNC__, __LINE__,result,"MM4A_malloc failed.");
        }
    }

    if(OK == result)
    {
        memcpy(reply_msg, msg, rep_length);
        if (XX4A_STATUS_INFO_SUBSCRIBE_CODE != reply_msg->reply_header.function_code)
        {
            result = XX4A_PARAMETER_ERR;
            EH4A_show_exception(COMPONENT_ID_XX, __FILE__, __ZOO_FUNC__, __LINE__,result,"function code incorrect.");
        }
        error_code = reply_msg->reply_header.execute_result;
        memcpy((void*)&status, &reply_msg->reply_body.status_info_subscribe_code_rep_msg.status, sizeof(XX4A_STATUS_STRUCT));
        callback_struct = (XX4I_STATUS_INFO_SUBSCRIBE_CODE_CALLBACK_STRUCT*) local_proc;
        ((XX4A_STATUS_CALLBACK_FUNCTION)callback_struct->callback_function)(status,error_code,context_p);
    }

   if(reply_msg != NULL)
   {
        MM4A_free(reply_msg);
   }
}


 ZOO_INT32 XX4A_status_info_subscribe(IN XX4A_STATUS_CALLBACK_FUNCTION callback_function,
												  OUT ZOO_UINT32 *handle,
												  INOUT void *context)
{
    ZOO_INT32 result = OK;
    ZOO_INT32 event_id = 0;
    MQ4A_CALLBACK_STRUCT* callback = NULL;
    if (NULL == callback_function)
    {
        result = XX4A_PARAMETER_ERR;
        EH4A_show_exception(COMPONENT_ID_XX, __FILE__, __ZOO_FUNC__, __LINE__,result,"callback_function is NULL.");
        return result;
    }

    /*function entry*/
    TR4A_trace(COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    /*fill callback strcut*/
    callback = (MQ4A_CALLBACK_STRUCT*)MM4A_malloc(sizeof(XX4I_STATUS_INFO_SUBSCRIBE_CODE_CALLBACK_STRUCT));
    if (NULL == callback)
    {
        result = XX4A_PARAMETER_ERR;
        EH4A_show_exception(COMPONENT_ID_XX, __FILE__, __ZOO_FUNC__, __LINE__,result,"callback is NULL.");
    }

    if (OK == result)
    {
        callback->callback_function = callback_function;
        event_id = XX4A_STATUS_INFO_SUBSCRIBE_CODE;
        result = XX4I_send_subscribe(XX4A_SERVER,
                                      XX4A_status_info_callback,
                                      callback,
                                      event_id,
                                      (ZOO_HANDLE*)handle,
                                      context);
        if (OK != result)
        {
           result = XX4A_PARAMETER_ERR;
           EH4A_show_exception(COMPONENT_ID_XX, __FILE__, __ZOO_FUNC__, __LINE__,result,"send_subscribe failed.");
           MM4A_free(callback);
        }
    }

    TR4A_trace(COMPONENT_ID_XX, __ZOO_FUNC__,"< function exit ...");
    return result;
}

ZOO_INT32 XX4A_status_info_unsubscribe(IN ZOO_UINT32 handle)
{
    ZOO_INT32 result = OK;
    ZOO_INT32 event_id = XX4A_STATUS_INFO_SUBSCRIBE_CODE;
    if(OK == result)
    {
        result = XX4I_send_unsubscribe(XX4A_SERVER,event_id,handle);
    }
    return result;
}

/**
 *@brief XX4A_set_const_name
 *@param name
 *@param p[64]
**/

ZOO_INT32 XX4A_set_const_name(IN const ZOO_CHAR * name,OUT char p[64])
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 result = OK;
    XX4I_REQUEST_STRUCT *request_message = NULL;/* 消息发送参数*/ 
    XX4I_REPLY_STRUCT *reply_message = NULL;	/* 接收参数*/
    ZOO_INT32 ZOO_timeout = 60;
    ZOO_INT32 request_length = 0;/*发送消息长度*/
    ZOO_INT32 reply_length = 0;/*应该接收消息长度*/
    ZOO_INT32 func_code = XX4A_SET_CONST_NAME_CODE;
    result = XX4I_get_request_message_length(func_code, &request_length);
    if(OK == result)
    {
        request_message = (XX4I_REQUEST_STRUCT *)MM4A_malloc(request_length);
    }

    if(OK == result)
    {
        if(request_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        result = XX4I_get_reply_message_length(func_code, &reply_length);
    }

    if(OK == result)
    {
        reply_message = (XX4I_REPLY_STRUCT *)MM4A_malloc(reply_length);
    }

    if(OK == result)
    {
        if(reply_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        request_message->request_header.function_code = func_code;
        reply_message->reply_header.function_code = func_code;
        request_message->request_header.need_reply = ZOO_TRUE;
        memcpy((void *)(request_message->request_body.set_const_name_req_msg.name),name,sizeof(ZOO_CHAR ) * XX4I_BUFFER_LENGTH);
    }

    if(OK == result)
    {
        result = XX4I_send_request_and_reply(XX4A_SERVER,request_message,reply_message,ZOO_timeout);
    }

    if(OK == result)
    {
        result = reply_message->reply_header.execute_result;
        memcpy(&p[0],&reply_message->reply_body.set_const_name_rep_msg.p[0],sizeof(char) * 64);
    }

    MM4A_free(request_message);
    MM4A_free(reply_message);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ..." );
    return result;
}

/**
 *@brief XX4A_get_name
 *@param name[16][8]
**/

ZOO_INT32 XX4A_get_name(OUT ZOO_CHAR name[16][8])
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 result = OK;
    XX4I_REQUEST_STRUCT *request_message = NULL;/* 消息发送参数*/ 
    XX4I_REPLY_STRUCT *reply_message = NULL;	/* 接收参数*/
    ZOO_INT32 ZOO_timeout = 60;
    ZOO_INT32 request_length = 0;/*发送消息长度*/
    ZOO_INT32 reply_length = 0;/*应该接收消息长度*/
    ZOO_INT32 func_code = XX4A_GET_NAME_CODE;
    result = XX4I_get_request_message_length(func_code, &request_length);
    if(OK == result)
    {
        request_message = (XX4I_REQUEST_STRUCT *)MM4A_malloc(request_length);
    }

    if(OK == result)
    {
        if(request_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        result = XX4I_get_reply_message_length(func_code, &reply_length);
    }

    if(OK == result)
    {
        reply_message = (XX4I_REPLY_STRUCT *)MM4A_malloc(reply_length);
    }

    if(OK == result)
    {
        if(reply_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        request_message->request_header.function_code = func_code;
        reply_message->reply_header.function_code = func_code;
        request_message->request_header.need_reply = ZOO_TRUE;
    }

    if(OK == result)
    {
        result = XX4I_send_request_and_reply(XX4A_SERVER,request_message,reply_message,ZOO_timeout);
    }

    if(OK == result)
    {
        result = reply_message->reply_header.execute_result;
        memcpy(&name[0],&reply_message->reply_body.get_name_rep_msg.name[0],sizeof(ZOO_CHAR) * 16 * 8);
    }

    MM4A_free(request_message);
    MM4A_free(reply_message);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ..." );
    return result;
}

/**
 *@brief XX4A_set_name
 *@param name[16]
**/

ZOO_INT32 XX4A_set_name(IN ZOO_CHAR name[16])
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 result = OK;
    XX4I_REQUEST_STRUCT *request_message = NULL;/* 消息发送参数*/ 
    XX4I_REPLY_STRUCT *reply_message = NULL;	/* 接收参数*/
    ZOO_INT32 ZOO_timeout = 60;
    ZOO_INT32 request_length = 0;/*发送消息长度*/
    ZOO_INT32 reply_length = 0;/*应该接收消息长度*/
    ZOO_INT32 func_code = XX4A_SET_NAME_CODE;
    result = XX4I_get_request_message_length(func_code, &request_length);
    if(OK == result)
    {
        request_message = (XX4I_REQUEST_STRUCT *)MM4A_malloc(request_length);
    }

    if(OK == result)
    {
        if(request_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        result = XX4I_get_reply_message_length(func_code, &reply_length);
    }

    if(OK == result)
    {
        reply_message = (XX4I_REPLY_STRUCT *)MM4A_malloc(reply_length);
    }

    if(OK == result)
    {
        if(reply_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        request_message->request_header.function_code = func_code;
        reply_message->reply_header.function_code = func_code;
        request_message->request_header.need_reply = ZOO_TRUE;
        memcpy((void *)(&request_message->request_body.set_name_req_msg.name[0]),&name[0],sizeof(ZOO_CHAR) * 16);
    }

    if(OK == result)
    {
        result = XX4I_send_request_and_reply(XX4A_SERVER,request_message,reply_message,ZOO_timeout);
    }

    if(OK == result)
    {
        result = reply_message->reply_header.execute_result;
    }

    MM4A_free(request_message);
    MM4A_free(reply_message);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ..." );
    return result;
}

/**
 *@brief XX4A_start_sig
 *@param name[16]
**/

ZOO_INT32 XX4A_start_sig(IN ZOO_CHAR name[16])
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 result = OK;
    XX4I_REQUEST_STRUCT *request_message = NULL;/* 消息发送参数*/ 
    XX4I_REPLY_STRUCT *reply_message = NULL;	/* 接收参数*/
    ZOO_INT32 ZOO_timeout = 60;
    ZOO_INT32 request_length = 0;/*发送消息长度*/
    ZOO_INT32 reply_length = 0;/*应该接收消息长度*/
    ZOO_INT32 func_code = XX4A_START_SIG_CODE;
    result = XX4I_get_request_message_length(func_code, &request_length);
    if(OK == result)
    {
        request_message = (XX4I_REQUEST_STRUCT *)MM4A_malloc(request_length);
    }

    if(OK == result)
    {
        if(request_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        result = XX4I_get_reply_message_length(func_code, &reply_length);
    }

    if(OK == result)
    {
        reply_message = (XX4I_REPLY_STRUCT *)MM4A_malloc(reply_length);
    }

    if(OK == result)
    {
        if(reply_message == NULL)
        {
            result = XX4A_PARAMETER_ERR;
        }
    }

    if(OK == result)
    {
        request_message->request_header.function_code = func_code;
        reply_message->reply_header.function_code = func_code;
        request_message->request_header.need_reply = ZOO_FALSE;
        memcpy((void *)(&request_message->request_body.start_sig_req_msg.name[0]),&name[0],sizeof(ZOO_CHAR) * 16);
    }

    if(OK == result)
    {
        result = XX4I_send_signal(XX4A_SERVER,request_message,request_length);
    }

    if(OK == result)
    {
        result = reply_message->reply_header.execute_result;
    }

    MM4A_free(request_message);
    MM4A_free(reply_message);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ..." );
    return result;
}

