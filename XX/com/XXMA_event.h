/***********************************************************
 * Copyright (C) 2018, shanghai NIO CO. ,LTD
 * All rights reserved.
 * Product        : ZOO
 * Component id   : XX
 * File Name      : XXMA_event.h
 * Description    : {Summary Description}
 * History        : 
 * Version        date          auther         context 
 * V1.0.0         2018-08-27    Generator      created
*************************************************************/
#ifndef XXMA_EVENT_H
#define XXMA_EVENT_H

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <ZOO.h>
#include <MQ4A_if.h>
#include <MQ4A_type.h>
#include <MM4A_if.h>
#include <EH4A_if.h>
#include <TR4A_if.h>
#include "XX4I_type.h"
#include "XX4A_type.h"

/**
 *@brief XXMA_raise_4A_initialize
 *@param device_id
**/
ZOO_EXPORT ZOO_INT32 XXMA_raise_4A_initialize(IN ZOO_INT32 error_code,IN XX4I_REPLY_STRUCT * reply);




/**
 *@brief XXMA_raise_4A_get_status
 *@param device_id
 *@param status
**/
ZOO_EXPORT ZOO_INT32 XXMA_raise_4A_get_status(IN ZOO_INT32 error_code,IN XX4A_STATUS_STRUCT status,IN XX4I_REPLY_STRUCT * reply);




/**
 *@brief XX4A_status_info_subscribe
 *@param status
 *@param error_code
 *@param *context
**/
ZOO_EXPORT void XXMA_raise_4A_status_info_subscribe(IN XX4A_STATUS_STRUCT status,IN ZOO_INT32 error_code,IN void *context);


/**
 *@brief XXMA_raise_4A_set_const_name
 *@param name
 *@param p[64]
**/
ZOO_EXPORT ZOO_INT32 XXMA_raise_4A_set_const_name(IN ZOO_INT32 error_code,IN char p[64],IN XX4I_REPLY_STRUCT * reply);


/**
 *@brief XXMA_raise_4A_get_name
 *@param name[16][8]
**/
ZOO_EXPORT ZOO_INT32 XXMA_raise_4A_get_name(IN ZOO_INT32 error_code,IN ZOO_CHAR name[16][8],IN XX4I_REPLY_STRUCT * reply);


/**
 *@brief XXMA_raise_4A_set_name
 *@param name[16]
**/
ZOO_EXPORT ZOO_INT32 XXMA_raise_4A_set_name(IN ZOO_INT32 error_code,IN XX4I_REPLY_STRUCT * reply);


/**
 *@brief XXMA_raise_4A_start_sig
 *@param name[16]
**/
ZOO_EXPORT ZOO_INT32 XXMA_raise_4A_start_sig(IN ZOO_INT32 error_code,IN XX4I_REPLY_STRUCT * reply);



#endif // XXMA_event.h
