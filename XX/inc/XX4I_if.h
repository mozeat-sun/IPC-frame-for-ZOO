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
@brief ��ȡ������Ϣ���ȡ��ֽڡ�
*@param function_code   ������
*@param *message_length �ֽڳ��� 
*@precondition:
*@postcondition:
*/
ZOO_EXPORT ZOO_INT32 XX4I_get_request_message_length(IN ZOO_INT32 function_code,
													INOUT ZOO_INT32 *message_length );

/*
@brief ��ȡ�ش���Ϣ���ȡ��ֽڡ�
*@param function_code   ������
*@param *message_length �ֽڳ��� 
*@precondition:
*@postcondition:
*/
ZOO_EXPORT ZOO_INT32 XX4I_get_reply_message_length(IN ZOO_INT32 function_code,
													INOUT ZOO_INT32 *message_length );

/*
*@brief ��Ŀ���ַ������Ϣ������÷�����Ϣ��ͬ���ӿڣ����������÷�
*@param MQ4A_SERV_ADDR   ��������ַ
*@param *request_message ������Ϣ
*@param *reply_message   �ظ���Ϣ
*@param timeout          ������Ϣ��ȴ���ʱʱ�� 
*@precondition:
*@postcondition: 
*/
ZOO_EXPORT ZOO_INT32 XX4I_send_request_and_reply(IN const MQ4A_SERV_ADDR server,
													IN XX4I_REQUEST_STRUCT  *request_message,
													INOUT XX4I_REPLY_STRUCT *reply_message,
													IN ZOO_INT32 timeout);

/*
*@brief ��Ŀ���ַ������Ϣ���첽�ӿڣ������������XX4I_receive_reply_message
*@param MQ4A_SERV_ADDR   ��������ַ
*@param *request_message ������Ϣ 
*@precondition:
*@postcondition:
*/
ZOO_EXPORT ZOO_INT32 XX4I_send_request_message(IN const MQ4A_SERV_ADDR server,
													IN XX4I_REQUEST_STRUCT *request_message);

/*
*@brief ����Ŀ����Ϣ
	*@param server         ��������ַ
*@param function_code  ������
*@param *reply_message ������Ϣ
*@param timeout        ��ʱʱ��
*@description:         �첽�ӿڣ����XX4I_send_request_messageһ��ʹ��
*@precondition:
*@postcondition:
*/
ZOO_EXPORT ZOO_INT32 XX4I_receive_reply_message(IN const MQ4A_SERV_ADDR server,
													IN ZOO_INT32 function_code,
													INOUT XX4I_REPLY_STRUCT *reply_message,
													IN ZOO_INT32 timeout);

/*
*@brief ��Ŀ���ַ������Ϣ�����ĵ��û������յ���Ϣ
*@param event_id       ��Ϣ�ı�ţ�һ��ָ������
*@param *reply_message ��Ϣ�ṹ�壬�����������
*@description:         ��Ҫ�ȶ��ģ������յ� 
*@precondition:
*@postcondition:
*/
ZOO_EXPORT ZOO_INT32 XX4I_publish_event(IN const MQ4A_SERV_ADDR server,
													IN ZOO_INT32 event_id,
													INOUT XX4I_REPLY_STRUCT *reply_message);

/*
*@brief ���Ͷ�����Ϣ
*@param server            ��������ַ
*@param callback_function ���ػص�������
*@param callback_struct   �ӿڻص��ṹ��
*@param event_id          ������Ϣ
*@param *handle           ����������
*@param *context          �����ı�ʶ
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
*@brief ȡ������
*@param server   ��������ַ
*@param event_id ������Ϣ
*@param handle   ���������� 
*@precondition:
*@postcondition:
*/
ZOO_EXPORT ZOO_INT32 XX4I_send_unsubscribe(IN const MQ4A_SERV_ADDR server,
													IN ZOO_INT32 event_id,
													IN ZOO_HANDLE handle);

/*
*@brief �����ź���Ϣ
*@param server  ��������ַ
*@param message ������Ϣ
*@param message_length   ������Ϣ����
*@precondition:
*@postcondition:
*/
ZOO_EXPORT ZOO_INT32 XX4I_send_signal(IN const MQ4A_SERV_ADDR server,
													IN void * message,
													IN ZOO_INT32 message_length);

#endif // XX4I_if.h

