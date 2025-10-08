# ast_nodes.py
from dataclasses import dataclass
from typing import List, Optional, Union

# Expresiones
@dataclass
class Num:
    type: str = "Num"
    value: int = 0

@dataclass
class Var:
    type: str = "Var"
    name: str = ""

@dataclass
class BinOp:
    type: str = "BinOp"
    op: str = ""             # '+','-','*','/','<','>','<=','>=','==','!='
    left: object = None
    right: object = None

@dataclass
class Call:
    type: str = "Call"
    name: str = ""
    args: List[object] = None

# Sentencias
@dataclass
class Assign:
    type: str = "Assign"
    target: Var = None
    value: object = None

@dataclass
class Return:
    type: str = "Return"
    value: Optional[object] = None

@dataclass
class If:
    type: str = "If"
    cond: BinOp = None            # o expresión booleana
    then_body: List[object] = None
    else_body: Optional[List[object]] = None

@dataclass
class While:
    type: str = "While"
    cond: BinOp = None
    body: List[object] = None

@dataclass
class ExprStmt:
    type: str = "ExprStmt"
    expr: object = None

@dataclass
class Block:
    type: str = "Block"
    stmts: List[object] = None

# Funciones y programa
@dataclass
class FuncDef:
    type: str = "FuncDef"
    name: str = ""
    params: List[str] = None
    body: Block = None

@dataclass
class Program:
    type: str = "Program"
    funcs: List[FuncDef] = None
