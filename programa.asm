; ===== emu8086 / .COM =====
org 100h

jmp start

; ---- RUNTIME opcional (p.ej. print) aquí ----


start:
    ; Llama a main si existe
    call main
    ; terminar .COM
    mov ax, 4C00h
    int 21h
