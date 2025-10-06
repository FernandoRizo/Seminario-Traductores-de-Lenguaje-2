

from collections import defaultdict, deque
import sys

# ===== 1) Definición de símbolos (DEBEN COINCIDIR CON compilador.csv) =====
TERMINALS = [
    "tipo","identificador","entero","(",")","{","}",";",
    ",","=","return","opSuma","$"
]
NONTERMINALS = [
    "Program","DeclList","Decl","VarDecl","FunDef","ParamListOpt","ParamList","Param",
    "Block","StmtListOpt","StmtList","Stmt","Assign","Return","Expr","Term","Factor",
    "Call","ArgListOpt","ArgList"
]

SYMBOLS = TERMINALS + NONTERMINALS
SYM2IDX = {s:i for i,s in enumerate(SYMBOLS)}

# ===== 2) Gramática =====
# Formato: dict LHS -> list of RHS (cada RHS es tuple de símbolos)
G = defaultdict(list)

def R(lhs, rhs):
    parts = rhs.split()
    if parts == ["ε"]:
        G[lhs].append(tuple())       # <<<< producción VACÍA
    else:
        G[lhs].append(tuple(parts))

# Reglas (idénticas al bloque BNF de arriba, en el MISMO orden para numeración estable):
R("Program",       "DeclList")

R("DeclList",      "DeclList Decl")
R("DeclList",      "Decl")

R("Decl",          "VarDecl ;")
R("Decl",          "FunDef")

R("VarDecl",       "tipo identificador")

R("FunDef",        "tipo identificador ( ParamListOpt ) Block")

R("ParamListOpt",  "ε")
R("ParamListOpt",  "ParamList")

R("ParamList",     "Param")
R("ParamList",     "ParamList , Param")

R("Param",         "tipo identificador")

R("Block",         "{ StmtListOpt }")

R("StmtListOpt",   "ε")
R("StmtListOpt",   "StmtList")

R("StmtList",      "Stmt")
R("StmtList",      "StmtList Stmt")

R("Stmt",          "VarDecl ;")
R("Stmt",          "Assign ;")
R("Stmt",          "Return ;")

R("Assign",        "identificador = Expr")

R("Return",        "return Expr")

R("Expr",          "Expr opSuma Term")
R("Expr",          "Term")

R("Term",          "Factor")

R("Factor",        "identificador")
R("Factor",        "entero")
R("Factor",        "( Expr )")
R("Factor",        "Call")

R("Call",          "identificador ( ArgListOpt )")

R("ArgListOpt",    "ε")
R("ArgListOpt",    "ArgList")

R("ArgList",       "Expr")
R("ArgList",       "ArgList , Expr")

# Augment grammar: S' -> Program
START = "Program"
AUG_START = "S'"
G[AUG_START] = [(START,)]

# Map rules to (lhs_id, rhs_len, lhs_name) for output: lhs_id es índice de la columna del NoTerminal
RULES = []
RULE_LHS = []
for lhs in [AUG_START] + NONTERMINALS:
    for rhs in G[lhs]:
        if lhs == AUG_START:  # no se imprime como regla del usuario
            continue
for lhs in NONTERMINALS:
    for rhs in G[lhs]:
        RULES.append((SYM2IDX[lhs], 0 if rhs==("ε",) else len(rhs), lhs))
        RULE_LHS.append((lhs, rhs))

# ===== 3) FIRST/FOLLOW para SLR(1) =====
FIRST = {s:set() for s in SYMBOLS}
FOLLOW = {A:set() for A in NONTERMINALS}
FIRST[AUG_START] = set()
FOLLOW[AUG_START] = set()

for t in TERMINALS:
    FIRST[t].add(t)

def first_of_seq(seq):
    if len(seq) == 0:           # <<<< secuencia vacía = ε
        return {"ε"}
    out = set()
    for X in seq:
        out |= (FIRST[X] - {"ε"})
        if "ε" not in FIRST[X]:
            break
    else:
        out.add("ε")
    return out

changed=True
while changed:
    changed=False
    for A in NONTERMINALS + [AUG_START]:
        for beta in G[A]:
            if len(beta) == 0:
                if "ε" not in FIRST[A]:
                    FIRST[A].add("ε"); changed=True
            else:
                f = first_of_seq(beta)
                if not f- FIRST[A]:
                    pass
                else:
                    FIRST[A] |= (f-{"ε"}); changed=True

