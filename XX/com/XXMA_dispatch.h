/***********************************************************
 * Copyright (C) 2018, shanghai NIO CO. ,LTD
 * All rights reserved.
 * Product        : ZOO
 * Component id   : XX
 * File Name      : XXMA_dispatch.h
 * Description    : {Summary Description}
 * History        : 
 * Version        date          auther         context 
 * V1.0.0         2018-08-27    Generator      created
*************************************************************/

#ifndef XXMA_DISPATCH_H
#define XXMA_DISPATCH_H
#include <ZOO.h>
#include <MQ4A_if.h>
#include <MQ4A_type.h>
#include <MM4A_if.h>
#include "XX4I_type.h"
#include "XX4A_type.h"
#include "XXMA_implement.h"

/**
*@brief dispatch message from client to server internal interface
*@param context        
*@param server        address
*@param msg           request message to server
*@param len           request message length
*@param reply_msg     reply message length to caller
*@param reply_msg_len reply message length
**/
ZOO_EXPORT void XXMA_callback_handler(void * context,const MQ4A_SERV_ADDR server,void * msg,ZOO_INT32 len,void ** reply_msg,ZOO_INT32 * reply_msg_len);

#endif // XXMA_dispatch.h
