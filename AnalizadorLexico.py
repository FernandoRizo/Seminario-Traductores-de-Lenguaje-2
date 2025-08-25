# -*- coding: utf-8 -*-

import re

# --------------------------------------------------
# Clase Token
# --------------------------------------------------
class Token:
    
    def __init__(self, tipo, valor, tipo_num):
        self.tipo = tipo
        self.valor = valor
        self.tipo_num = tipo_num

    def __str__(self):
        # Representación en formato de tabla para una fácil lectura.
        return f'| {self.valor:<15} | {self.tipo:<20} | {self.tipo_num:<5} |'

# --------------------------------------------------
# Analizador Léxico
# --------------------------------------------------
def analizador_lexico(codigo):
    """
    Esta función toma una cadena de código como entrada y la divide en tokens.
    """
    
    # Lista de especificaciones de tokens en formato (TIPO, regex, VALOR_NUMERICO)

    especificaciones = [
        ('ESPACIO',         r'\s+',                     -1),
        ('COMENTARIO',      r'//.*',                    -1),

        # Cadena (simple, no cruza línea). Acepta escapes tipo \" \\ \n \t \r
        ('CADENA',          r'"([^"\\\n]|\\.)*"',       3),

        ('REAL',            r'\d+\.\d+',                2),
        ('ENTERO',          r'\d+',                     1),

        # Dos caracteres primero
        ('OP_AND',          r'&&',                      9),
        ('OP_OR',           r'\|\|',                    8),
        ('OP_IGUALDAD',     r'==|!=',                   11),
        ('OP_RELAC',        r'<=|>=|<|>',               7),

        # Un carácter
        ('ASIGNACION',      r'=',                       18),
        ('OP_SUMA',         r'\+|-',                    5),
        ('OP_MUL',          r'\*|/',                    6),
        ('OP_NOT',          r'!',                       10),

        # Delimitadores
        ('PUNTO_Y_COMA',    r';',                       12),
        ('COMA',            r',',                       13),
        ('PARENTESIS_IZQ',  r'\(',                      14),
        ('PARENTESIS_DER',  r'\)',                      15),
        ('LLAVE_IZQ',       r'\{',                      16),
        ('LLAVE_DER',       r'\}',                      17),

        ('FIN',             r'\$',                      23),

       
        ('IDENTIFICADOR',   r'[A-Za-z_][A-Za-z0-9_]*',  0),

        ('ERROR',           r'.',                       -1),
    ]

    palabras_reservadas = {
        'if':     ('IF', 19),
        'while':  ('WHILE', 20),
        'return': ('RETURN', 21),
        'else':   ('ELSE', 22),
        'int':    ('TIPO', 4),
        'float':  ('TIPO', 4),
        'void':   ('TIPO', 4),  
    }


    # Une todas las expresiones regulares en una sola.
    regex_unida = '|'.join(f'(?P<{tipo}>{regex})' for tipo, regex, _ in especificaciones)
    
    tokens_encontrados = []
    linea = 1
    columna = 1

    # Recorre todas las coincidencias en el código.
    for match in re.finditer(regex_unida, codigo):
        tipo_token = match.lastgroup
        valor = match.group()
        
        # Actualiza la columna para el seguimiento de errores.
        columna = match.start()

        if tipo_token == 'ESPACIO' or tipo_token == 'COMENTARIO':
            # Ignora los espacios y comentarios
            if '\n' in valor:
                linea += valor.count('\n')
            continue
        
        elif tipo_token == 'IDENTIFICADOR':
            # Si es un identificador, verifica si es una palabra reservada.
            if valor in palabras_reservadas:
                tipo, tipo_num = palabras_reservadas[valor]
                tokens_encontrados.append(Token(tipo, valor, tipo_num))
            else:
                tokens_encontrados.append(Token('IDENTIFICADOR', valor, 0)) 
        
        elif tipo_token == 'ERROR':
            print(f"Error: Carácter no reconocido '{valor}' en la línea {linea}, columna {columna}")
        
            
        else:
            # Para cualquier otro token, busca su tipo numérico en la lista de especificaciones.
            for tipo_spec, _, tipo_num_spec in especificaciones:
                if tipo_spec == tipo_token:
                    tokens_encontrados.append(Token(tipo_token, valor, tipo_num_spec))
                    break
    
    return tokens_encontrados

# --------------------------------------------------
# Código de Prueba
# --------------------------------------------------
if __name__ == '__main__':
    
    # Código de ejemplo para probar el analizador
    codigo_fuente = """
   
    int main() {
        int resultado = 0;
        float numero_real = 10.5;
        
        if (resultado >= 0 && numero_real > 10.0) {
            resultado = resultado + 1;
        } else {
            return 0;
        }
        
        while(resultado < 5) {
            resultado = resultado + 1;
        }
        
        // Fin del programa
        return resultado;
    }
    
    """
    
    # Obtenemos la lista de tokens
    lista_de_tokens = analizador_lexico(codigo_fuente)
    
    # Imprimimos la tabla de resultados
    print('-' * 55)
    print('| Lexema          | Tipo de Token        | Valor Numérico |')
    print('-' * 55)
    for token in lista_de_tokens:
        print(token)
    print('-' * 55)