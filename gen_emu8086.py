# gen_emu8086.py
from typing import List, Tuple, Dict, Optional

Quad = Tuple[str, Optional[str], Optional[str], Optional[str]]

class Frame:
    def __init__(self, func_name: str, n_params: int):
        self.func_name = func_name
        self.n_params = n_params
        self.off: Dict[str, int] = {}  # nombre -> desplazamiento relativo a bp
        self.next_local = -2           # locales: -2,-4,-6,...
        self.param_base = 4            # [bp+4] primer parámetro
        self.local_size = 0

    def add_param(self, name: str, index: int):
        """Fija el offset de un parámetro por su índice (0-based)."""
        if name is None: return
        self.off[name] = self.param_base + 2*index

    def add_local_or_temp(self, name: str):
        """Asigna slot negativo para variables locales o temporales."""
        if name is None: return
        if name in self.off: return  # ya asignado (p.ej. parámetro)
        self.off[name] = self.next_local
        self.next_local -= 2
        # local_size: bytes totales reservados (redondeado hacia abajo)
        self.local_size = max(self.local_size, -self.next_local - 2)

def is_temp(x: str) -> bool:
    return bool(x) and x.startswith("t")

def offset_str(off: int) -> str:
    return f"+{off}" if off>=0 else f"{off}"

def collect_names(quads: List[Quad]) -> Dict[str,str]:
    """
    Escanea quads y devuelve nombres vistos (vars/temps) para asignación de offsets.
    Ignora labels (L...), constantes (isdigit), strings (STR...), y None.
    """
    names: Dict[str,str] = {}
    for op,a,b,r in quads:
        # ignora quads que no generan locals (literales/calls especiales)
        if op in ("strlit","printf_i","printf_si","getchar","; TODO"):
            continue
        for x in (a,b,r):
            if isinstance(x,str) and x not in (None,""):
                if x.startswith("L"):   continue
                if x.startswith("STR"): continue
                if x.isdigit():         continue
                names[x] = "temp" if is_temp(x) else "var"
    return names

