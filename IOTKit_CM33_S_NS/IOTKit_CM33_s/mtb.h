
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

#define MTB_BUFFER_SIZE 1024

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


#define DWT_BASE_addr 0xE0001000


#define DWT_FUNCTION_DATAVSIZE_OFFSET   10
#define DWT_FUNCTION_ACTION_OFFSET      4
#define DWT_FUNCTION_MATCHED_OFFSET     24
#define DWT_FUNCTION_MATCH_OFFSET       0

#define DWT_FUNCTION_DATAVSIZE_MASK     0b11 << DWT_FUNCTION_DATAVSIZE_OFFSET
#define DWT_FUNCTION_ACTION_MASK        0b11 << DWT_FUNCTION_ACTION_OFFSET
#define DWT_FUNCTION_MATCHED_MASK       0b1 << DWT_FUNCTION_MATCHED_OFFSET
#define DWT_FUNCTION_MATCH_MASK         0b1111 <<  DWT_FUNCTION_MATCH_OFFSET

typedef struct DWT_struct{
	uint32_t DWT_CTRL;
	uint32_t DWT_CYCCNT;
	uint32_t DWT_CPICNT;
	uint32_t DWT_EXCCNT;
	uint32_t DWT_SLEEPCNT;
	uint32_t DWT_LSUCNT;
	uint32_t DWT_FOLDCNT;
	uint32_t DWT_PCSR;
	uint32_t DWT_COMP0[2];
	uint32_t DWT_FUNCTION0[2];
	uint32_t DWT_COMP1[2];
	uint32_t DWT_FUNCTION1[2];
	uint32_t DWT_COMP2[2];
	uint32_t DWT_FUNCTION2[2];
	uint32_t DWT_COMP3[2];
	uint32_t DWT_FUNCTION3[2];
	// uint8_t DWT_DEVARCH;
	// uint16_t DWT_DEVTYPE;
	// uint32_t DWT_PID4;
	// uint32_t DWT_PID5;
	// uint16_t DWT_PID6;
	// uint16_t DWT_PID7;
	// uint32_t DWT_PIDR0;
	// uint32_t DWT_PIDR1;
	// uint16_t DWT_PIDR2;
	// uint16_t DWT_PIDR3;
	// uint32_t DWT_CIDR0;
	// uint32_t DWT_CIDR1;
	// uint16_t DWT_CIDR2;
	// uint16_t DWT_CIDR3;
}DWT_struct;



#endif

