#include "mtb.h"
#include "core_cm33.h"

SCB_Type * SCB_ = ((SCB_Type *) SCB_BASE);

MTB_struct *mtb = (MTB_struct *) MTB_BASE_addr;
CoreDebug_Type * CoreDebug_ = ((CoreDebug_Type *)     DCB_BASE         );
DWT_Type * DWT_ = ((DWT_Type       *)     DWT_BASE         );
ITM_Type * ITM_ = ((ITM_Type       *)     ITM_BASE         ) ;

#define DWT_FUNCTION_ACTION_VALUE 0b10 << DWT_FUNCTION_ACTION_OFFSET       // Generate a data trace match
#define DWT_FUNCTION_DATAVSIZE_VALUE 0b10 << DWT_FUNCTION_DATAVSIZE_OFFSET // word size
#define DWT_FUNCTION_MATCH_VALUE 0b0011 << DWT_FUNCTION_MATCH_OFFSET       // Generate a match on the data value
#define DWT_FUNCTION_MODIFY_MASK (DWT_FUNCTION_MATCH_MASK | DWT_FUNCTION_DATAVSIZE_MASK | DWT_FUNCTION_ACTION_MASK)
#define DWT_FUNCTION_MODIFY_VALUE (DWT_FUNCTION_MATCH_VALUE | DWT_FUNCTION_DATAVSIZE_VALUE | DWT_FUNCTION_ACTION_VALUE)

#define START_INIT_MTB_ADDRESS  0x2007B8
#define START_END_MTB_ADDRESS   0x200830

#define STOP_INIT_MTB_ADDRESS   0x200750
#define STOP_END_MTB_ADDRESS    0x2007A8

// compile this function with -O3 flag
#pragma GCC push_options
#pragma GCC optimize ("-O3")

void mtb_setup_DWT()
{
    // Enable DWT
    CoreDebug_->DEMCR |= (DEMCR_TRCENA | DEMCR_MON_EN ); // Enable Trace and Debug
    
    ITM_->TCR |= (ITM_TCR_TXENA|ITM_TCR_ITMENA);

    // DWT_->COMP0 = (uint32_t) matmul;  // Initial Address
    DWT_->COMP0 = (uint32_t) START_INIT_MTB_ADDRESS;
    SET_BITS(DWT->COMP0,0,0,0b0);

    // DWT->COMP1 = (uint32_t) matmul2; // Final Address
    DWT_->COMP1 = (uint32_t) START_END_MTB_ADDRESS;
    SET_BITS(DWT->COMP1,0,0,0b0);     
    
    // DWT->COMP2 = (uint32_t) run;  // Initial Address
    DWT_->COMP2 = (uint32_t) STOP_INIT_MTB_ADDRESS;
    SET_BITS(DWT->COMP2,0,0,0b0);
    
    // DWT->COMP3 = (uint32_t) setup_DWT; // Final Address
    DWT_->COMP3 = (uint32_t) STOP_END_MTB_ADDRESS;
    SET_BITS(DWT->COMP3,0,0,0b0);
    
    // START SIGNAL
    // CMP0
    SET_BITS(DWT->FUNCTION0,10,11,0b00); // DATAVSIZE
    SET_BITS(DWT->FUNCTION0,4,5,0b00); // ACTION
    SET_BITS(DWT->FUNCTION0,0,3,0b0010); // MATCH

    // CMP1
    SET_BITS(DWT->FUNCTION1,10,11,0b00); // DATAVSIZE
    SET_BITS(DWT->FUNCTION1,4,5,0b11); // ACTION
    SET_BITS(DWT->FUNCTION1,0,3,0b0011); // MATCH

    // STOP SIGNAL
    // CMP2
    SET_BITS(DWT->FUNCTION2,10,11,0b00); // DATAVSIZE
    SET_BITS(DWT->FUNCTION2,4,5,0b00); // ACTION
    SET_BITS(DWT->FUNCTION2,0,3,0b0010); // MATCH

    // CMP3
    SET_BITS(DWT->FUNCTION3,10,11,0b00); // DATAVSIZE
    SET_BITS(DWT->FUNCTION3,4,5,0b11); // ACTION
    SET_BITS(DWT->FUNCTION3,0,3,0b0011); // MATCH
    return;
}


void mtb_cleanMTB(){
    uint32_t * ptr = (uint32_t *) mtb->MTB_BASE;
    for (int i = 0; i < MTB_BUFFER_SIZE; i++){
        ptr[i] = 0;
    }
}

void mtb_debugMonitorHandler(){
    if (mtb->MTB_FLOW == (MTB_WATERMARK_A)){
        mtb->MTB_FLOW = (MTB_WATERMARK_B);
    } else {
        mtb->MTB_FLOW = MTB_WATERMARK_A;
        mtb->MTB_POSITION = 0;
    }
    mtb->MTB_MASTER &= ~( 1U << 9 );
    mtb->MTB_MASTER &= ~( 1U << 31 );
    // mtb->MTB_FLOW &= ~(MTB_FLOW_AUTOSTOP_MASK|MTB_FLOW_AUTOHALT_MASK);

    // while(1){};
    return;
}

void mtb_setup_MTB(){
    // setup VTOR 
    uint32_t * VTOR = (uint32_t *) SCB_->VTOR;
    // VTOR[7] = (uint32_t) secureExceptionHandler;
    VTOR[12] = (uint32_t) mtb_debugMonitorHandler;


    // SCB_NS->VTOR = (uint32_t) VTOR;
    mtb_cleanMTB();
    mtb->MTB_TSTART |= 0b10;  // Set to use DWT_COMP1
    mtb->MTB_TSTOP  |= 0b1000;  // Set to use DWT_COMP3
    // mtb->MTB_FLOW = MTB_WATERMARK_A;
    mtb->MTB_POSITION = 0;
    mtb->MTB_MASTER |= MTB_MASTER_TSTARTEN_MASK;
    mtb->MTB_MASTER |= MTB_MASTER_MASK_MASK;
    return;
}

#pragma GCC pop_options

void mtb_init(){
	mtb_setup_DWT();
	mtb_setup_MTB();
	return;
}

void mtb_exit(){
    
    // clean mtb buffer
    mtb_cleanMTB();
    
    // deactivate MTB
    mtb->MTB_MASTER &= ~(1U << 5);
    mtb->MTB_MASTER &= ~(1U << 9);
    mtb->MTB_MASTER &= ~(1U << 31);

    // deactivate DWT
    DWT_->COMP0 = 0;
    DWT_->COMP1 = 0;
    DWT_->COMP2 = 0;
    DWT_->COMP3 = 0;
    DWT_->FUNCTION0 = 0;
    DWT_->FUNCTION1 = 0;
    DWT_->FUNCTION2 = 0;
    DWT_->FUNCTION3 = 0;
    
    return;
}