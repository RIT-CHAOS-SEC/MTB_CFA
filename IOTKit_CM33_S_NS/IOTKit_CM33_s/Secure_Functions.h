/*----------------------------------------------------------------------------
 * Name:    Secure_Functions.h
 * Purpose: Function and Typedef Declarations to include into NonSecure Application.
 *----------------------------------------------------------------------------*/

#ifndef SECURE_FUNCTIONS_H_
#define SECURE_FUNCTIONS_H_

#include <arm_cmse.h>
#include "cfa.h"

#define NSENTRY __attribute__((cmse_nonsecure_entry))

/* Define typedef for NonSecure callback function */ 
typedef int32_t (*NonSecure_funcptr)(uint32_t);

/* typedef for NonSecure callback functions */
typedef int32_t (*NonSecure_fpParam)(uint32_t) __attribute__((cmse_nonsecure_call));
typedef void (*NonSecure_fpVoid)(void) __attribute__((cmse_nonsecure_call));


/* Function declarations for Secure functions called from NonSecure application */
extern int32_t Secure_LED_On (uint32_t);
extern int32_t Secure_LED_Off(uint32_t);
extern int32_t Secure_LED_On_callback (NonSecure_funcptr);
extern int32_t Secure_LED_Off_callback(NonSecure_funcptr);
extern void    Secure_printf (char*);


void SECURE_register_callback(void *);
void SECURE_start_cfa(CFReport *);

#endif /* SECURE_FUNCTIONS_H_ */