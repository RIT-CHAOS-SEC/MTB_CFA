	.cpu cortex-m33
	.arch armv8-m.main
	.fpu fpv5-sp-d16
	.arch_extension dsp
	.eabi_attribute 27, 1
	.eabi_attribute 28, 1
	.eabi_attribute 20, 1
	.eabi_attribute 21, 1
	.eabi_attribute 23, 3
	.eabi_attribute 24, 1
	.eabi_attribute 25, 1
	.eabi_attribute 26, 1
	.eabi_attribute 30, 6
	.eabi_attribute 34, 1
	.eabi_attribute 18, 4
	.file	"application.c"
	.text
	.section	.MTBDR_MEM,"ax",%progbits
	.align	1
	.global	application
	.syntax unified
	.thumb
	.thumb_func
	.type	application, %function
application:
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 1, uses_anonymous_args = 0
	push	{r7, lr}
	add	r7, sp, #0
	movs	r2, #43
	ldr	r1, .L2
	ldr	r0, .L2+4
	bl	duffcopy
	nop
	pop	{r7, pc}
.L3:
	.align	2
.L2:
	.word	target
	.word	source
	.size	application, .-application
	.align	1
	.global	application_entry
	.syntax unified
	.thumb
	.thumb_func
	.type	application_entry, %function
application_entry:
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 1, uses_anonymous_args = 0
	push	{r7, lr}
	add	r7, sp, #0
	bl	application
	nop
	pop	{r7, pc}
	.size	application_entry, .-application_entry
	.global	source
	.section	.bss.source,"aw",%nobits
	.align	2
	.type	source, %object
	.size	source, 100
source:
	.space	100
	.global	target
	.section	.bss.target,"aw",%nobits
	.align	2
	.type	target, %object
	.size	target, 100
target:
	.space	100
	.section	.MTBDR_MEM
	.align	1
	.global	duffcopy
	.syntax unified
	.thumb
	.thumb_func
	.type	duffcopy, %function
duffcopy:
	@ args = 0, pretend = 0, frame = 24
	@ frame_needed = 1, uses_anonymous_args = 0
	@ link register save eliminated.
	push	{r7}
	sub	sp, sp, #28
	add	r7, sp, #0
	str	r0, [r7, #12]
	str	r1, [r7, #8]
	str	r2, [r7, #4]
	ldr	r3, [r7, #4]
	adds	r3, r3, #7
	cmp	r3, #0
	bge	.L7
	adds	r3, r3, #7
.L7:
	asrs	r3, r3, #3
	str	r3, [r7, #20]
	ldr	r3, [r7, #4]
	adds	r3, r3, #1
	str	r3, [r7, #4]
	ldr	r3, [r7, #4]
	rsbs	r2, r3, #0
	and	r3, r3, #7
	and	r2, r2, #7
	it	pl
	rsbpl	r3, r2, #0
	cmp	r3, #7
	beq	.L8
	cmp	r3, #7
	bgt	.L17
	cmp	r3, #6
	beq	.L10
	cmp	r3, #6
	bgt	.L17
	cmp	r3, #5
	beq	.L11
	cmp	r3, #5
	bgt	.L17
	cmp	r3, #4
	beq	.L12
	cmp	r3, #4
	bgt	.L17
	cmp	r3, #3
	beq	.L13
	cmp	r3, #3
	bgt	.L17
	cmp	r3, #2
	beq	.L14
	cmp	r3, #2
	bgt	.L17
	cmp	r3, #0
	beq	.L15
	cmp	r3, #1
	beq	.L16
	b	.L17
.L18:
	nop
.L15:
	ldr	r2, [r7, #8]
	adds	r3, r2, #1
	str	r3, [r7, #8]
	ldr	r3, [r7, #12]
	adds	r1, r3, #1
	str	r1, [r7, #12]
	ldrb	r2, [r2]	@ zero_extendqisi2
	strb	r2, [r3]
.L8:
	ldr	r2, [r7, #8]
	adds	r3, r2, #1
	str	r3, [r7, #8]
	ldr	r3, [r7, #12]
	adds	r1, r3, #1
	str	r1, [r7, #12]
	ldrb	r2, [r2]	@ zero_extendqisi2
	strb	r2, [r3]
.L10:
	ldr	r2, [r7, #8]
	adds	r3, r2, #1
	str	r3, [r7, #8]
	ldr	r3, [r7, #12]
	adds	r1, r3, #1
	str	r1, [r7, #12]
	ldrb	r2, [r2]	@ zero_extendqisi2
	strb	r2, [r3]
.L11:
	ldr	r2, [r7, #8]
	adds	r3, r2, #1
	str	r3, [r7, #8]
	ldr	r3, [r7, #12]
	adds	r1, r3, #1
	str	r1, [r7, #12]
	ldrb	r2, [r2]	@ zero_extendqisi2
	strb	r2, [r3]
.L12:
	ldr	r2, [r7, #8]
	adds	r3, r2, #1
	str	r3, [r7, #8]
	ldr	r3, [r7, #12]
	adds	r1, r3, #1
	str	r1, [r7, #12]
	ldrb	r2, [r2]	@ zero_extendqisi2
	strb	r2, [r3]
.L13:
	ldr	r2, [r7, #8]
	adds	r3, r2, #1
	str	r3, [r7, #8]
	ldr	r3, [r7, #12]
	adds	r1, r3, #1
	str	r1, [r7, #12]
	ldrb	r2, [r2]	@ zero_extendqisi2
	strb	r2, [r3]
.L14:
	ldr	r2, [r7, #8]
	adds	r3, r2, #1
	str	r3, [r7, #8]
	ldr	r3, [r7, #12]
	adds	r1, r3, #1
	str	r1, [r7, #12]
	ldrb	r2, [r2]	@ zero_extendqisi2
	strb	r2, [r3]
.L16:
	ldr	r2, [r7, #8]
	adds	r3, r2, #1
	str	r3, [r7, #8]
	ldr	r3, [r7, #12]
	adds	r1, r3, #1
	str	r1, [r7, #12]
	ldrb	r2, [r2]	@ zero_extendqisi2
	strb	r2, [r3]
	ldr	r3, [r7, #20]
	subs	r3, r3, #1
	str	r3, [r7, #20]
	ldr	r3, [r7, #20]
	cmp	r3, #0
	bgt	.L18
.L17:
	nop
	adds	r7, r7, #28
	mov	sp, r7
	@ sp needed
	ldr	r7, [sp], #4
	bx	lr
	.size	duffcopy, .-duffcopy
	.section	.MTBTMP_MEM,"ax",%progbits
	.align	1
	.global	trampoline_mtbdr
	.syntax unified
	.thumb
	.thumb_func
	.type	trampoline_mtbdr, %function
trampoline_mtbdr:
	@ Naked Function: prologue and epilogue provided by programmer.
	@ args = 0, pretend = 0, frame = 0
	@ frame_needed = 1, uses_anonymous_args = 0
	.syntax unified
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
@ 1548 "application.c" 1
	nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

@ 0 "" 2
	.thumb
	.syntax unified
	nop
	.size	trampoline_mtbdr, .-trampoline_mtbdr
	.ident	"GCC: (GNU Tools for STM32 12.3.rel1.20240612-1315) 12.3.1 20230626"
