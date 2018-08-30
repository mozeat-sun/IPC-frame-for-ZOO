/***********************************************************
 * Copyright (C) 2018, shanghai NIO CO. ,LTD
 * All rights reserved.
 * Product        : ZOO
 * Component id   : XX
 * File Name      : XX4I.c
 * Description    : {Summary Description}
 * History        : 
 * Version        date          auther         context 
 * V1.0.0         2018-08-27    Generator      created
*************************************************************/
#include "XX4I_if.h"
/*
@brief 获取请求消息长度【字节】
*@param function_code   函数码
*@param *message_length 字节长度 
*@precondition:
*@postcondition:
*/
ZOO_INT32 XX4I_get_request_message_length(IN ZOO_INT32 function_code,
													INOUT ZOO_INT32 *message_length )
{    ZOO_INT32 result = OK;
    /* 检查输入参数指针是否?*/
    if ( NULL == message_length )
    {
        result = XX4A_PARAMETER_ERR;
        EH4A_show_exception(COMPONENT_ID_XX, __FILE__, __ZOO_FUNC__, __LINE__,result,"request msg length is NULL.");
    }
    else
    {
        *message_length = 0;
    }
    /*查询发送请求消息的长度*/
    if ( OK == result )
    {
        switch( function_code )
        {
        case XX4A_INITIALIZE_CODE:
            *message_length = sizeof(XX4I_REQUEST_HEADER_STRUCT)+sizeof(XX4I_INITIALIZE_CODE_REQ_STRUCT);
            break;
        case XX4A_GET_STATUS_CODE:
            *message_length = sizeof(XX4I_REQUEST_HEADER_STRUCT)+sizeof(XX4I_GET_STATUS_CODE_REQ_STRUCT);
            break;
        case XX4A_SET_CONST_NAME_CODE:
            *message_length = sizeof(XX4I_REQUEST_HEADER_STRUCT)+sizeof(XX4I_SET_CONST_NAME_CODE_REQ_STRUCT);
            break;
        case XX4A_GET_NAME_CODE:
            *message_length = sizeof(XX4I_REQUEST_HEADER_STRUCT)+sizeof(XX4I_GET_NAME_CODE_REQ_STRUCT);
            break;
        case XX4A_SET_NAME_CODE:
            *message_length = sizeof(XX4I_REQUEST_HEADER_STRUCT)+sizeof(XX4I_SET_NAME_CODE_REQ_STRUCT);
            break;
        case XX4A_START_SIG_CODE:
            *message_length = sizeof(XX4I_REQUEST_HEADER_STRUCT)+sizeof(XX4I_START_SIG_CODE_REQ_STRUCT);
            break;
        default:
               result = XX4A_PARAMETER_ERR;
               EH4A_show_exception(COMPONENT_ID_XX, __FILE__, __ZOO_FUNC__,__LINE__,result," Error in XX4I_get_request_message_length.");
               break;
        }
    }
    return result;
}


