/*----------------------------------------------------------------------------
 * Name:    main_ns.c
 * Purpose: Main function non-secure mode
 *----------------------------------------------------------------------------*/

#include <arm_cmse.h>
#include "RTE_Components.h"                        /* Component selection */
#include CMSIS_device_header
#include "Board_LED.h"                             /* ::Board Support:LED */
#include "..\IOTKit_CM33_s\Secure_Functions.h"     /* Secure Code Entry Points */


char text[] = "Hello World (non-secure)\r\n";

/*----------------------------------------------------------------------------
  NonSecure functions used for callbacks
 *----------------------------------------------------------------------------*/
int32_t NonSecure_LED_On(uint32_t num);
int32_t NonSecure_LED_On(uint32_t num)
{
  return LED_On(num);
}

int32_t NonSecure_LED_Off(uint32_t num);
int32_t NonSecure_LED_Off(uint32_t num)
{
  return LED_Off(num);
}


/*----------------------------------------------------------------------------
  SysTick IRQ Handler
 *----------------------------------------------------------------------------*/
void SysTick_Handler (void);
void SysTick_Handler (void) {
  static uint32_t ticks;

  switch (ticks++) {
    case  10:
      LED_On(7u);
      break;
    case 20:
      Secure_LED_On(6u);
      break;
    case 30:
      LED_Off(7u);
      break;
    case 50:
      Secure_LED_Off(6u);
      break;
    case 99:
      ticks = 0;
      break;
    default:
      if (ticks > 99) {
        ticks = 0;
      }
  }
}


static uint32_t x;
/*----------------------------------------------------------------------------
  Main function
 *----------------------------------------------------------------------------*/

#define MAXX 10
#define MAXY 5
void matmul3()
{
    int mat[MAXX][MAXY];
    int val = 0;
    if (val == 1)
    {
        val++;
    }
    else
    {
        val += 4;
    }

    for (int x = 0; x < MAXX; x++)
    {
        for (int y = 0; y < MAXY; y++)
        {
            val += mat[x][y] + mat[y][x];
        }
    }
    val = val + 2;
    return;
}

int main (void)
{
  uint32_t i;
	
	
  /* exercise some floating point instructions */
  volatile uint32_t fpuType = SCB_GetFPUType(); 
  volatile float  x1 = 12.4567f;
  volatile float  x2 = 0.6637967f;
  volatile float  x3 = 24.1111118f;

  x3 = x3 * (x1 / x2);

  /* exercise some core register from Non Secure Mode */
  x = __get_MSP();
  x = __get_PSP();

  /* register NonSecure callbacks in Secure application */
  Secure_LED_On_callback(NonSecure_LED_On);
  Secure_LED_Off_callback(NonSecure_LED_Off);

#if 0
  LED_Initialize ();                      /* already done in Secure part */
#endif

  // SystemCoreClockUpdate();
  // SysTick_Config(SystemCoreClock / 100);  /* Generate interrupt each 10 ms */


	matmul3();


  while (1) {
    LED_On (5u);
    for (i = 0; i < 0x100000; i++) __NOP();
    LED_Off(5u);
    for (i = 0; i < 0x100000; i++) __NOP();
    Secure_LED_On (4u);
    for (i = 0; i < 0x100000; i++) __NOP();
    Secure_LED_Off(4u);
    for (i = 0; i < 0x100000; i++) __NOP();

    Secure_printf(text);
  }
}
