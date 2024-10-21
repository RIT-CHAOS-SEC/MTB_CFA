/*----------------------------------------------------------------------------
 * Name:    main_s.c
 * Purpose: Main function secure mode
 *----------------------------------------------------------------------------*/

#include "RTE_Components.h" /* Component selection */
#include <arm_cmse.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include CMSIS_device_header
#include "Board_GLCD.h"  /* ::Board Support:Graphic LCD */
#include "Board_LED.h"   /* ::Board Support:LED */
#include "GLCD_Config.h" /* Keil.V2M-MPS2 IOT-Kit::Board Support:Graphic LCD */
#include "mtb.h"
#include "core_cm33.h"

/* Start address of non-secure application */
#define NONSECURE_START (0x00200000u)

extern GLCD_FONT GLCD_Font_16x24;

extern int stdout_init(void);

/* typedef for NonSecure callback functions */
typedef int32_t (*NonSecure_fpParam)(uint32_t)
    __attribute__((cmse_nonsecure_call));
typedef void (*NonSecure_fpVoid)(void) __attribute__((cmse_nonsecure_call));

char text[] = "Hello World (secure)\r\n";

/*----------------------------------------------------------------------------
  NonSecure callback functions
 *----------------------------------------------------------------------------*/
extern NonSecure_fpParam pfNonSecure_LED_On;
NonSecure_fpParam pfNonSecure_LED_On = (NonSecure_fpParam)NULL;
extern NonSecure_fpParam pfNonSecure_LED_Off;
NonSecure_fpParam pfNonSecure_LED_Off = (NonSecure_fpParam)NULL;

/*----------------------------------------------------------------------------
  Secure functions exported to NonSecure application
 *----------------------------------------------------------------------------*/
int32_t Secure_LED_On(uint32_t num) __attribute__((cmse_nonsecure_entry));
int32_t Secure_LED_On(uint32_t num) { return LED_On(num); }

int32_t Secure_LED_Off(uint32_t num) __attribute__((cmse_nonsecure_entry));
int32_t Secure_LED_Off(uint32_t num) { return LED_Off(num); }

void Secure_printf(char *pString) __attribute__((cmse_nonsecure_entry));
void Secure_printf(char *pString) { printf("%s", pString); }

/*----------------------------------------------------------------------------
  Secure function for NonSecure callbacks exported to NonSecure application
 *----------------------------------------------------------------------------*/
int32_t Secure_LED_On_callback(NonSecure_fpParam callback)
    __attribute__((cmse_nonsecure_entry));
int32_t Secure_LED_On_callback(NonSecure_fpParam callback)
{
    pfNonSecure_LED_On = callback;
    return 0;
}

int32_t Secure_LED_Off_callback(NonSecure_fpParam callback)
    __attribute__((cmse_nonsecure_entry));
int32_t Secure_LED_Off_callback(NonSecure_fpParam callback)
{
    pfNonSecure_LED_Off = callback;
    return 0;
}

/*----------------------------------------------------------------------------
  SysTick IRQ Handler
 *----------------------------------------------------------------------------*/
void SysTick_Handler(void);
void SysTick_Handler(void)
{
    static uint32_t ticks = 0;
    static uint32_t ticks_printf = 0;

    switch (ticks++)
    {
    case 10:
        LED_On(0u);
        break;
    case 20:
        LED_Off(0u);
        break;
    case 30:
        if (pfNonSecure_LED_On != NULL)
        {
            pfNonSecure_LED_On(1u);
        }
        break;
    case 50:
        if (pfNonSecure_LED_Off != NULL)
        {
            pfNonSecure_LED_Off(1u);
        }
        break;
    case 99:
        ticks = 0;
        if (ticks_printf++ == 3)
        {
            printf("%s", text);
            ticks_printf = 0;
        }
        break;
    default:
        if (ticks > 99)
        {
            ticks = 0;
        }
    }
}



void entry_point(){
  return;
}

void matmul()
{
    int mat[5][5];
    int val = 0;
    if (val == 1)
    {
        val++;
    }
    else
    {
        val += 2;
    }

    for (int x = 0; x < 2; x++)
    {
        for (int y = 0; y < 2; y++)
        {
            val += mat[x][y] + mat[y][x];
        }
    }
    val = val + 2;
    return;
}

void matmul2()
{
    int mat[5][5];
    int val = 0;
    if (val == 1)
    {
        val++;
    }
    else
    {
        val += 4;
    }

    for (int x = 0; x < 2; x++)
    {
        for (int y = 0; y < 2; y++)
        {
            val += mat[x][y] + mat[y][x];
        }
    }
    val = val + 2;
    return;
}