/*
@brief 获取回答消息长度【字节】
*@param function_code   函数码
*@param *message_length 字节长度 
*@precondition:
*@postcondition:
*/
ZOO_INT32 XX4I_get_reply_message_length(IN ZOO_INT32 function_code,
													INOUT ZOO_INT32 *message_length )
{    ZOO_INT32 result = OK;
    /* 检查输入参数指针是否?*/
    if ( NULL == message_length )
    {
        result = XX4A_PARAMETER_ERR;
        EH4A_show_exception(COMPONENT_ID_XX, __FILE__,__ZOO_FUNC__,__LINE__,result,"request msg length is NULL.");
    }
    else
    {
        *message_length = 0;
    }
    /*查询发送请求消息的长度*/
    if ( OK == result )
    {
        switch( function_code )
        {
        case XX4A_INITIALIZE_CODE:
            *message_length = sizeof(XX4I_REPLY_HEADER_STRUCT)+sizeof(XX4I_INITIALIZE_CODE_REP_STRUCT);
            break;
        case XX4A_GET_STATUS_CODE:
            *message_length = sizeof(XX4I_REPLY_HEADER_STRUCT)+sizeof(XX4I_GET_STATUS_CODE_REP_STRUCT);
            break;
        case XX4A_STATUS_INFO_SUBSCRIBE_CODE:
            *message_length = sizeof(XX4I_REPLY_HEADER_STRUCT)+sizeof(XX4I_STATUS_INFO_SUBSCRIBE_CODE_REP_STRUCT);
            break;
        case XX4A_SET_CONST_NAME_CODE:
            *message_length = sizeof(XX4I_REPLY_HEADER_STRUCT)+sizeof(XX4I_SET_CONST_NAME_CODE_REP_STRUCT);
            break;
        case XX4A_GET_NAME_CODE:
            *message_length = sizeof(XX4I_REPLY_HEADER_STRUCT)+sizeof(XX4I_GET_NAME_CODE_REP_STRUCT);
            break;
        case XX4A_SET_NAME_CODE:
            *message_length = sizeof(XX4I_REPLY_HEADER_STRUCT)+sizeof(XX4I_SET_NAME_CODE_REP_STRUCT);
            break;
        case XX4A_START_SIG_CODE:
            *message_length = sizeof(XX4I_REPLY_HEADER_STRUCT)+sizeof(XX4I_START_SIG_CODE_REP_STRUCT);
            break;
        default:
               result = XX4A_PARAMETER_ERR;
               EH4A_show_exception(COMPONENT_ID_XX, __FILE__,__ZOO_FUNC__, __LINE__,result," Error in XX4I_get_request_message_length.");
               break;
        }
    }
    return result;
}


/*
*@brief 向目标地址发送消息，并获得返回消息，同步接口，会阻塞调用方
*@param MQ4A_SERV_ADDR   服务器地址
*@param *request_message 请求消息
*@param *reply_message   回复消息
*@param timeout          请求消息最长等待超时时间 
*@precondition:
*@postcondition: 
*/
ZOO_INT32 XX4I_send_request_and_reply(IN const MQ4A_SERV_ADDR server,
													IN XX4I_REQUEST_STRUCT  *request_message,
													INOUT XX4I_REPLY_STRUCT *reply_message,
													IN ZOO_INT32 timeout)
{
    ZOO_INT32 result = OK;
    ZOO_INT32 request_length = 0;/*发送消息长*/
    ZOO_INT32 reply_length = 0;/*应该接收消息长度*/
    ZOO_INT32 actual_reply_length = 0;/*实际接收数据长度*/

    if(request_message == NULL)
    {
        result = XX4A_PARAMETER_ERR;
    }

    if(result == OK)
    {
        result = XX4I_get_request_message_length(request_message->request_header.function_code, &request_length);
    }

    if(result == OK)
    {
        result = XX4I_get_reply_message_length(reply_message->reply_header.function_code, &reply_length);
    }

    if(result == OK)
    {
        result = MQ4A_send_request_and_reply(server,
												request_message,
												request_length,
												reply_message,
												reply_length,
												&actual_reply_length,
												    XX4I_RETRY_INTERVAL,
												timeout);
    }

 	return result;
}

/*
*@brief 向目标地址发送消息，异步接口，非阻塞，配合XX4I_receive_reply_message
*@param MQ4A_SERV_ADDR   服务器地址
*@param *request_message 请求消息 
*@precondition:
*@postcondition:
*/
ZOO_INT32 XX4I_send_request_message(IN const MQ4A_SERV_ADDR server,
													IN XX4I_REQUEST_STRUCT *request_message)

{
    ZOO_INT32 result = OK;
    ZOO_INT32 request_length = 0;/* 发送的消息长度 */
    /*查询发送请求消息的长度*/
    if ( OK == result )
    {
        result = XX4I_get_request_message_length(request_message->request_header.function_code, &request_length );

    }

    /*发送消息*/
    if ( OK == result )
    {
        result = MQ4A_send_request( server,				 /*发送目标服务器地址*/
                                    request_message,					 /*发送消息体*/
                                    request_length,						 /*发送消息长*/
                                    XX4I_RETRY_INTERVAL );           /*发送间隔时*/
    }

    return result;
}

