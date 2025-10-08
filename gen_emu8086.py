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
    Ignora labels (L...), constantes (isdigit) y None.
    """
    names: Dict[str,str] = {}
    for op,a,b,r in quads:
        for x in (a,b,r):
            if isinstance(x,str) and x not in (None,""):
                if x.startswith("L"): continue
                if x.isdigit(): continue
                names[x] = "temp" if is_temp(x) else "var"
    return names

def gen_asm(quads: List[Quad]) -> str:
    out: List[str] = []
    out += [
        "; ===== emu8086 / .COM =====",
        "org 100h",
        "",
        "jmp start",
        "",
        "; ---- RUNTIME opcional (p.ej. print) aquí ----",
        "",
    ]

    i = 0
    while i < len(quads):
        op,a,b,r = quads[i]

        if op == "func":
            fname, nparams = a, int(b)

            # Extrae el cuerpo de la función hasta endfunc
            body: List[Quad] = []
            j = i+1
            while not (quads[j][0] == "endfunc" and quads[j][1] == fname):
                body.append(quads[j]); j += 1

            # 1) Construye el frame y registra parámetros por nombre e índice
            fr = Frame(fname, nparams)
            has_ret = False
            param_names: List[str] = [None]*nparams
            for op2,a2,b2,r2 in body:
                if op2 == "defparam":
                    idx = int(b2)
                    if 0 <= idx < nparams:
                        param_names[idx] = a2
                        fr.add_param(a2, idx)
                elif op2 == "ret":
                   
                    has_ret = True

            # 2) Registra locales/temporales (todos los nombres que no sean parámetros)
            names = collect_names(body)
            for name, kind in names.items():
                if name in param_names:
                    continue  # ya tiene offset positivo
                fr.add_local_or_temp(name)

            # Etiqueta y prólogo
            out.append(f"{fname}:")
            out += [
                "    push bp",
                "    mov  bp, sp",
                f"    sub  sp, {max(0, fr.local_size)}"
            ]

            # 3) Emite cuerpo (saltando 'defparam', que solo era meta-información)
            k = i+1
            while not (quads[k][0]=="endfunc" and quads[k][1]==fname):
                op2,a2,b2,r2 = quads[k]

                if op2 == "defparam":
                    # No genera código; ya usamos esto para asignar offsets
                    k += 1
                    continue

                # labels
                if op2 == "label":
                    out.append(f"{r2}:")
                # gotos
                elif op2 == "goto":
                    out.append(f"    jmp {r2}")
                # asignación '='  (src -> dst)
                elif op2 == "=":
                    if a2 is not None and a2.isdigit():
                        out += [f"    mov ax, {a2}",
                                f"    mov [bp{offset_str(fr.off[r2])}], ax"]
                    else:
                        out += [f"    mov ax, [bp{offset_str(fr.off[a2])}]",
                                f"    mov [bp{offset_str(fr.off[r2])}], ax"]
                # aritmética
                elif op2 in ("+","-","*","/"):
                    out += [f"    mov ax, [bp{offset_str(fr.off[a2])}]"]
                    if op2 == "+":
                        out += [f"    add ax, [bp{offset_str(fr.off[b2])}]"]
                    elif op2 == "-":
                        out += [f"    sub ax, [bp{offset_str(fr.off[b2])}]"]
                    elif op2 == "*":
                        out += [f"    imul word ptr [bp{offset_str(fr.off[b2])}]"]
                    elif op2 == "/":
                        out += [f"    cwd",
                                f"    idiv word ptr [bp{offset_str(fr.off[b2])}]"]
                    out += [f"    mov [bp{offset_str(fr.off[r2])}], ax"]
                # comparaciones con salto (if<, if>, ...)
                elif op2 in ("if<","if>","if<=","if>=","if==","if!="):
                    jmp = {"if<":"jl","if>":"jg","if<=":"jle","if>=":"jge","if==":"je","if!=":"jne"}[op2]
                    out += [f"    mov ax, [bp{offset_str(fr.off[a2])}]",
                            f"    cmp ax, [bp{offset_str(fr.off[b2])}]",
                            f"    {jmp} {r2}"]
                # parámetros y llamada
                elif op2 == "param":
                    out += [f"    push word ptr [bp{offset_str(fr.off[a2])}]"]
                elif op2 == "call":
                    callee = a2
                    out += [f"    call {callee}"]
                    # callee limpia sus args con 'ret 2*nparams'
                    out += [f"    mov [bp{offset_str(fr.off[r2])}], ax"]
                # retorno
                elif op2 == "ret":
                    if a2 is not None:
                        out += [f"    mov ax, [bp{offset_str(fr.off[a2])}]"]
                    out += [
                        f"    mov  sp, bp",
                        f"    pop  bp",
                        f"    ret {2*fr.n_params}"
                    ]
                k += 1

            # saltar al endfunc
            if not has_ret:
                # Epílogo y retorno implícito (ret 2*nparams) si la función no retornó explícitamente
                out += [
                    f"    mov  sp, bp",
                    f"    pop  bp",
                    f"    ret {2*fr.n_params}"
                ]
            i = j

        i += 1

    # Punto de entrada
    out += [
        "",
        "start:",
        "    ; Llama a main si existe",
        "    call main",
        "    ; terminar .COM",
        "    mov ax, 4C00h",
        "    int 21h",
        ""
    ]
    return "\n".join(out)
