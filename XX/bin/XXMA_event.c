/***********************************************************
 * Copyright (C) 2018, shanghai NIO CO. ,LTD
 * All rights reserved.
 * Product        : ZOO
 * Component id   : XX
 * File Name      : XXMA_event.c
 * Description    : {Summary Description}
 * History        : 
 * Version        date          auther         context 
 * V1.0.0         2018-08-27    Generator      created
*************************************************************/
#include "XXMA_event.h"

/**
 *@brief XXMA_raise_4A_initialize
 *@param device_id
**/
ZOO_INT32 XXMA_raise_4A_initialize(IN ZOO_INT32 error_code,IN XX4I_REPLY_STRUCT * reply)
{
    ZOO_INT32 rtn = OK;
    if(reply == NULL)
    {
        rtn = XX4A_PARAMETER_ERR;
    }

    if(OK == rtn)
    {
        reply->reply_header.execute_result = error_code;
    }
    return rtn;
}

/**
 *@brief XXMA_raise_4A_get_status
 *@param device_id
 *@param status
**/
ZOO_INT32 XXMA_raise_4A_get_status(IN ZOO_INT32 error_code,IN XX4A_STATUS_STRUCT status,IN XX4I_REPLY_STRUCT * reply)
{
    ZOO_INT32 rtn = OK;
    if(reply == NULL)
    {
        rtn = XX4A_PARAMETER_ERR;
    }

    if(OK == rtn)
    {
        reply->reply_header.execute_result = error_code;
        memcpy(&reply->reply_body.get_status_rep_msg.status,&status,sizeof(XX4A_STATUS_STRUCT));
    }
    return rtn;
}

/**
 *@brief XX4A_status_info_subscribe
 *@param status
 *@param error_code
 *@param *context
**/
void XXMA_raise_4A_status_info_subscribe(IN XX4A_STATUS_STRUCT status,IN ZOO_INT32 error_code,IN void *context)
{
    ZOO_INT32 rtn = OK;
    XX4I_REPLY_STRUCT * reply_message = NULL;
    reply_message = (XX4I_REPLY_STRUCT * ) MM4A_malloc(sizeof(XX4I_REPLY_STRUCT));
    if(NULL == reply_message)
    {
        rtn = XX4A_PARAMETER_ERR;
    }
    
    if(OK == rtn)
    {
        reply_message->reply_header.function_code = XX4A_STATUS_INFO_SUBSCRIBE_CODE;
        reply_message->reply_header.execute_result = error_code;
        memcpy(&reply_message->reply_body.status_info_subscribe_code_rep_msg.status,&status,sizeof(XX4A_STATUS_STRUCT));
    }

    if(OK == rtn)
    {
        rtn = XX4I_publish_event(XX4A_SERVER,
                                            XX4A_STATUS_INFO_SUBSCRIBE_CODE,
                                            reply_message);
    }

    if(OK != rtn)
    {
        EH4A_show_exception(COMPONENT_ID_XX, __FILE__, __ZOO_FUNC__, __LINE__,rtn,"publish_event failed.");
    }
    MM4A_free(reply_message);
    return ;
}
/**
 *@brief XXMA_raise_4A_set_const_name
 *@param name
 *@param p[64]
**/
ZOO_INT32 XXMA_raise_4A_set_const_name(IN ZOO_INT32 error_code,IN char p[64],IN XX4I_REPLY_STRUCT * reply)
{
    ZOO_INT32 rtn = OK;
    if(reply == NULL)
    {
        rtn = XX4A_PARAMETER_ERR;
    }

    if(OK == rtn)
    {
        reply->reply_header.execute_result = error_code;
        memcpy(&reply->reply_body.set_const_name_rep_msg.p[0],&p[0],sizeof(char) * 64);
    }
    return rtn;
}

/**
 *@brief XXMA_raise_4A_get_name
 *@param name[16][8]
**/
ZOO_INT32 XXMA_raise_4A_get_name(IN ZOO_INT32 error_code,IN ZOO_CHAR name[16][8],IN XX4I_REPLY_STRUCT * reply)
{
    ZOO_INT32 rtn = OK;
    if(reply == NULL)
    {
        rtn = XX4A_PARAMETER_ERR;
    }

    if(OK == rtn)
    {
        reply->reply_header.execute_result = error_code;
        memcpy(&reply->reply_body.get_name_rep_msg.name[0],&name[0],sizeof(ZOO_CHAR) * 16 * 8);
    }
    return rtn;
}

/**
 *@brief XXMA_raise_4A_set_name
 *@param name[16]
**/
ZOO_INT32 XXMA_raise_4A_set_name(IN ZOO_INT32 error_code,IN XX4I_REPLY_STRUCT * reply)
{
    ZOO_INT32 rtn = OK;
    if(reply == NULL)
    {
        rtn = XX4A_PARAMETER_ERR;
    }

    if(OK == rtn)
    {
        reply->reply_header.execute_result = error_code;
    }
    return rtn;
}

/**
 *@brief XXMA_raise_4A_start_sig
 *@param name[16]
**/
ZOO_INT32 XXMA_raise_4A_start_sig(IN ZOO_INT32 error_code,IN XX4I_REPLY_STRUCT * reply)
{
    ZOO_INT32 rtn = OK;
    if(reply == NULL)
    {
        rtn = XX4A_PARAMETER_ERR;
    }

    if(OK == rtn)
    {
        reply->reply_header.execute_result = error_code;
    }
    return rtn;
}


