/*******************************************************************************
* Copyright (C) 2017, shanghai NIO ltd
* All rights reserved.
* Product: ZOO
* Module: ZOO
* Component id: XX
* File name: XX4A_type.h
* Description: data definition for XX
* History recorder:
* Version   date           author            context
* 1.0       2018-04-21     weiwang.sun       created
******************************************************************************/
#ifndef XX4A_TYPE_H
#define XX4A_TYPE_H
#include <ZOO.h>
#include <XX4A_type.h>

/*
*@brief define component id to specify this model for log
*/	
#ifndef COMPONENT_ID_XX
#define COMPONENT_ID_XX "XX"
#endif

/*
*@brief define error code 
*/
#define XX4A_BASE_ERR               (0x58580000)
#define XX4A_SYSTEM_ERR             ((XX4A_BASE_ERR) + 0x01)
#define XX4A_PARAMETER_ERR          ((XX4A_BASE_ERR) + 0x02)
#define XX4A_TIMEOUT_ERR            ((XX4A_BASE_ERR) + 0x03)
#define XX4A_ILLEGAL_CALL_ERROR     ((XX4A_BASE_ERR) + 0x04)

/*
*@brief define state machine 
*/
typedef enum
{
    XX4A_STRATE_MIN = 0,
    XX4A_STRATE_TERMINATE,//上电状态/维修状态
    XX4A_STRATE_IDLE,//初始化完成状态
	XX4A_STRATE_BUSY,//切入运营状态
	XX4A_STRATE_UNKNOWN,//运行错误状态
    XX4A_COMMAND_MAX
}XX4A_STATE_ENUM;

//设备数量枚举
typedef enum
{
    XX4A_DEVICD_ID_MIN = 0,
    XX4A_DEVICD_ID_1,//第一个设备
    XX4A_DEVICD_ID_2,/* xxx */
	XX4A_DEVICD_ID_3,//
	XX4A_DEVICD_ID_4,//
    XX4A_DEVICD_ID_MAX
}XX4A_DEVICD_ID_ENUM;

//设备状态枚举
typedef struct
{
	XX4A_STATE_ENUM state;//状态机
	ZOO_BOOL on_line;//是否在线	
}XX4A_STATUS_STRUCT;

#endif