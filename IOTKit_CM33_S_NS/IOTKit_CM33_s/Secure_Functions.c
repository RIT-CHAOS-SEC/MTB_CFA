
#include "Secure_Functions.h"
#include "cfa.h"
#include <stdint.h>
#include "core_cm33.h"

// define callback functions
NonSecure_fpVoid fNSFunc = (NonSecure_fpVoid)NULL;

#define MEMORY_REGION_CFA_START 0x20000000U
#define MEMORY_REGION_CFA_END   0x20010000U
#define TRUE 1
#define FALSE 0

NSENTRY void SECURE_register_callback(void* callback)
{
    // check if callback is a valid address
    if (callback == NULL | callback < MEMORY_REGION_CFA_START | callback > MEMORY_REGION_CFA_END)
    {
        return;
    }

    fNSFunc = (NonSecure_fpVoid) callback;
    return;
}

uint32_t CFA_stat = FALSE;

uint8_t _set_stat(){
    // disable interrupt
    __disable_irq();
    if (CFA_stat == TRUE)
    {
        __enable_irq();
        return 1;
    }
    // set the status
    CFA_stat = TRUE;
    // enable interrupt
    __enable_irq();
    return 0;
}

void _clear_stat(){
    // disable interrupt
    __disable_irq();
    // clear the status
    CFA_stat = FALSE;
    // enable interrupt
    __enable_irq();
}

NSENTRY void SECURE_start_cfa(CFReport * report){

    __disable_irq();
    // check if callback function is defined
    if (fNSFunc == NULL)
    {
        report->status = CFA_STATUS_ERROR;
        __enable_irq();
        return;
    }
    __enable_irq();

    // initialize cfa process
    if(_set_stat())return; 

    eCFA_init_cfa(report);

    _clear_stat();
    
    return;
}