FOLLOW[START].add("$")
changed=True
while changed:
    changed=False
    for A in NONTERMINALS + [AUG_START]:
        for beta in G[A]:
            # if len(beta) == 0:                  # <<<< producción ε
            #     if "ε" not in FIRST[A]:
            #         FIRST[A].add("ε"); changed = True
            # else:
            #     f = first_of_seq(beta)
            #     if not (f - FIRST[A]):
            #         pass
            #     else:
            #         FIRST[A] |= (f - {"ε"}); changed = True
            for i,X in enumerate(beta):
                if X in NONTERMINALS:
                    trail = tuple(beta[i+1:]) if i+1 < len(beta) else tuple()
                    f = first_of_seq(trail)
                    add = (f - {"ε"})
                    if not add.issubset(FOLLOW[X]):
                        FOLLOW[X] |= add; changed = True
                    if "ε" in f or len(trail) == 0:             # <<<< trail vacío
                        if not FOLLOW[A].issubset(FOLLOW[X]):
                            FOLLOW[X] |= FOLLOW[A]; changed = True

# ===== 4) Items LR(0) y construcción C (automata) =====
def closure(items):
    # items: set of (A, alpha, •, beta)
    I=set(items)
    added=True
    while added:
        added=False
        for (A,alpha,dot,beta) in list(I):
            if beta:
                B = beta[0]
                if B in NONTERMINALS or B==AUG_START:
                    for gamma in G[B]:
                        itm = (B, tuple(), 0, tuple(gamma))
                        if itm not in I:
                            I.add(itm); added=True
    return frozenset(I)

def goto(I,X):
    J=set()
    for (A,alpha,dot,beta) in I:
        if beta and beta[0]==X:
            J.add((A, alpha+(beta[0],), 0, beta[1:]))
    return closure(J) if J else None

# inicial
C=[]
start_item = closure({(AUG_START, tuple(), 0, (START,))})
C.append(start_item)
W=deque([start_item])
EDGES={}
while W:
    I=W.popleft()
    for X in SYMBOLS:
        J = goto(I,X)
        if J:
            EDGES.setdefault(I,{})[X]=J
            if J not in C:
                C.append(J); W.append(J)

state_index = {I:i for i,I in enumerate(C)}

# ===== 5) ACTION/GOTO SLR(1) =====
nrows = len(C)
ncols = len(SYMBOLS)
TAB = [[0]*ncols for _ in range(nrows)]

# indexado de reglas para reduce: usamos orden RULE_LHS
# Construimos una lista con (lhs, rhs) para numerarlas 1..N
RULE_LIST = []
for lhs in NONTERMINALS:
    for rhs in G[lhs]:
        if rhs==("ε",):   # epsilon es RHS de len 0
            RULE_LIST.append( (lhs, tuple()) )
        else:
            RULE_LIST.append( (lhs, tuple(rhs)) )

def rule_no_of(lhs, rhs):
    # numeración 1..N siguiendo RULE_LIST
    for i,(L,R) in enumerate(RULE_LIST, start=1):
        if L==lhs and R==rhs:
            return i
    raise RuntimeError("Regla no encontrada")

ACCEPT_SET = set()

for I in C:
    s = state_index[I]
    # shifts
    for X,J in EDGES.get(I,{}).items():
        j = state_index[J]
        if X in TERMINALS:
            col = SYM2IDX[X]
            TAB[s][col] = j  # shift j

    # reduces
    for (A,alpha,dot,beta) in I:
        if A==AUG_START and beta==() and not alpha:
            # no debería pasar aquí
            pass
        if beta == ():
            if A == AUG_START and alpha == (START,):
                TAB[s][SYM2IDX["$"]] = -1  # ACCEPT
            else:
                rno = rule_no_of(A, alpha)     # alpha es la RHS consumida (puede ser vacía)
                for a in FOLLOW[A]:
                    col = SYM2IDX[a]
                    TAB[s][col] = -(rno + 1)

    # gotos (NoTerminales)
    for X,J in EDGES.get(I,{}).items():
        if X in NONTERMINALS:
            TAB[s][SYM2IDX[X]] = state_index[J]

# ===== 6) Salida compilador.lr =====
# Reglas para la cabecera del archivo: (lhs_id, rhs_len, lhs_name)
RULES_OUT = []
for lhs, rhs in RULE_LIST:
    lhs_id = SYM2IDX[lhs]
    rhs_len = len(rhs)  
    RULES_OUT.append((lhs_id, rhs_len, lhs))

with open("compilador.lr","w",encoding="utf-8") as f:
    f.write(str(len(RULES_OUT))+"\n")
    for lhs_id, rhs_len, lhs in RULES_OUT:
        f.write(f"{lhs_id} {rhs_len} {lhs}\n")
    f.write(f"{nrows} {ncols}\n")
    for r in range(nrows):
        row = " ".join(str(x) for x in TAB[r])
        f.write(row+"\n")

print("Listo: compilador.lr generado.")
print(f"Estados: {nrows}, Columnas: {ncols}")
