	.file	"Code.c"
	.intel_syntax noprefix
	.text
	.p2align 4
	.globl	suma
	.def	suma;	.scl	2;	.type	32;	.endef
	.seh_proc	suma
suma:
	.seh_endprologue
	lea	eax, [rcx+rdx]
	ret
	.seh_endproc
	.section .rdata,"dr"
.LC0:
	.ascii "%d\12\0"
.LC1:
	.ascii "Presiona ENTER para salir...\0"
	.section	.text.startup,"x"
	.p2align 4
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
	sub	rsp, 40
	.seh_stackalloc	40
	.seh_endprologue
	call	__main
	mov	edx, 17
	lea	rcx, .LC0[rip]
	call	printf
	lea	rcx, .LC1[rip]
	call	printf
	call	getchar
	xor	eax, eax
	add	rsp, 40
	ret
	.seh_endproc
	.globl	a
	.bss
	.align 4
a:
	.space 4
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (Rev8, Built by MSYS2 project) 15.2.0"
	.def	printf;	.scl	2;	.type	32;	.endef
	.def	getchar;	.scl	2;	.type	32;	.endef
