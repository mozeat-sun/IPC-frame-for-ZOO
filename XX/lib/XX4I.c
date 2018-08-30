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
@brief ��ȡ������Ϣ���ȡ��ֽڡ�
*@param function_code   ������
*@param *message_length �ֽڳ��� 
*@precondition:
*@postcondition:
*/
ZOO_INT32 XX4I_get_request_message_length(IN ZOO_INT32 function_code,
													INOUT ZOO_INT32 *message_length )
{    ZOO_INT32 result = OK;
    /* ����������ָ���Ƿ�?*/
    if ( NULL == message_length )
    {
        result = XX4A_PARAMETER_ERR;
        EH4A_show_exception(COMPONENT_ID_XX, __FILE__, __ZOO_FUNC__, __LINE__,result,"request msg length is NULL.");
    }
    else
    {
        *message_length = 0;
    }
    /*��ѯ����������Ϣ�ĳ���*/
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
@brief ��ȡ�ش���Ϣ���ȡ��ֽڡ�
*@param function_code   ������
*@param *message_length �ֽڳ��� 
*@precondition:
*@postcondition:
*/
ZOO_INT32 XX4I_get_reply_message_length(IN ZOO_INT32 function_code,
													INOUT ZOO_INT32 *message_length )
{    ZOO_INT32 result = OK;
    /* ����������ָ���Ƿ�?*/
    if ( NULL == message_length )
    {
        result = XX4A_PARAMETER_ERR;
        EH4A_show_exception(COMPONENT_ID_XX, __FILE__,__ZOO_FUNC__,__LINE__,result,"request msg length is NULL.");
    }
    else
    {
        *message_length = 0;
    }
    /*��ѯ����������Ϣ�ĳ���*/
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
*@brief ��Ŀ���ַ������Ϣ������÷�����Ϣ��ͬ���ӿڣ����������÷�
*@param MQ4A_SERV_ADDR   ��������ַ
*@param *request_message ������Ϣ
*@param *reply_message   �ظ���Ϣ
*@param timeout          ������Ϣ��ȴ���ʱʱ�� 
*@precondition:
*@postcondition: 
*/
ZOO_INT32 XX4I_send_request_and_reply(IN const MQ4A_SERV_ADDR server,
													IN XX4I_REQUEST_STRUCT  *request_message,
													INOUT XX4I_REPLY_STRUCT *reply_message,
													IN ZOO_INT32 timeout)
{
    ZOO_INT32 result = OK;
    ZOO_INT32 request_length = 0;/*������Ϣ��*/
    ZOO_INT32 reply_length = 0;/*Ӧ�ý�����Ϣ����*/
    ZOO_INT32 actual_reply_length = 0;/*ʵ�ʽ������ݳ���*/

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
*@brief ��Ŀ���ַ������Ϣ���첽�ӿڣ������������XX4I_receive_reply_message
*@param MQ4A_SERV_ADDR   ��������ַ
*@param *request_message ������Ϣ 
*@precondition:
*@postcondition:
*/
ZOO_INT32 XX4I_send_request_message(IN const MQ4A_SERV_ADDR server,
													IN XX4I_REQUEST_STRUCT *request_message)

{
    ZOO_INT32 result = OK;
    ZOO_INT32 request_length = 0;/* ���͵���Ϣ���� */
    /*��ѯ����������Ϣ�ĳ���*/
    if ( OK == result )
    {
        result = XX4I_get_request_message_length(request_message->request_header.function_code, &request_length );

    }

    /*������Ϣ*/
    if ( OK == result )
    {
        result = MQ4A_send_request( server,				 /*����Ŀ���������ַ*/
                                    request_message,					 /*������Ϣ��*/
                                    request_length,						 /*������Ϣ��*/
                                    XX4I_RETRY_INTERVAL );           /*���ͼ��ʱ*/
    }

    return result;
}

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
ZOO_INT32 XX4I_receive_reply_message(IN const MQ4A_SERV_ADDR server,
													IN ZOO_INT32 function_code,
													INOUT XX4I_REPLY_STRUCT *reply_message,
													IN ZOO_INT32 timeout)
{
    ZOO_INT32 result = OK;
    ZOO_INT32 actual_replay_length = 0;    /*ʵ�ʽ������ݳ���*/
    ZOO_INT32 reply_length = 0; /*Ӧ�ý��ճ���*/
    result = XX4I_get_reply_message_length( function_code, &reply_length );
    /*���շ�����Ϣ*/
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
*@brief ��Ŀ���ַ������Ϣ�����ĵ��û������յ���Ϣ
*@param event_id       ��Ϣ�ı�ţ�һ��ָ������
*@param *reply_message ��Ϣ�ṹ�壬�����������
*@description:         ��Ҫ�ȶ��ģ������յ� 
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
*@brief ȡ������
*@param server   ��������ַ
*@param event_id ������Ϣ
*@param handle   ���������� 
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
*@brief �����ź���Ϣ
*@param server  ��������ַ
*@param message ������Ϣ
*@param message_length   ������Ϣ����
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

