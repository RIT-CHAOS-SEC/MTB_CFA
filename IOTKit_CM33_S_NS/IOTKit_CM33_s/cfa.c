# include "cfa.h"
# include "mtb.h"
# include <stdint.h>
# include <string.h>
# include <stdio.h>

CFReport report_s;
typedef void (*NonSecure_fpVoid)(void) __attribute__((cmse_nonsecure_call));

uint8_t attestationKey[KEY_SIZE] = {0};

extern NonSecure_fpVoid fNSFunc;

error_t vCFA_copy_report(CFReport*report_ns){
    
    if( memcpy(report_ns, &report_s, sizeof(CFReport)) == NULL)
    {
        return CFA_STATUS_ERROR;
    }
    return CFA_STATUS_SUCCESS;
}

void vDebug_send_report_to_UART(){
    // todo
}

void vCFA_add_log(){
    //todo
}


error_t eCFA_init_cfa(CFReport *report_ns){
    

    printf("[LOG] CFA funtion entry\n");


    report_ns->status = CFA_STATUS_STARTED;
    
    if(memcmp(report_ns->challenge, report_s.challenge, sizeof(uint32_t) * CFA_CHALLANGE_SIZE))
    {
        report_ns->status = CFA_STATUS_FAILURE;
        return CFA_STATUS_FAILURE;
    }

    // clean the report
    memset(report_ns, 0, sizeof(CFReport));

    // hash the memory
    // todo

    // configure the MTB
    //todo

    printf("[LOG] CFA Calling Non Secure Function\n");
    // run the NSfunction
    fNSFunc();
    printf("[LOG] CFA Returned from Non Secure Function\n");

    // sign the report
    // todo

    // copy the report
    if(vCFA_copy_report(report_ns) == CFA_STATUS_ERROR)
    {
        report_ns->status = CFA_STATUS_ERROR;
        return CFA_STATUS_ERROR;
    }

    report_ns->status = CFA_STATUS_SUCCESS;

    vDebug_send_report_to_UART();

    printf("[LOG] CFA funtion exit\n");

    return CFA_STATUS_SUCCESS;
}