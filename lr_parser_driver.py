# -*- coding: utf-8 -*-
from ast_nodes import *
import sys
import os
import csv
import importlib.util
from dataclasses import dataclass
from typing import List, Tuple

import argparse

BASE = os.path.dirname(os.path.abspath(__file__))
def here(*parts): return os.path.join(BASE, *parts)



# === Carga módulos del usuario (desde la misma carpeta) ===
def _load_module(name: str, path: str):
    path = os.path.abspath(path)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo cargar {name} desde {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    return module

AnalizadorLexico = _load_module("analizadorLexico", here("analizadorLexico.py"))
simbolos_lexicos = _load_module("simbolos_lexicos", here("simbolos_lexicos.py"))

Estado = simbolos_lexicos.Estado
Terminal = simbolos_lexicos.Terminal
NoTerminal = simbolos_lexicos.NoTerminal
Pila = simbolos_lexicos.Pila

def _rhs_symbols_from_stack(stack, rhs_len):
    """
    Devuelve los símbolos (string) del RHS en orden izq→der,
    leyendo desde la cima: [ ... , <Simbolo_k>, Estado, <Simbolo_{k-1}>, Estado, ... ].
    """
    syms_rev = []
    idx = len(stack._data) - 2  # -1 es Estado; -2 es el símbolo más a la derecha
    for _ in range(rhs_len):
        symobj = stack._data[idx]
        if hasattr(symobj, 'sym'):      # Terminal(...)
            syms_rev.append(symobj.sym)
        else:                           # NoTerminal(...)
            syms_rev.append(symobj.name)
        idx -= 2                        # saltar el Estado intermedio
    return list(reversed(syms_rev))     # izq→der



# === Lee encabezados (símbolo -> columna) desde compilador.csv ===
def load_symbol_headers(csv_path: str) -> Tuple[List[str], dict]:
    with open(csv_path, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        header = next(reader)
    symbols = header[1:]  # la primera columna es el estado
    mapping = {sym: idx for idx, sym in enumerate(symbols)}
    return symbols, mapping

# === Lee la máquina LR desde compilador.lr ===
def load_lr_table(lr_path: str):
    lines = []
    with open(lr_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(line)

    it = iter(lines)
    num_rules = int(next(it))
    rules = []
    while len(rules) < num_rules:
        line = next(it)
        if line.startswith("..."):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        lhs_id = int(parts[0]); rhs_len = int(parts[1]); lhs_name = parts[2]
        rules.append((lhs_id, rhs_len, lhs_name))

    dims = next(it)
    while dims.startswith("..."):
        dims = next(it)
    num_rows, num_cols = map(int, dims.split())

    table = []
    for _ in range(num_rows):
        row = []
        while len(row) < num_cols:
            parts = next(it).split()
            row.extend(int(x) for x in parts)
        table.append(row[:num_cols])
    return num_rules, rules, num_rows, num_cols, table

symbols, sym_to_col = load_symbol_headers(here("compilador.csv"))
_, rules, nrows, ncols, table = load_lr_table(here("compilador.lr"))

# print(">> Columnas (CSV ↔ LR):")
# for i,s in enumerate(symbols):
#     print(f"  col {i}: '{s}'")

# # Ver la acción en estado 10 con ')'
# if ')' in sym_to_col:
#     print(">> ACTION[10,')'] =", table[10][sym_to_col[')']])
# else:
#     print(">> OJO: ')' no está en encabezado CSV")
# === Mapeo del tipo de token (lexer) a terminal de la gramática ===
TOKEN_TYPE_TO_TERMINAL = {
    'IDENTIFICADOR': 'identificador',
    'ENTERO': 'entero',
    'REAL': 'real',
    'CADENA': 'cadena',
    'TIPO': 'tipo',
    'OP_SUMA': 'opSuma',
    'OP_MUL': 'opMul',
    'OP_RELAC': 'opRelac',
    'OP_OR': 'opOr',
    'OP_AND': 'opAnd',
    'OP_NOT': 'opNot',
    'OP_IGUALDAD': 'opIgualdad',
    'PUNTO_Y_COMA': ';',
    'COMA': ',',
    'PARENTESIS_IZQ': '(',
    'PARENTESIS_DER': ')',
    'LLAVE_IZQ': '{',
    'LLAVE_DER': '}',
    'ASIGNACION': '=',
    'IF': 'if',
    'WHILE': 'while',
    'RETURN': 'return',
    'ELSE': 'else',
    'FIN': '$',
}

@dataclass
class TraceStep:
    step: int
    stack_repr: str
    lookahead: str
    action: int
    note: str

class LRParser:
    def __init__(self, table, rules, symbols, sym_to_col):
        self.table = table
        self.rules = rules
        self.symbols = symbols
        self.sym_to_col = sym_to_col

    def _tokenize(self, code: str):
        toks = AnalizadorLexico.analizador_lexico(code)
        mapped = []
        for t in toks:
            sym = TOKEN_TYPE_TO_TERMINAL.get(t.tipo)
            if sym is None and t.valor in self.sym_to_col:
                sym = t.valor
            if sym is None:
                raise ValueError(f"No puedo mapear el token: tipo={t.tipo} valor={t.valor}")
            if sym not in self.sym_to_col:
                raise ValueError(f"Símbolo '{sym}' no se encuentra en el compilador")

            # yylval: lo que viajará por la pila semántica
            if sym == 'identificador':
                yylval = t.valor               # nombre
            elif sym == 'entero':
                yylval = int(t.valor)
            elif sym in ('tipo','opSuma','=',',','(',')','{','}',';','return'):
                yylval = t.valor               # operador/puntación/keyword (si hace falta)
            else:
                yylval = t.valor               # por defecto

            mapped.append((sym, self.sym_to_col[sym], yylval))
        mapped.append(('$', self.sym_to_col['$'], '$'))
        return mapped
    

    def parse(self, code: str, trace: bool = True):
        # Acciones semánticas (dict por clave textual de producción)
        ACTIONS = _make_actions()

        stack = Pila()
        stack.push(Estado(0))
        input_syms = self._tokenize(code)
        ip = 0
        steps: List[TraceStep] = []
        step_no = 0

        # pila de valores semánticos paralela
        sem_stack: List[object] = []

        def stack_str() -> str:
            return str(stack)

        # Necesitamos reconstruir el orden textual de reglas (para nombrar la producción)
        # Esta lista DEBE reflejar el mismo orden de RULE_LIST en builder_lr.py
        PRODUCCIONES = [
            # 1..N (sin la aumentada)
            ("Program",      ("DeclList",)),
            ("DeclList",     ("DeclList","Decl")),
            ("DeclList",     ("Decl",)),
            ("Decl",         ("VarDecl",";",)),
            ("Decl",         ("FunDef",)),
            ("VarDecl",      ("tipo","identificador",)),
            ("FunDef",       ("tipo","identificador","(","ParamListOpt",")","Block")),
            ("ParamListOpt", ()),                         # ε
            ("ParamListOpt", ("ParamList",)),
            ("ParamList",    ("Param",)),
            ("ParamList",    ("ParamList",",","Param")),
            ("Param",        ("tipo","identificador")),
            ("Block",        ("{","StmtListOpt","}")),
            ("StmtListOpt",  ()),                         # ε
            ("StmtListOpt",  ("StmtList",)),
            ("StmtList",     ("Stmt",)),
            ("StmtList",     ("StmtList","Stmt")),
            ("Stmt",         ("VarDecl",";",)),
            ("Stmt",         ("Assign",";",)),
            ("Stmt",         ("Return",";",)),
            ("Assign",       ("identificador","=","Expr")),
            ("Return",       ("return","Expr")),
            ("Expr",         ("Expr","opSuma","Term")),
            ("Expr",         ("Term",)),
            ("Term",         ("Factor",)),
            ("Factor",       ("identificador",)),
            ("Factor",       ("entero",)),
            ("Factor",       ("(","Expr",")")),
            ("Factor",       ("Call",)),
            ("Call",         ("identificador","(","ArgListOpt",")")),
            ("ArgListOpt",   ()),                         # ε
            ("ArgListOpt",   ("ArgList",)),
            ("ArgList",      ("Expr",)),
            ("ArgList",      ("ArgList",",","Expr")),
        ]
        steps: List[TraceStep] = []
        step_no = 0
        ok = False
        msg = "Error inesperado"

        MAX_STEPS = 20000

        while True:
            if step_no > MAX_STEPS:
                steps.append(TraceStep(step_no, str(stack), "<guard>", 0, "ABORT: demasiados pasos"))
                ok = False
                msg = "Bucle detectado (demasiados pasos)"
                break

            state = stack.top().id
            look_sym, look_col, look_lex = input_syms[ip]
            act = self.table[state][look_col]
            note = ""

            if act == 0:
                note = "ERROR"
                steps.append(TraceStep(step_no, str(stack), look_sym, act, note))
                ok = False
                msg = f"Error sintáctico en estado {state} con símbolo '{look_sym}'"
                break

            if act > 0:
                # SHIFT
                stack.push(Terminal(look_sym))
                stack.push(Estado(act))
                ip += 1
                note = f"shift → estado {act}"

            elif act == -1:
                # ACCEPT (no retornes aquí; registra y rompe)
                note = "ACCEPT"
                steps.append(TraceStep(step_no, str(stack), look_sym, act, note))
                ok = True
                msg = "Cadena aceptada"
                break

            else:
                # REDUCE
                rule_no = -act - 1
                lhs_id, rhs_len, lhs_name = self.rules[rule_no - 1]
                for _ in range(rhs_len):
                    stack.pop(); stack.pop()
                top_state = stack.top().id
                goto_state = self.table[top_state][lhs_id]
                if goto_state <= 0:
                    note = f"reduce R{rule_no} → GOTO inválido"
                    steps.append(TraceStep(step_no, str(stack), look_sym, act, note))
                    ok = False
                    msg = f"Error en GOTO después de R{rule_no} (top_state={top_state}, lhs_id={lhs_id})"
                    break
                stack.push(NoTerminal(lhs_name))
                stack.push(Estado(goto_state))
                note = f"reduce R{rule_no}: {lhs_name} (|rhs|={rhs_len}) → goto {goto_state}"

            # ⬇⬇ SIEMPRE registra el paso al final de la iteración
            steps.append(TraceStep(step_no, str(stack), look_sym, act, note))
            step_no += 1

        return ok, steps, msg


def _leer_fuente_desde_cli() -> str:
    """
    Prioridad:
    1) --file RUTA  (o -f RUTA)
    2) primer argumento si es ruta existente
    3) primer argumento como código literal
    4) stdin si hay contenido redirigido
    5) cadena vacía (epsilon)
    """
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("-f", "--file", dest="file", help="Code.c")
    ap.add_argument("src", nargs="?", help="Código literal o ruta")
    ap.add_argument("--trace", dest="trace", type=int, default=30, help="Cuántos pasos imprimir (por defecto 30)")
    ap.add_argument("--help", action="store_true")
    ap.add_argument("--dump-lex", action="store_true", help="Muestra tokens del lexer")
    ap.add_argument("--dump-lr", action="store_true", help="Muestra columnas y celdas de la LR")

    args, _ = ap.parse_known_args()

    if args.help:
        print("Uso:")
        print("  python lr_parser_driver.py \"int x ;\"")
        print("  python lr_parser_driver.py ruta/al/archivo.c")
        print("  python lr_parser_driver.py -f ruta/al/archivo.c")
        print("  type archivo.c | python lr_parser_driver.py   (Windows)")
        print("  cat archivo.c | python3 lr_parser_driver.py   (Linux/Mac)")
        sys.exit(0)

    # 1) flag -f/--file
    if args.file:
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(), args

    # 2) si el primer argumento es ruta existente -> léelo como archivo
    if args.src and os.path.isfile(args.src):
        with open(args.src, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(), args

    # 3) si hay argumento y no es archivo -> trátalo como código literal
    if args.src:
        return args.src,args

    # 4) si llega por stdin (pipe/redirect)
    if not sys.stdin.isatty():
        return sys.stdin.read(), args

    # 5) sin entrada -> epsilon
    return "" , args

def _make_actions():
    A = {}

    # Program / DeclList
    A["Program → DeclList"] = lambda rhs: Program(funcs=[d for d in rhs[0] if isinstance(d, FuncDef)])

    A["DeclList → DeclList Decl"] = lambda rhs: (rhs[0] if isinstance(rhs[0], list) else []) + ([rhs[1]] if len(rhs) > 1 else [])

    A["DeclList → Decl"]          = lambda rhs: [rhs[0]]

    # Decl
    A["Decl → VarDecl ;"] = lambda rhs: None
    A["Decl → FunDef"]    = lambda rhs: rhs[0]

    # VarDecl (sin ;)
    A["VarDecl → tipo identificador"] = lambda rhs: ("vardecl", rhs[1])

    def _fun_def(rhs):
        # Acepta len 6 (con paréntesis) o len 4 (sin subirlos a la pila)
        if len(rhs) == 6:
            # rhs = [tipo, ident, '(', params, ')', Block]
            return FuncDef(name=rhs[1], params=rhs[3] or [], body=rhs[5])
        elif len(rhs) == 4:
            # rhs = [tipo, ident, params, Block]
            return FuncDef(name=rhs[1], params=rhs[2] or [], body=rhs[3])
        else:
            # Fallback informativo para depurar si tu LR usa otra aridad
            raise ValueError(f"FunDef: RHS inesperado len={len(rhs)} → {rhs}")

    A["FunDef → tipo identificador ( ParamListOpt ) Block"] = _fun_def

    # Params
    A["ParamListOpt → /* vacío */"] = lambda rhs: []
    A["ParamListOpt → ParamList"]   = lambda rhs: rhs[0]

    A["ParamList → Param"]              = lambda rhs: [rhs[0]]
    A["ParamList → ParamList , Param"]  = lambda rhs: rhs[0] + [rhs[2]]
    A["Param → tipo identificador"]     = lambda rhs: rhs[1]

    # Block / StmtList
    A["Block → { StmtListOpt }"] = lambda rhs: Block(stmts=rhs[1] or [])

    A["StmtListOpt → /* vacío */"] = lambda rhs: []
    A["StmtListOpt → StmtList"]    = lambda rhs: rhs[0]

    A["StmtList → Stmt"]           = lambda rhs: [rhs[0]]
    A["StmtList → StmtList Stmt"]  = lambda rhs: rhs[0] + [rhs[1]]

    # Stmt
    A["Stmt → VarDecl ;"]  = lambda rhs: None
    A["Stmt → Assign ;"]   = lambda rhs: rhs[0]
    A["Stmt → Return ;"]   = lambda rhs: rhs[0]

    # Assign / Return
    A["Assign → identificador = Expr"] = lambda rhs: Assign(target=Var(name=rhs[0]), value=rhs[2])
    A["Return → return Expr"]    = lambda rhs: Return(value=rhs[1])

    # Expr / Term / Factor
    A["Expr → Expr opSuma Term"] = lambda rhs: BinOp(op=rhs[1], left=rhs[0], right=rhs[2])
    A["Expr → Term"]             = lambda rhs: rhs[0]

    A["Term → Factor"]           = lambda rhs: rhs[0]

    A["Factor → identificador"]  = lambda rhs: Var(name=rhs[0])
    A["Factor → entero"]         = lambda rhs: Num(value=rhs[0])
    A["Factor → ( Expr )"]       = lambda rhs: rhs[1]
    A["Factor → Call"]           = lambda rhs: rhs[0]

    # Call / Args
    A["Call → identificador ( ArgListOpt )"] = lambda rhs: Call(name=rhs[0], args=rhs[2] or [])

    A["ArgListOpt → /* vacío */"] = lambda rhs: []
    A["ArgListOpt → ArgList"]     = lambda rhs: rhs[0]

    A["ArgList → Expr"]               = lambda rhs: [rhs[0]]
    A["ArgList → ArgList , Expr"]     = lambda rhs: rhs[0] + [rhs[2]]

    return A

def _as_list_of_stmts(x):
    # Block ya trae lista; una Stmt suelta la metemos en lista
    if x is None: return []
    if isinstance(x, Block): return x.stmts or []
    if isinstance(x, list): return x
    return [x]

def main():

    src, args = _leer_fuente_desde_cli()

    symbols, sym_to_col = load_symbol_headers(here("compilador.csv"))
    _, rules, nrows, ncols, table = load_lr_table(here("compilador.lr"))

   
    if getattr(args, "dump_lr", False):
        print(">> Columnas (CSV ↔ LR):")
    for i,s in enumerate(symbols):
        print(f"  col {i}: '{s}'")
    if ')' in sym_to_col and len(table) > 10:
        print(">> ACTION[10,')'] =", table[10][sym_to_col[')']])


    if ncols != len(symbols):
        raise ValueError(f"Desalineado: LR declara {ncols} columnas y CSV tiene {len(symbols)} símbolos.")

    parser = LRParser(table, rules, symbols, sym_to_col)

    

    ok, steps, result = parser.parse(src, trace=True)

    if getattr(args, "dump_lex", False):
        # muestra lexemas rápidos (sin modificar el parser)
        toks = AnalizadorLexico.analizador_lexico(src)
        print(f">> {len(toks)} tokens:")
        print("   ", " ".join(getattr(t, "valor", "?") for t in toks)[:300], "...")


    print("=== Resultado ===")
    if ok:
        print("Cadena aceptada")
    else:
        print(result)  # mensaje de error
        print("=== Trazas (primeras 200) ===")
        for s in steps[:200]:
            print(f"[{s.step:03}] {s.stack_repr:<60}  ⟂ {s.lookahead:<10}  act={s.action:>3}  {s.note}")
            if len(steps<200):
                print(f". . . {len(steps)-200} Pasos más.")
        return

    print("=== Trazas (primeras 200) ===")
    for s in steps[:200]:
        print(f"[{s.step:03}] {s.stack_repr:<60}  ⟂ {s.lookahead:<10}  act={s.action:>3}  {s.note}")

    # result es el AST (Program)
    ast_root = result
    # Generar IR y ASM
    from ir import gen_program
    from gen_emu8086 import gen_asm

    quads = gen_program(ast_root)
    asm = gen_asm(quads)
    out_path = here("programa.asm")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(asm)
    print(f"\nListo: {out_path} generado.")


if __name__ == "__main__":
    main()
