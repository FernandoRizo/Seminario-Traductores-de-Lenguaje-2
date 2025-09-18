# -*- coding: utf-8 -*-
"""
Terminal:
    python lr_parser_driver.py "int x ;"
    python lr_parser_driver.py "int main ( ) { return 0 ; }"
    python lr_parser_driver.py             
"""
import sys
import os
import csv
import importlib.util
from dataclasses import dataclass
from typing import List, Tuple

BASE = os.path.dirname(os.path.abspath(__file__))
def here(*parts): return os.path.join(BASE, *parts)

# === Carga módulos del usuario (desde la misma carpeta) ===
def _load_module(name: str, path: str):
    path = os.path.abspath(path)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"No pude cargar {name} desde {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    return module

AnalizadorLexico = _load_module("AnalizadorLexico", here("AnalizadorLexico.py"))
simbolos_lexicos = _load_module("simbolos_lexicos", here("simbolos_lexicos.py"))

Estado = simbolos_lexicos.Estado
Terminal = simbolos_lexicos.Terminal
NoTerminal = simbolos_lexicos.NoTerminal
Pila = simbolos_lexicos.Pila

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
            mapped.append((sym, self.sym_to_col[sym]))
        mapped.append(('$', self.sym_to_col['$']))
        return mapped

    def parse(self, code: str, trace: bool = True):
        stack = Pila()
        stack.push(Estado(0))
        input_syms = self._tokenize(code)
        ip = 0
        steps: List[TraceStep] = []
        step_no = 0

        def stack_str() -> str:
            return str(stack)

        while True:
            state = stack.top().id
            look_sym, look_col = input_syms[ip]
            act = self.table[state][look_col]
            note = ""

            if act == 0:
                steps.append(TraceStep(step_no, stack_str(), look_sym, act, "ERROR"))
                return False, steps, f"Error sintáctico en estado {state} con símbolo '{look_sym}'"

            if act > 0:
                stack.push(Terminal(look_sym))
                stack.push(Estado(act))
                ip += 1
                note = f"shift → estado {act}"

            elif act == -1:
                steps.append(TraceStep(step_no, stack_str(), look_sym, act, "ACCEPT"))
                return True, steps, "Cadena aceptada"

            else:
                rule_no = -act - 1
                lhs_id, rhs_len, lhs_name = self.rules[rule_no - 1]
                for _ in range(rhs_len):
                    stack.pop(); stack.pop()
                top_state = stack.top().id
                goto_state = self.table[top_state][lhs_id]
                if goto_state <= 0:
                    steps.append(TraceStep(step_no, stack_str(), look_sym, act, f"reduce R{rule_no} → GOTO inválido"))
                    return False, steps, f"Error en GOTO después de R{rule_no} (top_state={top_state}, lhs_id={lhs_id})"
                stack.push(NoTerminal(lhs_name))
                stack.push(Estado(goto_state))
                note = f"reduce R{rule_no}: {lhs_name} (|rhs|={rhs_len}) → goto {goto_state}"

            if trace:
                steps.append(TraceStep(step_no, stack_str(), look_sym, act, note))
            step_no += 1

def main():
    symbols, sym_to_col = load_symbol_headers(here("compilador.csv"))
    _, rules, nrows, ncols, table = load_lr_table(here("compilador.lr"))
    parser = LRParser(table, rules, symbols, sym_to_col)

    if len(sys.argv) >= 2:
        src = sys.argv[1]
    else:
        src = ""  # ε
    ok, steps, msg = parser.parse(src, trace=True)
    print("=== Resultado ===")
    print(msg)
    print("=== Trazas (primeras 30) ===")
    for s in steps[:30]:
        print(f"[{s.step:03}] {s.stack_repr:<60}  ⟂ {s.lookahead:<10}  act={s.action:>3}  {s.note}")
    if len(steps) > 30:
        print(f"... ({len(steps)-30} pasos más)")

if __name__ == "__main__":
    main()
