/***********************************************************
 * Copyright (C) 2018, shanghai NIO CO. ,LTD
 * All rights reserved.
 * Product        : ZOO
 * Component id   : XX
 * File Name      : XXMA_implement.h
 * Description    : {Summary Description}
 * History        : 
 * Version        date          auther         context 
 * V1.0.0         2018-08-27    Generator      created
*************************************************************/
#ifndef XXMA_IMPLEMENT_H
#define XXMA_IMPLEMENT_H

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ZOO.h>
#include <MQ4A_if.h>
#include <MQ4A_type.h>
#include <MM4A_if.h>
#include <EH4A_if.h>
#include <TR4A_if.h>
#include "XXMA_event.h"
#include "XX4I_type.h"
#include "XX4A_type.h"


/**
 *@brief startup system 
**/
ZOO_EXPORT void XX4A_startup(void);

/**
 *@brief shutdown system 
**/
ZOO_EXPORT void XX4A_shutdown(void);

/**
 *@brief XXMA_implement_4A_initialize
 *@param device_id
**/
ZOO_EXPORT ZOO_INT32 XXMA_implement_4A_initialize(IN XX4A_DEVICD_ID_ENUM device_id,IN XX4I_REPLY_STRUCT * reply);

/**
 *@brief XXMA_implement_4A_get_status
 *@param device_id
 *@param status
**/
ZOO_EXPORT ZOO_INT32 XXMA_implement_4A_get_status(IN XX4A_DEVICD_ID_ENUM device_id,IN XX4I_REPLY_STRUCT * reply);

/**
 *@brief XXMA_implement_4A_set_const_name
 *@param name
 *@param p[64]
**/
ZOO_EXPORT ZOO_INT32 XXMA_implement_4A_set_const_name(IN const ZOO_CHAR * name,IN XX4I_REPLY_STRUCT * reply);

/**
 *@brief XXMA_implement_4A_get_name
 *@param name[16][8]
**/
ZOO_EXPORT ZOO_INT32 XXMA_implement_4A_get_name(IN XX4I_REPLY_STRUCT * reply);

/**
 *@brief XXMA_implement_4A_set_name
 *@param name[16]
**/
ZOO_EXPORT ZOO_INT32 XXMA_implement_4A_set_name(IN ZOO_CHAR name[16],IN XX4I_REPLY_STRUCT * reply);

/**
 *@brief XXMA_implement_4A_start_sig
 *@param name[16]
**/
ZOO_EXPORT ZOO_INT32 XXMA_implement_4A_start_sig(IN ZOO_CHAR name[16],IN XX4I_REPLY_STRUCT * reply);


#endif // XXMA_implement.h