void exit_point(void){
  entry_point();
  matmul();
}

void run(void){
	exit_point();
}

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

void setup_DWT()
{
    // Enable DWT
    CoreDebug_->DEMCR |= DEMCR_TRCENA;
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


void cleanMTB(){
    uint32_t * ptr = (uint32_t *) mtb->MTB_BASE;
    for (int i = 0; i < MTB_BUFFER_SIZE; i++){
        ptr[i] = 0;
    }
}

void secureExceptionHandler(){
    if (mtb->MTB_FLOW == (MTB_WATERMARK_A)){
        mtb->MTB_FLOW = (MTB_WATERMARK_B);
    } else {
        mtb->MTB_FLOW = MTB_WATERMARK_A;
    }

    mtb->MTB_MASTER &= ~( 1U << 9 );
    mtb->MTB_MASTER &= ~( 1U << 31 );
    // mtb->MTB_FLOW &= ~(MTB_FLOW_AUTOSTOP_MASK|MTB_FLOW_AUTOHALT_MASK);
    
    // set last bit of LR to 0
    
    return;

}

#pragma GCC pop_options

void setup_MTB(){

    // setup VTOR 
    uint32_t * VTOR = (uint32_t *) SCB_->VTOR;
    VTOR[7] = (uint32_t) secureExceptionHandler;
    SCB_NS->VTOR = (uint32_t) VTOR;


    cleanMTB();
    mtb->MTB_TSTART |= 0b10;  // Set to use DWT_COMP1
    mtb->MTB_TSTOP  |= 0b1000;  // Set to use DWT_COMP3
    //mtb->MTB_FLOW = MTB_WATERMARK_A;
    mtb->MTB_FLOW = 0;
    mtb->MTB_POSITION = 0;
    mtb->MTB_MASTER |= MTB_MASTER_TSTARTEN_MASK;
    mtb->MTB_MASTER |= MTB_MASTER_MASK_MASK;
    return;
}

void exec(){
	setup_DWT();
	setup_MTB();
	// run();
	return;
}

static uint32_t x;
/*----------------------------------------------------------------------------
  Main function
 *----------------------------------------------------------------------------*/
int main(void)
{
    uint32_t NonSecure_StackPointer = (*((uint32_t *)(NONSECURE_START + 0u)));
    NonSecure_fpVoid NonSecure_ResetHandler =
        (NonSecure_fpVoid)(*((uint32_t *)(NONSECURE_START + 4u)));

    /* exercise some floating point instructions from Secure Mode */
    volatile uint32_t fpuType = SCB_GetFPUType();
    volatile float x1 = 12.4567f;
    volatile float x2 = 0.6637967f;
    volatile float x3 = 24.1111118f;

    x3 = x3 * (x1 / x2);

    /* exercise some core register from Secure Mode */
    x = __get_MSP();
    x = __get_PSP();
    __TZ_set_MSP_NS(NonSecure_StackPointer);
    x = __TZ_get_MSP_NS();
    __TZ_set_PSP_NS(0x22000000u);
    x = __TZ_get_PSP_NS();

    SystemCoreClockUpdate();

    stdout_init(); /* Initialize Serial interface */
    LED_Initialize();
    GLCD_Initialize();

    /* display initial screen */
    GLCD_SetFont(&GLCD_Font_16x24);
    GLCD_SetBackgroundColor(GLCD_COLOR_WHITE);
    GLCD_ClearScreen();
    GLCD_SetBackgroundColor(GLCD_COLOR_BLUE);
    GLCD_SetForegroundColor(GLCD_COLOR_RED);
    GLCD_DrawString(0 * 16, 0 * 24, "   V2M-MPS2+ Demo   ");
    GLCD_DrawString(0 * 16, 1 * 24, " Secure/Non-Secure  ");
    GLCD_DrawString(0 * 16, 2 * 24, "   www.keil.com     ");

    GLCD_SetBackgroundColor(GLCD_COLOR_WHITE);
    GLCD_SetForegroundColor(GLCD_COLOR_BLACK);
    switch ((SCB->CPUID >> 4) & 0xFFF)
    {
    case 0xD20:
        GLCD_DrawString(0 * 16, 4 * 24, "  Cortex-M23        ");
        break;
    case 0xD21:
        GLCD_DrawString(0 * 16, 4 * 24, "  Cortex-M33        ");
        break;
    default:
        GLCD_DrawString(0 * 16, 4 * 24, "  unknown Cortex-M  ");
        break;
    }

    // SysTick_Config(SystemCoreClock / 100); /* Generate interrupt each 10 ms */

    exec();

    NonSecure_ResetHandler();
}
