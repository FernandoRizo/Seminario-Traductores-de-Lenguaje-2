# -*- coding: utf-8 -*-
import re
from dataclasses import dataclass
from typing import List

@dataclass
class Tok:
    tipo: str
    valor: str
    linea: int
    columna: int

# Palabras reservadas
RESERVADAS_TIPO = {"int", "float", "char", "void",}
RESERVADAS = {
    "if": "IF",
    "while": "WHILE",
    "return": "RETURN",
    "else": "ELSE",
    #"return" : "RETURN",
    #"main" : "MAIN"
}

# Regex base
_espacios = re.compile(r'[ \t\r]+')
_nl       = re.compile(r'\n')
_ident    = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')
_entero   = re.compile(r'[0-9]+')
_real     = re.compile(r'(?:[0-9]+\.[0-9]*|\.[0-9]+)(?:[eE][+-]?[0-9]+)?|[0-9]+[eE][+-]?[0-9]+')
_cadena   = re.compile(r'"(?:[^"\\]|\\.)*"')

def analizador_lexico(src: str) -> List[Tok]:
    i = 0
    linea = 1
    col = 1
    n = len(src)
    toks: List[Tok] = []

    def adv(m):
        nonlocal i, col, linea
        s, e = m.span()
        texto = src[s:e]
        i = e
        col += (e - s)
        return texto

    while i < n:
        # saltar espacios y comentarios
        m = _espacios.match(src, i)
        if m:
            adv(m)
            continue
        if src.startswith("//", i):
            j = src.find("\n", i)
            if j < 0: j = n
            col += (j - i)
            i = j
            continue
        if src.startswith("/*", i):
            j = src.find("*/", i+2)
            if j < 0:
                raise ValueError(f"Error léxico: comentario no cerrado en línea {linea}, columna {col}")
            # contar saltos de línea dentro del comentario
            comentario = src[i:j+2]
            nl_count = comentario.count("\n")
            if nl_count:
                linea += nl_count
                col = len(comentario.split("\n")[-1]) + 1
            else:
                col += len(comentario)
            i = j + 2
            continue

        # saltos de línea
        m = _nl.match(src, i)
        if m:
            adv(m)
            linea += 1
            col = 1
            continue

        # tokens complejos
        m = _real.match(src, i)
        if m:
            lex = adv(m)
            toks.append(Tok("REAL", lex, linea, col - len(lex)))
            continue

        m = _entero.match(src, i)
        if m:
            lex = adv(m)
            toks.append(Tok("ENTERO", lex, linea, col - len(lex)))
            continue

        m = _cadena.match(src, i)
        if m:
            lex = adv(m)
            toks.append(Tok("CADENA", lex, linea, col - len(lex)))
            continue

        m = _ident.match(src, i)
        if m:
            lex = adv(m)
            if lex in RESERVADAS_TIPO:
                toks.append(Tok("TIPO", lex, linea, col - len(lex)))
            elif lex in RESERVADAS:
                toks.append(Tok(RESERVADAS[lex], lex, linea, col - len(lex)))
            else:
                toks.append(Tok("IDENTIFICADOR", lex, linea, col - len(lex)))
            continue

        # Operadores (ordena por los de 2 chars primero)
        two = src[i:i+2]
        one = src[i]

        if two in ("==", "!=", "<=", ">=", "&&", "||"):
            tipo = {
                "&&": "OP_AND", "||": "OP_OR",
                "==": "OP_IGUALDAD", "!=": "OP_IGUALDAD",
                "<=": "OP_RELAC", ">=": "OP_RELAC",
            }[two]
            toks.append(Tok(tipo, two, linea, col))
            i += 2; col += 2
            continue

        if one in "+-":
            toks.append(Tok("OP_SUMA", one, linea, col)); i+=1; col+=1; continue
        if one in "*/%":
            toks.append(Tok("OP_MUL", one, linea, col)); i+=1; col+=1; continue
        if one in "<>":
            toks.append(Tok("OP_RELAC", one, linea, col)); i+=1; col+=1; continue
        if one == "!":
            toks.append(Tok("OP_NOT", "!", linea, col)); i+=1; col+=1; continue
        if one == "=":
            toks.append(Tok("ASIGNACION", "=", linea, col)); i+=1; col+=1; continue

        # Puntuación
        mapa_punc = {
            ";": "PUNTO_Y_COMA", ",": "COMA",
            "(": "PARENTESIS_IZQ", ")": "PARENTESIS_DER",
            "{": "LLAVE_IZQ",     "}": "LLAVE_DER",
        }
        if one in mapa_punc:
            toks.append(Tok(mapa_punc[one], one, linea, col)); i+=1; col+=1; continue

        # Si llegamos aquí, carácter inválido
        raise ValueError(f"Error léxico: carácter inválido '{src[i]}' en línea {linea}, columna {col}")

    return toks
