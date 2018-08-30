/***********************************************************
 * Copyright (C) 2018, shanghai NIO CO. ,LTD
 * All rights reserved.
 * Product        : ZOO
 * Component id   : XX
 * File Name      : XXMA_main.c
 * Description    : {Summary Description}
 * History        : 
 * Version        date          auther         context 
 * V1.0.0         2018-08-27    Generator      created
*************************************************************/

#include <string.h>
#include <ZOO.h>
#include <MQ4A_if.h>
#include <MQ4A_type.h>
#include <MM4A_if.h>
#include "XX4I_type.h"
#include "XX4A_implement.h"
#include "XXMA_dispatch.h"


ZOO_INT32 main(int argc,char *argv[])
{
    ZOO_INT32 rtn = OK;
    /* ��������ַ */
    MQ4A_SERV_ADDR server_addr = {0};
    MQ4A_SERVER_MODE_ENUM server_mode = MQ4A_SERVER_MODE_SYNC;/* ͬ��ģʽ */
    if(argc >= 2 )
    {
        strncpy(server_addr, argv[1], strlen(argv[1]));
        server_addr[31]= '\0';
    }
    else
    {
        strncpy(server_addr,XX4A_SERVER,strlen(XX4A_SERVER));
    }
    /* ��ʼ��XXģ�飬���ڴ���ʵ��*/
    XX4A_startup();
    /* ��ʼ���ڴ�� */
    MM4A_initialize();
    if(OK == rtn)
    {
        /* ��ʼ�������� */
         rtn = MQ4A_server_initialize(server_addr,server_mode);/* ��ʼ������� */
    }
    if(OK == rtn)
    {
        /* ע�����˴�����Ϣ�ص����������ڽ��տͻ�����Ϣ��ת����������ڲ��ӿ� */
        rtn = MQ4A_register_event_handler(server_addr,XXMA_callback_handler);
    }
    if(OK == rtn)
    {
        /* ����˽����¼�����״̬ */
        rtn = MQ4A_enter_event_loop(server_addr);
    }
    /* ��ֹ����� */
    MQ4A_server_terminate(server_addr);
    MM4A_terminate();
    XX4A_shutdown();
    return rtn;
}
