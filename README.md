# Proyecto Compilador → 8086 (emu8086)

Compilador académico que toma programas en un lenguaje tipo C con tokens en español y los **traduce a ensamblador 8086** (real mode). El ensamblador se puede **abrir, compilar y ejecutar en emu8086** para observar el flujo, registros y memoria.

> Ejemplos de tokens: `tipo`, `identificador`, `entero`, `opSuma`, `return`, etc.  
> Ejemplo de driver: `lr_parser_driver.py` que ejecuta lexer → parser → generador de código.

---

## Tabla de contenido

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso rápido](#uso-rápido)
- [Qué se genera](#qué-se-genera)
- [Abrir/compilar/ejecutar en emu8086 (paso a paso)](#abrircompilarejecutar-en-emu8086-paso-a-paso)
- [Convenciones del ensamblador 8086](#convenciones-del-ensamblador-8086)
- [Ejemplo mínimo de entrada](#ejemplo-mínimo-de-entrada)
- [Solución de problemas](#solución-de-problemas)
- [Roadmap](#roadmap)
- [Licencia](#licencia)

---

## Características

- **Análisis léxico**: reconoce tokens (`tipo`, `identificador`, `entero`, `opSuma`, símbolos, etc.).
- **Análisis sintáctico LR**: driver `lr_parser_driver.py` con trazas opcionales (`--trace`).
- **Generación de código 8086**: emite `.asm` (compatible con emu8086).
- **Trazas y depuración**: modos `--dump-lex` y `--trace` para seguir el parser.
- **Salida organizada**: artefactos en carpetas `out/asm/` y `out/bin/`.

> Nota: Aunque a veces se use GCC para obtener `.s` de C, **la ruta oficial** de este proyecto es **nuestra** cadena (lexer → parser → codegen 8086) y **emu8086** como ensamblador/entorno de ejecución.

---

## Requisitos

- **Python 3.9+** (probado en Windows 10/11).
- **emu8086** (versión de evaluación o completa).
- (Opcional) **DOSBox** si deseas ejecutar `.exe/.com` fuera del emulador de emu8086.
- (Opcional) **GCC/MinGW** solo si quieres comparar salidas de GCC (no requerido por el flujo 8086).

---

## Instalación

```bash
# 1) Clona el repositorio
git clone https://github.com/USUARIO/Proyecto-compilador.git
cd Proyecto-compilador

# 2) (Opcional) Crea un entorno virtual
python -m venv .venv
.venv\Scripts\activate  # PowerShell/CMD en Windows

# 3) Instala dependencias
pip install -r requirements.txt
```

## Uso rápido

Generar ensamblador 8086 desde un archivo de ejemplo:

# Desde la raíz del repo
python src/drivers/lr_parser_driver.py examples/code.c


Modos de depuración (útiles para tareas de la materia):

# Volcado de tokens (léxico)
python src/drivers/lr_parser_driver.py examples/code.c --dump-lex

# Trazas del parser (primeras N)
python src/drivers/lr_parser_driver.py examples/code.c --trace 200

# Directorio de salida (si tu driver lo soporta)
python src/drivers/lr_parser_driver.py examples/code.c --out out/asm


La salida principal será un .asm en out/asm/.

## Qué se genera

out/asm/PROGRAMA.asm
Ensamblador 8086 con:

Secciones de datos y código.

Convención simple para main.

Instrucciones básicas: mov, add, sub, mul, div, cmp, jmp, j*, llamadas a rutinas de I/O si se usan macros.

(Opcional) out/bin/PROGRAMA.com o .exe
Si decides crear ejecutables desde emu8086 (ver siguiente sección).

## Abrir/compilar/ejecutar en emu8086 (paso a paso)

Estos pasos asumen que ya tienes un .asm generado en out/asm/.

Abre emu8086.

En el menú, ve a File → Open y selecciona tu archivo:
Proyecto-compilador\out\asm\PROGRAMA.asm

Revisa el código (opcional).

Compilar: clic en Compile (o F7).

Si tu .asm usa macros de emu8086, verifica que include 'emu8086.inc' esté presente (si tu generador lo usa).

Si hay errores de sintaxis, el panel inferior mostrará la línea; corrige y recompila.

Ejecutar en el emulador: clic en Emulate (o F9).

Se abrirá la ventana de ejecución. Puedes:

Ver registros (AX, BX, CX, DX, IP, FLAGS).

Step Into / Step Over para depurar.

Observar memoria y stack.

Crear ejecutable (.exe/.com) (opcional):

Menú Compile → Create EXE File o Create COM File.

Guarda el binario en out/bin/.

Puedes ejecutar el .com/.exe dentro de emu8086 (Emulate → Load), o en DOSBox si lo deseas.

Tip: Si emu8086 no encuentra includes, copia tus .inc (o el runtime_macros.asm) a la ruta del proyecto o ajusta rutas include.

## Convenciones del ensamblador 8086

Modelo: real mode, segmento único simple (.model tiny o .model small según plantilla).

Secciones:

data / stack para variables y pila.

code con start: (o etiqueta _main → start).

Salida:

Si usas macros de emu8086 para imprimir, suelen venir de emu8086.inc (e.g., PRINT, PRINTN, PUTC).

Retorno:

Programas .com: salir con mov ah, 4Ch / int 21h.

El emisor (emitter_8086.py) puede insertar prólogos/epílogos, reservar variables y traducir operaciones aritméticas y saltos condicionales (opSuma → add, etc.).

## Ejemplo mínimo de entrada

examples/code.c

// Lenguaje tipo C con tokens en español
tipo entero a = 5, b = 3;

tipo entero main() {
    tipo entero c;
    c = a opSuma b;     // suma
    return c;
}


Comando

python src/drivers/lr_parser_driver.py examples/code.c --dump-lex --trace 50


Salida esperada (resumen)

out/asm/code.asm con secciones de datos para a, b, c y código que:

carga a y b en registros

realiza la suma

mueve el resultado a c

hace return desde main

## Solución de problemas

1) “No se ve la pila / no aparecen trazas”
Usa los flags del driver:

--dump-lex           # tokens
--trace N            # N pasos del parser LR


2) “emu8086 marca error de sintaxis”

Verifica que tu emisor 8086 genere directivas/modelo compatibles.

Si usas macros (PRINT, etc.), agrega:

include 'emu8086.inc'


y compila dentro de emu8086.

3) “Se compiló pero no ejecuta nada”

Asegura un punto de entrada (start:) y un retorno correcto:

mov ah, 4Ch
int 21h


Si creas .com, usa .model tiny y ubica código/datos acorde.

4) “Quiero un .exe/.com”

En emu8086: Compile → Create EXE/COM File y guarda en out/bin/.

5) GCC vs 8086

El flag -masm= de GCC acepta intel o att, no AMD.

Para este proyecto no necesitas GCC; el flujo es propio → 8086 → emu8086.

## Roadmap

 Expresiones lógicas y condicionales (if, while).

 Llamadas a función con stack frame.

 Arreglos y acceso indexado.

 Librería de E/S (macros o rutinas estándar).

 Más tests y ejemplos.
