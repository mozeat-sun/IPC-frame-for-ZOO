/***********************************************************
 * Copyright (C) 2018, shanghai NIO CO. ,LTD
 * All rights reserved.
 * Product        : ZOO
 * Component id   : XX
 * File Name      : XXMA_implement.c
 * Description    : {Summary Description}
 * History        : 
 * Version        date          auther         context 
 * V1.0.0         2018-08-27    Generator      created
*************************************************************/
#include "XXMA_implement.h"

/**
 *@brief startup system 
**/ 
void XX4A_startup(void)
{
    /** usr add */
}

/**
 *@brief shutdown system 
**/ 
void XX4A_shutdown(void)
{
    /** usr add */
}

/**
 *@brief XXMA_implement_4A_initialize
 *@param device_id
**/
ZOO_INT32 XXMA_implement_4A_initialize(IN XX4A_DEVICD_ID_ENUM device_id,IN XX4I_REPLY_STRUCT * reply)
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 rtn = OK;
    /* usr add ... BEGIN */


    /* usr add ... END*/
    XXMA_raise_4A_initialize(rtn,reply);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ... ");
    return rtn;
}

/**
 *@brief XXMA_implement_4A_get_status
 *@param device_id
 *@param status
**/
ZOO_INT32 XXMA_implement_4A_get_status(IN XX4A_DEVICD_ID_ENUM device_id,IN XX4I_REPLY_STRUCT * reply)
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 rtn = OK;
    XX4A_STATUS_STRUCT status;
    /* usr add ... BEGIN */


    /* usr add ... END*/
    XXMA_raise_4A_get_status(rtn,status,reply);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ... ");
    return rtn;
}

/**
 *@brief XXMA_implement_4A_set_const_name
 *@param name
 *@param p[64]
**/
ZOO_INT32 XXMA_implement_4A_set_const_name(IN const ZOO_CHAR * name,IN XX4I_REPLY_STRUCT * reply)
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 rtn = OK;
    char p[64];
    memset(&p[0],0,sizeof(char) * 64);
    /* usr add ... BEGIN */


    /* usr add ... END*/
    XXMA_raise_4A_set_const_name(rtn,p,reply);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ... ");
    return rtn;
}

/**
 *@brief XXMA_implement_4A_get_name
 *@param name[16][8]
**/
ZOO_INT32 XXMA_implement_4A_get_name(IN XX4I_REPLY_STRUCT * reply)
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 rtn = OK;
    ZOO_CHAR name[16][8];
    memset(&name[0],0,sizeof(ZOO_CHAR) * 16 * 8);
    /* usr add ... BEGIN */


    /* usr add ... END*/
    XXMA_raise_4A_get_name(rtn,name,reply);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ... ");
    return rtn;
}

/**
 *@brief XXMA_implement_4A_set_name
 *@param name[16]
**/
ZOO_INT32 XXMA_implement_4A_set_name(IN ZOO_CHAR name[16],IN XX4I_REPLY_STRUCT * reply)
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 rtn = OK;
    /* usr add ... BEGIN */


    /* usr add ... END*/
    XXMA_raise_4A_set_name(rtn,reply);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ... ");
    return rtn;
}

/**
 *@brief XXMA_implement_4A_start_sig
 *@param name[16]
**/
ZOO_INT32 XXMA_implement_4A_start_sig(IN ZOO_CHAR name[16],IN XX4I_REPLY_STRUCT * reply)
{
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "> function entry ... ");
    ZOO_INT32 rtn = OK;
    /* usr add ... BEGIN */


    /* usr add ... END */
    /* don't need reply */
    MM4A_free(reply);
    TR4A_trace( COMPONENT_ID_XX, __ZOO_FUNC__, "< function exit ... ");
    return rtn;
}