/*
*@brief 接收目标消息
	*@param server         服务器地址
*@param function_code  函数码
*@param *reply_message 返回消息
*@param timeout        超时时间
*@description:         异步接口，配合XX4I_send_request_message一起使用
*@precondition:
*@postcondition:
*/
ZOO_INT32 XX4I_receive_reply_message(IN const MQ4A_SERV_ADDR server,
													IN ZOO_INT32 function_code,
													INOUT XX4I_REPLY_STRUCT *reply_message,
													IN ZOO_INT32 timeout)
{
    ZOO_INT32 result = OK;
    ZOO_INT32 actual_replay_length = 0;    /*实际接收数据长度*/
    ZOO_INT32 reply_length = 0; /*应该接收长度*/
    result = XX4I_get_reply_message_length( function_code, &reply_length );
    /*接收返回消息*/
    if ( OK == result )
    {
        result = MQ4A_get_reply( server, 
                  					reply_message,
                       				reply_length,
										&actual_replay_length,
								        timeout );
     }

    return result;
}

/*
*@brief 向目标地址发布消息，订阅的用户可以收到消息
*@param event_id       消息的编号，一般指函数码
*@param *reply_message 消息结构体，函数参数组合
*@description:         需要先订阅，才能收到 
*@precondition:
*@postcondition:
*/
ZOO_INT32 XX4I_publish_event(IN const MQ4A_SERV_ADDR server,
													IN ZOO_INT32 event_id,
													INOUT XX4I_REPLY_STRUCT *reply_message)
{
    ZOO_INT32 result = OK;
    ZOO_INT32 reply_length = 0;
    result = XX4I_get_reply_message_length(reply_message->reply_header.function_code, &reply_length);
    if (OK == result)
    {
         result = MQ4A_publish( server,
								    event_id,
 								reply_message,
								    reply_length );
    }

    return result;
}

/*
*@brief 发送订阅消息
*@param server            服务器地址
*@param callback_function 本地回调处理函数
*@param callback_struct   接口回调结构体
*@param event_id          请求消息
*@param *handle           订阅输出句柄
*@param *context          上下文标识
 *@precondition:
*@postcondition:
*/
ZOO_INT32 XX4I_send_subscribe(IN const MQ4A_SERV_ADDR server,
													IN MQ4A_EVENT_CALLBACK_FUNCTION callback_function,
													IN MQ4A_CALLBACK_STRUCT *callback_struct,
													IN ZOO_INT32 event_id,
													INOUT ZOO_HANDLE *handle,
													INOUT void *context)
{
    ZOO_INT32 result = OK;
    //ZOO_INT32 reply_length = 0;
    //result = XX4I_get_reply_message_length(event_id, &reply_length);
    if(OK == result)
    {
        result = MQ4A_subscribe( server,
										    callback_function,
											callback_struct,
											event_id,
											handle,
											context);
    }
    return result;
}

/*
*@brief 取消订阅
*@param server   服务器地址
*@param event_id 请求消息
*@param handle   订阅输出句柄 
*@precondition:
*@postcondition:
*/
ZOO_INT32 XX4I_send_unsubscribe(IN const MQ4A_SERV_ADDR server,
													IN ZOO_INT32 event_id,
													IN ZOO_HANDLE handle)
{
    ZOO_INT32 result = OK;
    result = MQ4A_unsubscribe( server,
									 event_id,
								   	 handle );
    return result;
}

/*
*@brief 发送信号消息
*@param server  服务器地址
*@param message 请求消息
*@param message_length   请求消息长度
*@precondition:
*@postcondition:
*/
ZOO_INT32 XX4I_send_signal(IN const MQ4A_SERV_ADDR server,
													IN void * message,
													IN ZOO_INT32 message_length)
{
    ZOO_INT32 result = OK;
    if (OK == result)
    {
         result = MQ4A_push( server,
								    message,
								    message_length);
    }

    return result;
}