def gen_asm(quads):
    """
    Emete ASM para emu8086 (.COM):
    - Literales de cadena:    op='strlit', a=texto, r='STRn'
    - printf entero:          op='printf_i',  a=valor
    - printf formato %d\\n:   op='printf_si', a='STRn', b=valor
    - getchar:                op='getchar'
    - asignación:             op='=', a=src, r=dst
    - binarios:               op in {'+','-','*','/'}, a=left, b=right, r=dst
    - parámetros:             op='param', a=valor
    - llamada:                op='call', a=nombre, b=num_args, r=dst
    - return:                 op='ret', a=valor (opcional), r=None
    - labels/jumps (opc):     op='label' (r='Lx'), op='jmp' (a='Lx'), op in {'jz','jnz'} (a='Lx', b=cond)
    """
    # ---------- helpers locales ----------
    def is_imm(x):
        return isinstance(x, str) and x.isdigit()

    def get_off(name: str) -> int:
        """Devuelve offset (negativo) desde BP para 'name', asignándolo si no existe."""
        nonlocal next_off
        if name not in off:
            off[name] = next_off
            next_off -= 2
        return off[name]

    def emit_load_ax(operand):
        """Carga 'operand' (inmediato, temp o var) en AX."""
        if operand is None:
            return
        if is_imm(operand):
            out.append(f"    mov ax, {operand}")
        elif isinstance(operand, str) and operand.startswith("STR"):
            # cargar dirección de cadena a DX si se va a imprimir texto (no usado en printf_i/si)
            out.append(f"    lea dx, {operand}")
        else:
            offv = get_off(operand)
            out.append(f"    mov ax, [bp{off_str(offv)}]")

    def emit_store_ax(dst):
        """Guarda AX en variable/temporal 'dst'."""
        if dst is None:
            return
        offv = get_off(dst)
        out.append(f"    mov [bp{off_str(offv)}], ax")

    def off_str(o: int) -> str:
        return f"{o:+d}"

    # ---------- recolecta literales de cadena ----------
    str_lits = []
    for op, a, b, r in quads:
        if op == "strlit":
            # convierte '\n' a 13,10 dentro del db
            txt = (a or "").replace("\\n", "\" , 13, 10, \"")
            str_lits.append((r, txt))

    out = []
    out += [
        "; ===== emu8086 DOS .COM emitter =====",
        "org 100h",
        "",
        ".data",
        "; ===== string literals =====",
    ]
    if str_lits:
        for label, txt in str_lits:
            out += [f'{label} db "{txt}",0']
    out += [
        "",
        ".code",
        "start:",
        "    mov ax, @data",
        "    mov ds, ax",
        "",
        "; ===== RUNTIME =====",
        "; imprime AX (unsigned) en decimal + CRLF",
        "print_ax proc near",
        "    push ax",
        "    push bx",
        "    push cx",
        "    push dx",
        "    mov cx, 0",
        "    mov bx, 10",
        "PA1:",
        "    xor dx, dx",
        "    div bx",
        "    push dx",
        "    inc cx",
        "    test ax, ax",
        "    jnz PA1",
        "PA2:",
        "    pop dx",
        "    add dl, '0'",
        "    mov ah, 02h",
        "    int 21h",
        "    loop PA2",
        "    ; CRLF",
        "    mov dl, 13",
        "    mov ah, 02h",
        "    int 21h",
        "    mov dl, 10",
        "    int 21h",
        "    pop dx",
        "    pop cx",
        "    pop bx",
        "    pop ax",
        "    ret",
        "print_ax endp",
        "",
        "; imprime ASCIIZ apuntada por DS:DX",
        "print_str proc near",
        "    push ax",
        "    push dx",
        "    push bx",
        "    mov  bx, dx",
        "PS1:",
        "    mov  al, [bx]",
        "    cmp  al, 0",
        "    je   PSF",
        "    mov  dl, al",
        "    mov  ah, 02h",
        "    int  21h",
        "    inc  bx",
        "    jmp  PS1",
        "PSF:",
        "    pop  bx",
        "    pop  dx",
        "    pop  ax",
        "    ret",
        "print_str endp",
        "",
        "__entry:",
        "    ; punto de entrada único",
        "    call main",
        "    mov ax, 4C00h",
        "    int 21h",
        "",
        "; ===== cuerpo de funciones =====",
        "",
        "main:",
        "    push bp",
        "    mov bp, sp",
        "    sub sp, 0      ; <-- parchearemos el tamaño real de locales al final",
    ]

    # frame de main: offsets perezosos
    off = {}         # name -> offset negativo desde BP
    next_off = -2    # comenzamos en -2, cada var ocupa 2 bytes
    sub_sp_idx = len(out) - 1  # línea a parchear

    # pila auxiliar para 'param' (por si quieres validar número de args)
    # aquí no es estrictamente necesaria; empujamos directo
    for op, a, b, r in quads:
        # -------- control de flujo mínimo --------
        if op == "label":
            out.append(f"{r}:")
            continue
        if op == "jmp":
            out.append(f"    jmp {a}")
            continue
        if op in ("jz", "jnz"):
            # si tu IR trae condición en b, carga y compara con 0
            emit_load_ax(b)
            out += ["    cmp ax, 0"]
            out.append(f"    {'jz' if op=='jz' else 'jnz'} {a}")
            continue

        # -------- especiales nuevos --------
        if op == "strlit":
            # ya emitidas en .data
            continue
        if op == "printf_i":
            emit_load_ax(a)
            out.append("    call print_ax")
            continue
        if op == "printf_si":
            # asumimos formato "%d\\n": ignoramos literal y solo imprimimos el entero con CRLF
            emit_load_ax(b)
            out.append("    call print_ax")
            continue
        if op == "getchar":
            out += [
                "    mov ah, 01h",
                "    int 21h",
            ]
            continue

        # -------- llamadas/parámetros --------
        if op == "param":
            if is_imm(a):
                out.append(f"    push {a}")
            else:
                offa = get_off(a)
                out.append(f"    push word ptr [bp{off_str(offa)}]")
            continue

        if op == "call":
            func_name = a
            # preserva BP/AX si quisieras (no es obligatorio)
            out.append(f"    call {func_name}")
            # si r recibe retorno, asumimos en AX
            if r:
                emit_store_ax(r)
            # limpia pila de parámetros si el callee no lo hace (cdecl)
            nargs = int(b) if isinstance(b, str) and b.isdigit() else 0
            if nargs > 0:
                out.append(f"    add sp, {nargs*2}")
            continue

        # -------- retorno --------
        if op == "ret":
            if a is not None:
                emit_load_ax(a)  # retorno en AX
            out += [
                "    mov sp, bp",
                "    pop bp",
                "    ret",
            ]
            continue

        # -------- asignación/binaries --------
        if op == "=":
            if is_imm(a):
                out.append(f"    mov ax, {a}")
            elif isinstance(a, str) and a.startswith("STR"):
                # si asignaras dirección de cadena a una variable, usarías LEA->AX y store
                out.append(f"    lea ax, {a}")
            else:
                offa = get_off(a)
                out.append(f"    mov ax, [bp{off_str(offa)}]")
            emit_store_ax(r)
            continue

        if op in ("+", "-", "*", "/"):
            # carga left en AX
            if is_imm(a):
                out.append(f"    mov ax, {a}")
            else:
                offa = get_off(a)
                out.append(f"    mov ax, [bp{off_str(offa)}]")

            # aplica con right
            if op in ("+", "-"):
                if is_imm(b):
                    out.append(f"    { 'add' if op=='+' else 'sub' } ax, {b}")
                else:
                    offb = get_off(b)
                    out.append(f"    { 'add' if op=='+' else 'sub' } ax, [bp{off_str(offb)}]")
            elif op == "*":
                if is_imm(b):
                    out.append(f"    mov bx, {b}")
                else:
                    offb = get_off(b)
                    out.append(f"    mov bx, [bp{off_str(offb)}]")
                out.append("    imul bx")
            else:  # '/'
                # división entera AX / B -> AX=quot
                out.append("    cwd")  # extensión de signo a DX:AX
                if is_imm(b):
                    out.append(f"    mov bx, {b}")
                else:
                    offb = get_off(b)
                    out.append(f"    mov bx, [bp{off_str(offb)}]")
                out.append("    idiv bx")

            emit_store_ax(r)
            continue

        # si llega algo no soportado:
        # out.append(f"    ; TODO op={op} a={a} b={b} r={r}")
        # (lo ignoramos en silencio)
        pass

    # epílogo por si no hubo 'ret' explícito
    out += [
        "    mov sp, bp",
        "    pop bp",
        "    ret",
        "",
        "; ===== fin main =====",
        "",
        "; puedes definir aquí otras funciones llamadas (p. ej., suma)",
        "suma:",
        "    push bp",
        "    mov  bp, sp",
        "    ; cdecl: [bp+4]=arg1 (primero empujado), [bp+6]=arg2",
        "    mov  ax, [bp+4]",
        "    add  ax, [bp+6]",
        "    mov  sp, bp",
        "    pop  bp",
        "    ret",
        "",
        "end start",
    ]

    # --------- parchea tamaño de frame ----------
    locals_bytes = (-next_off - 2) if next_off < -2 else 0
    out[sub_sp_idx] = f"    sub sp, {locals_bytes:>d}      ; locals"

    return "\n".join(out)
