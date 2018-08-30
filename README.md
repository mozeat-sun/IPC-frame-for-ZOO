# IPC-frame-for-ZOO
a python script for auto generate IPC frame code according header file

Rules:
  							进程间通信代码框架规范
每个组件需提供2个头文件：
接口头文件：XX4A_if.h
数据结构头文件：XX4A_type.h
一、接口规范(XX4A_if.h)
1、	组件名称必须是XX4A_/XX4T_，XX必须是2个字符以上,XX需要大写；
例如：XX4A_initialize();XXXX4A_initialize()；
4A是：for application：为运营和应用使用，接口必须有安全保护，并且能够为运营UI使用
4T是：for test：开发人员使用或者设备测试使用，方便编写测试UI，一般情况下不允许嵌入到运营的UI，主要原因：测试接口有可能不是项目需求，测试接口可靠性不高，安全性不够；

2、	异步请求：以_req结尾，例如XX4A_initialize_req();

3、	函数必须以 ZOO_EXPORT 开头；

4、	异步获取结果:以_wait为结尾，例如XX4A_initialize_wait();

5、	订阅回调函数指针：以XX4A_开头，以_CALLVACK_FUNCTION结尾，下划线，大写；

例如	：XX4A_STATUS_CALLBACK_FUNCTION
回调函数模板：
typedef void(*XX4A_STATUS_CALLBACK_FUNCTION)(IN XX4A_STATUS_STRUCT status,
								  IN ZOO_INT32 error_code,
								      IN void *context);

6、	订阅/取消订阅：以_subscribe/_unsubscribe为结尾，例如XX4A_status_info_subscribe(IN XX4A_STATUS_CALLBACK_FUNCTION callback_function, OUT ZOO_UINT32 *handle, INOUT void *context)/XX4A_status_info_unsubscribe()；

7、	接口参数必须标明是输入还是输出：IN/OUT/INOUT

二、数据结构

1、每个XX组件提供：XX4A_STATUS_STRUCT接口体，用于订阅数据；

	例如：

	typedef struct

	{
		XX4A_STATE_ENUM state;//状态机
	
		ZOO_BOOL on_line;//是否在线	
	
	}XX4A_STATUS_STRUCT;

2、提供错误定义

	错误码定义：每个组件按照ascii的值进行错误码定义，例如X的ascii码为X，那么XX的错误码定义：0x58580000
	
	每个组件必须提供以下错误码（用于通信端错误码提示）：
	
	#define XX4A_BASE_ERR               (0x58580000)
	
	#define XX4A_SYSTEM_ERR             ((XX4A_BASE_ERR) + 0x01)

	#define XX4A_PARAMETER_ERR          ((XX4A_BASE_ERR) + 0x02)

	#define XX4A_TIMEOUT_ERR            ((XX4A_BASE_ERR) + 0x03)

	#define XX4A_ILLEGAL_CALL_ERROR      ((XX4A_BASE_ERR) + 0x04)

	其他错误码可以在此基础上增加，错误码模块之间不能重叠

3、提供组件名称宏定义：用于trace打印组件
	#ifndef COMPONENT_ID_XX
#define COMPONENT_ID_XX "XX"
#endif
三、组件目录结构
	XX-
		  -bin:内部实现源文件
          -com:内部公共头文件
		  -lib:外部调用源文件
	      -inc:对外头文件
          -test
	  
四、代码生成器（Code Generator）

	输入：XX4A_if.h/xx4a_type.h
	
	输出：
	
		-XX-
		
		  -bin:
		  
			  -XX4A_main.c:进程main函数
			  
              -XX4A_dispatch.c:消息分发组件
	      
              -XX4A_event.c:消息回答/订阅组件
	      
              -XX4A_implement.c:消息实现组件
	      
          -com:
              -XX4A_dispatch.h:
	      
              -XX4A_event.h:
	      
              -XX4A_implement.h:
	      
		  -lib:
		  
			  -XX4A.c:接口消息组包
			  
              -XX4I.c:接口消息发送与接收
	      
	      -inc:
	      
	          -XX4A_if.h
		  
              -XX4A_type.h
	      
          -test
	  
       -XX4A.mk
       
       -libXX4A.mk
       
