/***********************************************************
 * Copyright (C) 2018, shanghai NIO CO. ,LTD
 * All rights reserved.
 * Product        : ZOO
 * Component id   : XX
 * File Name      : XX4I_if.h
 * Description    : {Summary Description}
 * History        : 
 * Version        date          auther         context 
 * V1.0.0         2018-08-27    Generator      created
*************************************************************/
#ifndef XX4I_IF_H
#define XX4I_IF_H

#include <ZOO.h>
#include <stdio.h>
#include <stdlib.h>
#include <EH4A_if.h>
#include <TR4A_if.h>
#include <MQ4A_if.h>
#include <MQ4A_type.h>
#include <MM4A_if.h>
#include "XX4I_type.h"
#include "XX4A_type.h"
/*
@brief 获取请求消息长度【字节】
*@param function_code   函数码
*@param *message_length 字节长度 
*@precondition:
*@postcondition:
*/
ZOO_EXPORT ZOO_INT32 XX4I_get_request_message_length(IN ZOO_INT32 function_code,
													INOUT ZOO_INT32 *message_length );

/*
@brief 获取回答消息长度【字节】
*@param function_code   函数码
*@param *message_length 字节长度 
*@precondition:
*@postcondition:
*/
ZOO_EXPORT ZOO_INT32 XX4I_get_reply_message_length(IN ZOO_INT32 function_code,
													INOUT ZOO_INT32 *message_length );

/*
*@brief 向目标地址发送消息，并获得返回消息，同步接口，会阻塞调用方
*@param MQ4A_SERV_ADDR   服务器地址
*@param *request_message 请求消息
*@param *reply_message   回复消息
*@param timeout          请求消息最长等待超时时间 
*@precondition:
*@postcondition: 
*/
ZOO_EXPORT ZOO_INT32 XX4I_send_request_and_reply(IN const MQ4A_SERV_ADDR server,
													IN XX4I_REQUEST_STRUCT  *request_message,
													INOUT XX4I_REPLY_STRUCT *reply_message,
													IN ZOO_INT32 timeout);

/*
*@brief 向目标地址发送消息，异步接口，非阻塞，配合XX4I_receive_reply_message
*@param MQ4A_SERV_ADDR   服务器地址
*@param *request_message 请求消息 
*@precondition:
*@postcondition:
*/
ZOO_EXPORT ZOO_INT32 XX4I_send_request_message(IN const MQ4A_SERV_ADDR server,
													IN XX4I_REQUEST_STRUCT *request_message);

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
ZOO_EXPORT ZOO_INT32 XX4I_receive_reply_message(IN const MQ4A_SERV_ADDR server,
													IN ZOO_INT32 function_code,
													INOUT XX4I_REPLY_STRUCT *reply_message,
													IN ZOO_INT32 timeout);

/*
*@brief 向目标地址发布消息，订阅的用户可以收到消息
*@param event_id       消息的编号，一般指函数码
*@param *reply_message 消息结构体，函数参数组合
*@description:         需要先订阅，才能收到 
*@precondition:
*@postcondition:
*/
ZOO_EXPORT ZOO_INT32 XX4I_publish_event(IN const MQ4A_SERV_ADDR server,
													IN ZOO_INT32 event_id,
													INOUT XX4I_REPLY_STRUCT *reply_message);

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
ZOO_EXPORT ZOO_INT32 XX4I_send_subscribe(IN const MQ4A_SERV_ADDR server,
													IN MQ4A_EVENT_CALLBACK_FUNCTION callback_function,
													IN MQ4A_CALLBACK_STRUCT *callback_struct,
													IN ZOO_INT32 event_id,
													INOUT ZOO_HANDLE *handle,
													INOUT void *context);

/*
*@brief 取消订阅
*@param server   服务器地址
*@param event_id 请求消息
*@param handle   订阅输出句柄 
*@precondition:
*@postcondition:
*/
ZOO_EXPORT ZOO_INT32 XX4I_send_unsubscribe(IN const MQ4A_SERV_ADDR server,
													IN ZOO_INT32 event_id,
													IN ZOO_HANDLE handle);

/*
*@brief 发送信号消息
*@param server  服务器地址
*@param message 请求消息
*@param message_length   请求消息长度
*@precondition:
*@postcondition:
*/
ZOO_EXPORT ZOO_INT32 XX4I_send_signal(IN const MQ4A_SERV_ADDR server,
													IN void * message,
													IN ZOO_INT32 message_length);

#endif // XX4I_if.h

