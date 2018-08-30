/*******************************************************************************
* Copyright (C) 2018, shanghai NIO ltd
* All rights reserved.
* Product: ZOO
* Module: XX
* Component id: XX
* File name: XX4A_if.h
* Description: interface for message queue
* History recorder:
* Version   date           author            context
* 1.0       2018-04-21     weiwang.sun       created
******************************************************************************/
#ifndef XX4A_IF_H
#define XX4A_IF_H
#include <ZOO.h>
#include <XX4A_type.h>

/**************************************************************************
INTERFACE <ZOO_INT32 XX4A_initialize>
{
<InterfaceType>:FUNCTION<Blocking/NonBlocking/callback_function>
<Parameters>
    IN:         notype none
    OUT:        notype none
    INOUT:      notype none
<Timeout>:      60
<Server>:       Default
<Returns>:      OK -- success
				XX4A_ILLEGAL_CALL_ERROR --illegal call
                XX4A_SYSTEM_ERR -- system error
                XX4A_TIMEOUT_ERR -- timeout error
                XX4A_PARAMETER_ERR -- parameters error
<Description>:       
			PRECONDITION:
			POSTCONDITION:
**************************************************************************/
ZOO_EXPORT ZOO_INT32 XX4A_initialize(IN XX4A_DEVICD_ID_ENUM device_id);/*同步函数,阻塞*/
ZOO_EXPORT ZOO_INT32 XX4A_initialize_req(IN XX4A_DEVICD_ID_ENUM device_id);/*异步请求，非阻塞，以 _req 为标志*/
ZOO_EXPORT ZOO_INT32 XX4A_initialize_wait(IN ZOO_INT32 timeout);/*异步请求结果，阻塞 _wait 为标志*/
		
/**************************************************************************
INTERFACE <ZOO_INT32 XX4A_get_status>
{
<InterfaceType>:FUNCTION<Blocking/NonBlocking/callback_function>
<Parameters>
    IN:         notype none
    OUT:        notype none
    INOUT:      XX4A_STATUS_STRUCT *status 
<Timeout>:      60
<Server>:       Default
<Returns>:      OK -- success
				XX4A_ILLEGAL_CALL_ERROR --illegal call
                XX4A_SYSTEM_ERR -- system error
                XX4A_TIMEOUT_ERR -- timeout error
                XX4A_PARAMETER_ERR -- parameters error
<Description>:            
			PRECONDITION:
			POSTCONDITION:
**************************************************************************/
ZOO_EXPORT ZOO_INT32 XX4A_get_status(IN XX4A_DEVICD_ID_ENUM device_id,INOUT XX4A_STATUS_STRUCT *status);
ZOO_EXPORT ZOO_INT32 XX4A_get_status_req(IN XX4A_DEVICD_ID_ENUM device_id);
ZOO_EXPORT ZOO_INT32 XX4A_get_status_wait(INOUT XX4A_STATUS_STRUCT *status,
											IN ZOO_INT32 timeout);
	
/**************************************************************************
INTERFACE <ZOO_INT32 XX4A_status_info_subscribe>
{
<InterfaceType>:EVENT<>
<Parameters>
    IN:		  XX4A_STATUS_CALLBACK_FUNCTION callback_function	  
    IN:		  notype none	 
    OUT:	  ZOO_UINT32 *handle	 
    INOUT:	  INOUT void *context_p	  
<Timeout>:	  60
<Server>: 	  none
<Returns>:	  OK -- success
			  XX4A_ILLEGAL_CALL_ERROR --illegal call
			  XX4A_PARAMETER_ERROR	  --parameters error
			  XX4A_SYSTEM_ERROR 	  --system error
			  XX4A_TIMEOUT_ERROR	  --timeout error
<Description>: 
}
**************************************************************************/
typedef void(*XX4A_STATUS_CALLBACK_FUNCTION)(IN XX4A_STATUS_STRUCT status,
								  IN ZOO_INT32 error_code,
								  IN void *context);

ZOO_EXPORT ZOO_INT32 XX4A_status_info_subscribe(IN XX4A_STATUS_CALLBACK_FUNCTION callback_function,
												  OUT ZOO_UINT32 *handle,
												  INOUT void *context);

ZOO_EXPORT ZOO_INT32 XX4A_status_info_unsubscribe(IN ZOO_UINT32 handle);	

ZOO_EXPORT ZOO_INT32 XX4A_set_const_name(IN const ZOO_CHAR * name,OUT char p[64]);

ZOO_EXPORT ZOO_INT32 XX4A_get_name(OUT ZOO_CHAR name[16][8]);

ZOO_EXPORT ZOO_INT32 XX4A_set_name(IN ZOO_CHAR name[16]);

ZOO_EXPORT ZOO_INT32 XX4A_start_sig(IN ZOO_CHAR name[16]);
#endif


