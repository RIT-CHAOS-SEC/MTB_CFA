
#ifndef MTB_H
#define MTB_H

#include <arm_cmse.h>

#define MTB_BASE_addr 						0xE0043000
#define MTB_MASTER_EN_MASK 				1<<31
#define MTB_MASTER_NSEN_MASK 			1<<30
#define MTB_MASTER_HALTREQ_MASK 	1<<9
#define MTB_MASTER_RAMPRIV_MASK 	1<<8
#define MTB_MASTER_TSTOPEN_MASK 	1<<6
#define MTB_MASTER_TSTARTEN_MASK 	1<<5
#define MTB_MASTER_HALTREQ_MASK 	1<<9
#define MTB_MASTER_MASK_MASK 			0b1111
#define MTB_FLOW_WATERMARK_MASK 	~(0b1111)
#define MTB_FLOW_AUTOHALT_MASK 	0b10
#define MTB_FLOW_AUTOSTOP_MASK 	0b01

#define MTB_BASE_MASK 	~(0b11111)


typedef struct MTB_struct{
	uint32_t MTB_POSITION;
	uint32_t MTB_MASTER;
	uint32_t MTB_FLOW;
	uint32_t MTB_BASE;
	uint32_t MTB_TSTART;		
	uint32_t MTB_TSTOP;
	uint32_t MTB_SECURE;	
} MTB_struct;

#endif