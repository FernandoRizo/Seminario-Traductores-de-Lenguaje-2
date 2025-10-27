# ir.py
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

Quad = Tuple[str, Optional[str], Optional[str], Optional[str]]

@dataclass
class IR:
    code: List[Quad] = field(default_factory=list)
    temp_i: int = 0
    label_i: int = 0

    def emit(self, q: Quad):
        self.code.append(q)

    def new_temp(self) -> str:
        self.temp_i += 1
        return f"t{self.temp_i}"

    def new_label(self, base="L") -> str:
        self.label_i += 1
        return f"{base}{self.label_i}"

def gen_expr(ir: IR, node) -> str:
    # Devuelve el nombre del temporal/variable/literal donde queda el valor
    if node.type == "Num":
        t = ir.new_temp()
        ir.emit(("=", str(node.value), None, t))
        return t

    if node.type == "Var":
        return node.name

    if node.type == "String":
        # reservar literal en el pool: STR1, STR2, ...
        label = ir.new_label("STR")
        ir.emit(("strlit", node.value, None, label))  # (texto, -, label)
        return label  # representará su dirección

    if node.type == "BinOp":
        a = gen_expr(ir, node.left)
        b = gen_expr(ir, node.right)
        t = ir.new_temp()
        ir.emit((node.op, a, b, t))  # '+','-','*','/','<','>','<=','>=','==','!='
        return t

    if node.type == "Call":
        # Caso especial: printf(...)
        if node.name == "printf":
            args = [gen_expr(ir, a) for a in node.args or []]
            if len(args) == 1:
                # printf(x) -> imprime entero x
                ir.emit(("printf_i", args[0], None, None))
                t = ir.new_temp()
                ir.emit(("=", "0", None, t))  # valor de retorno ficticio
                return t
            elif len(args) >= 2:
                # printf("%d\n", x)  -> imprime entero x y salto de línea
                # (ignoramos la cadena de formato y asumimos %d\n)
                fmt, val = args[0], args[1]
                ir.emit(("printf_si", fmt, val, None))
                t = ir.new_temp()
                ir.emit(("=", "0", None, t))
                return t
            else:
                # sin args: no imprimimos nada
                t = ir.new_temp()
                ir.emit(("=", "0", None, t))
                return t

        # Caso especial: getchar()
        if node.name == "getchar":
            ir.emit(("getchar", None, None, None))
            t = ir.new_temp()
            ir.emit(("=", "0", None, t))
            return t

        # Llamada normal: empuja parámetros derecha→izquierda
        for arg in reversed(node.args or []):
            v = gen_expr(ir, arg)
            ir.emit(("param", v, None, None))
        t = ir.new_temp()
        ir.emit(("call", node.name, str(len(node.args or [])), t))
        return t

    raise NotImplementedError(node.type)

def gen_stmt(ir: IR, node):
    if node is None:
        return
    if isinstance(node, list):
        for s in node:
            gen_stmt(ir, s)
        return
    if node.type == "Block":
        for s in (node.stmts or []):
            gen_stmt(ir, s)
        return
    if node.type == "Assign":
        dst = node.target.name
        src = gen_expr(ir, node.value)
        ir.emit(("=", src, None, dst))  # asignación: '=' (src -> dst)
        return
    if node.type == "Return":
        val = gen_expr(ir, node.value)
        ir.emit(("ret", val, None, None))  # 'ret' con valor
        return
    if node.type == "While":
        L_cond = ir.new_label("Lcond")
        L_body = ir.new_label("Lbody")
        L_end  = ir.new_label("Lend")
        ir.emit(("label", None, None, L_cond))
        a = gen_expr(ir, node.cond.left)
        b = gen_expr(ir, node.cond.right)
        op = "if" + node.cond.op    # if<, if>, if<=, ...
        ir.emit((op, a, b, L_body))
        ir.emit(("goto", None, None, L_end))
        ir.emit(("label", None, None, L_body))
        for s in (node.body or []):
            gen_stmt(ir, s)
        ir.emit(("goto", None, None, L_cond))
        ir.emit(("label", None, None, L_end))
        return
    if node.type == "ExprStmt":
        gen_expr(ir, node.expr)
        return
    # Si llega algo no manejado, deja una marca de TODO
    ir.emit(("; TODO", f"stmt {node.type}", None, None))

def gen_func(ir: IR, fnode):
    # Anuncia función y número de parámetros
    nparams = len(fnode.params or [])
    ir.emit(("func", fnode.name, str(nparams), None))

    # >>> NUEVO: declarar parámetros con nombre e índice
    for i, pname in enumerate(fnode.params or []):
        ir.emit(("defparam", pname, str(i), None))

    # Cuerpo
    for s in (fnode.body.stmts or []):
        gen_stmt(ir, s)

    # Fin de función
    ir.emit(("endfunc", fnode.name, None, None))

def gen_program(ast_root):
    ir = IR()
    for f in getattr(ast_root, "funcs", []):
        gen_func(ir, f)
    return ir.code
