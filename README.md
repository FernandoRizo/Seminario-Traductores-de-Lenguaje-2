Traductores de lenguaje 2 — Mini-compilador C → ASM (emu8086)

Este proyecto implementa un pipeline de compilación (lexer → parser LR(1) → AST → IR → backend) para un subconjunto de C y genera como salida ensamblador 8086 (modo real, DOS) compatible con emu8086 (y con DOSBox si exportas .COM/.EXE de 16-bit).
Además, incluye una ruta opcional para producir un .EXE nativo de Windows (PE) usando MinGW-w64/MSYS2.

✨ ¿Qué hace?

Analiza un archivo Code.c que contiene:

declaraciones de variables y funciones,

asignaciones,

expresiones aditivas (+),

llamadas a funciones (p. ej. suma(8,9)),

return Expr;

literales de cadena (para printf("%d\n", x) si activas el soporte)

Ignora directivas de preprocesador (#include, #define, …) para simplificar.

Genera:

Cuádruplas (IR intermedio).

ASM 16-bit para emu8086: programa.asm.

(Opcional) EXE Windows x64 vía GCC/MinGW (compilando el C directamente).
