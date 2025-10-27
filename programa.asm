; ===== emu8086 DOS .COM emitter =====
org 100h

.data
; ===== string literals =====
STR1 db ""%d" , 13, 10, """,0
STR2 db ""Presiona ENTER para salir..."",0

.code
start:
    mov ax, @data
    mov ds, ax

; ===== RUNTIME =====
; imprime AX (unsigned) en decimal + CRLF
print_ax proc near
    push ax
    push bx
    push cx
    push dx
    mov cx, 0
    mov bx, 10
PA1:
    xor dx, dx
    div bx
    push dx
    inc cx
    test ax, ax
    jnz PA1
PA2:
    pop dx
    add dl, '0'
    mov ah, 02h
    int 21h
    loop PA2
    ; CRLF
    mov dl, 13
    mov ah, 02h
    int 21h
    mov dl, 10
    int 21h
    pop dx
    pop cx
    pop bx
    pop ax
    ret
print_ax endp

; imprime ASCIIZ apuntada por DS:DX
print_str proc near
    push ax
    push dx
    push bx
    mov  bx, dx
PS1:
    mov  al, [bx]
    cmp  al, 0
    je   PSF
    mov  dl, al
    mov  ah, 02h
    int  21h
    inc  bx
    jmp  PS1
PSF:
    pop  bx
    pop  dx
    pop  ax
    ret
print_str endp

__entry:
    ; punto de entrada único
    call main
    mov ax, 4C00h
    int 21h

; ===== cuerpo de funciones =====

main:
    push bp
    mov bp, sp
    sub sp, 24      ; locals
    mov ax, [bp-2]
    add ax, [bp-4]
    mov [bp-6], ax
    mov ax, [bp-6]
    mov sp, bp
    pop bp
    ret
    mov ax, [bp-2]
    add ax, [bp-4]
    mov [bp-8], ax
    mov ax, [bp-8]
    mov [bp-10], ax
    mov ax, 9
    mov [bp-12], ax
    push word ptr [bp-12]
    mov ax, 8
    mov [bp-14], ax
    push word ptr [bp-14]
    call suma
    mov [bp-16], ax
    add sp, 4
    mov ax, [bp-16]
    mov [bp-10], ax
    mov ax, [bp-10]
    call print_ax
    mov ax, 0
    mov [bp-18], ax
    lea dx, STR2
    call print_ax
    mov ax, 0
    mov [bp-20], ax
    mov ah, 01h
    int 21h
    mov ax, 0
    mov [bp-22], ax
    mov ax, 0
    mov [bp-24], ax
    mov ax, [bp-24]
    mov sp, bp
    pop bp
    ret
    mov sp, bp
    pop bp
    ret

; ===== fin main =====

; puedes definir aquí otras funciones llamadas (p. ej., suma)
suma:
    push bp
    mov  bp, sp
    ; cdecl: [bp+4]=arg1 (primero empujado), [bp+6]=arg2
    mov  ax, [bp+4]
    add  ax, [bp+6]
    mov  sp, bp
    pop  bp
    ret

end start