import ply.lex as lex
import ply.yacc as yacc


tokens = (
    "KEYWORD",
    "IDENTIFIER",
    "INTEGER",
    "HEX",
    "FLOAT",
    "STRING",
    "CHAR",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "MOD",
    "OR",
    "AND",
    "NOT",
    "XOR",
    "LSHIFT",
    "RSHIFT",
    "LOR",
    "LAND",
    "LNOT",
    "LT",
    "LE",
    "GT",
    "GE",
    "EQ",
    "NE",
    "EQUALS",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "LBRACKET",
    "RBRACKET",
    "COMMA",
    "SEMI",
    "COLON",
    "DOT",
)

keywords = {
    "allocate",
    "bool",
    "break",
    "case",
    "char",
    "const",
    "continue",
    "declare",
    "default",
    "destruct",
    "double",
    "else",
    "false",
    "function",
    "float",
    "for",
    "if",
    "input",
    "int",
    "long",
    "output",
    "return",
    "sizeof",
    "static",
    "string",
    "switch",
    "true",
    "type",
}

t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_MOD = r"%"
t_OR = r"\|"
t_AND = r"&"
t_NOT = r"!"
t_XOR = r"\^"
t_LT = r"<"
t_GT = r">"
t_LE = r"<="
t_GE = r">="
t_EQ = r"=="
t_NE = r"!="
t_EQUALS = r"="
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_COMMA = r","
t_SEMI = r";"
t_COLON = r":"
t_DOT = r"\."

t_ignore = " \t"

def t_FLOAT(t):
    r"\d*\.\d+|\d+\.\d*"
    t.value = float(t.value)
    return t

# def t_HEX(t):
#     r"0x[0-9a-fA-F]+"
#     t.value = int(t.value, 16)
#     return t

def t_HEXINT(t):
    r"0x[0-9a-fA-F]+"
    t.type = "INTEGER"
    t.value = int(t.value, 16)
    return t

def t_INTEGER(t):
    r"\d+"
    t.value = int(t.value)
    return t

def t_STRING(t):
    r"\"([^\\\n]|(\\.))*?\""
    return t

def t_IDENTIFIER(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"
    if t.value in keywords:
        t.type = "KEYWORD"
    return t

def t_comment(t):
    r"(\#\#.*)|(\#/(.|\n)*?/\#)"
    pass

def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

def t_KEYWORD(t):
    r'(if|else|for|while|return|break|continue|destruct|sizeof|goto|input|output|function|type|declare|allocate|bool|char|const|double|float|int|long|string|switch|case|default)'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

def test_lexer(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

# if __name__ == "__main__":
#     test_input = """
# x = 12
# y = 0x1A
# if(x<=3):
#     print("yes")
# """.strip("").strip("\n")

#     test_lexer(test_input)

# Define the precedence of operators
precedence = (
    ('left', 'LOR'),
    ('left', 'LAND'),
    ('left', 'OR'),
    ('left', 'XOR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'NE'),
    ('nonassoc', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS', 'NOT', 'LNOT'),
)

# Parser rules
def p_program(p):
    '''program : ft_dcl_def_list'''
    p[0] = ('program', p[1])

def p_ft_dcl_def_list(p):
    '''ft_dcl_def_list : ft_dcl_def_list ft_dcl
                       | ft_dcl_def_list ft_def
                       | empty'''
    if len(p) == 3:
        p[0] = list(p[1]) + [p[2]]
    else:
        p[0] = []


def p_ft_dcl_content(p):
    '''ft_dcl_content : func_dcl
                      | global_var
                      | ft_dcl_content func_dcl
                      | ft_dcl_content global_var'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_func_dcl(p):
    '''func_dcl : func_prot SEMI'''
    p[0] = ('func_dcl', p[1])


def p_args(p):
    '''args : type
            | type COMMA args'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_params(p):
    '''params : type IDENTIFIER
              | type IDENTIFIER COMMA params'''
    if len(p) == 3:
        p[0] = [('param', p[1], p[2])]
    else:
        p[0] = [('param', p[1], p[2])] + p[4]

def p_type(p):
    '''type : KEYWORD
            | IDENTIFIER
            | type LBRACKET RBRACKET'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('array', p[1])



def p_ft_def(p):
    '''ft_def : func_def
              | type_def'''
    p[0] = p[1]


def p_inout(p):
    '''inout : input_list output_list
             | input_list
             | output_list
             | empty'''
    if len(p) == 3:
        p[0] = ('inout', p[1], p[2])
    elif len(p) == 2:
        if p[1][0] == 'input':
            p[0] = ('inout', p[1], None)
        elif p[1][0] == 'output':
            p[0] = ('inout', None, p[1])
    else:
        p[0] = ('inout', None, None)



def p_type_dcl(p):
    '''type_dcl : type_dcl_list'''
    p[0] = ('type_dcl', p[1])

def p_type_dcl_list(p):
    '''type_dcl_list : IDENTIFIER SEMI
                     | IDENTIFIER SEMI type_dcl_list'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_field_list(p):
    '''field_list : field SEMI
                  | field SEMI field_list'''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_field(p):
    '''field : type IDENTIFIER'''
    p[0] = ('field', p[1], p[2])

def p_block(p):
    '''block : LBRACE block_content RBRACE'''
    p[0] = ('block', p[2])

def p_block_content(p):
    '''block_content : var_dcl block_content
                     | statement block_content
                     | empty'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_var_dcl_list(p):
    '''var_dcl_list : COMMA var_dcl_cnt var_dcl_list
                    | empty'''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

def p_statement(p):
    '''statement : assignment SEMI
                 | func_call SEMI
                 | cond_stmt
                 | loop_stmt
                 | return_stmt
                 | break_stmt
                 | continue_stmt
                 | goto SEMI
                 | label
                 | expr SEMI
                 | destruct_stmt
                 | sizeof_stmt'''
    p[0] = p[1]

def p_return_stmt(p):
    '''return_stmt : KEYWORD SEMI'''
    if p[1].lower() == 'return':
        p[0] = ('return',)
    else:
        raise SyntaxError("Invalid return statement")



def p_expr(p):
    '''expr : expr binary_op expr
            | LPAREN expr RPAREN
            | func_call
            | variable
            | const_val
            | MINUS MINUS expr %prec UMINUS
            | NOT expr'''
    if len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = ('binary_op', p[2], p[1], p[3])
    elif len(p) == 3:
        p[0] = ('unary_op', p[1], p[2])
    else:
        p[0] = p[1]

def p_binary_op(p):
    '''binary_op : PLUS
                 | MINUS
                 | TIMES
                 | DIVIDE
                 | MOD
                 | AND
                 | OR
                 | LOR
                 | LAND
                 | EQ
                 | NE
                 | GE
                 | LE
                 | LT
                 | GT'''
    p[0] = p[1]


def p_assignment(p):
    '''assignment : variable EQUALS expr'''
    p[0] = ('assignment', p[1], p[3])

def p_func_call(p):
    '''func_call : IDENTIFIER LPAREN parameters RPAREN'''
    p[0] = ('func_call', p[1], p[3])

def p_parameters(p):
    '''parameters : expr
                  | expr COMMA parameters
                  | empty'''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    else:
        p[0] = [p[1]] + p[3]



def p_loop_stmt(p):
    '''loop_stmt : KEYWORD LPAREN var_dcl COLON expr COLON assignment RPAREN block'''
    if p[1].lower() == 'for':
        p[0] = ('for', p[3], p[5], p[7], p[9])
    else:
        raise SyntaxError(f"Expected 'for' keyword, found '{p[1]}'")

def p_label(p):
    '''label : IDENTIFIER COLON'''
    p[0] = ('label', p[1])

def p_variable(p):
    '''variable : IDENTIFIER
                | IDENTIFIER LBRACE expr RBRACE
                | IDENTIFIER DOT variable'''
    if len(p) == 2:
        p[0] = ('var', p[1])
    elif len(p) == 5:
        p[0] = ('array_access', p[1], p[3])
    else:
        p[0] = ('struct_access', p[1], p[3])
        

def p_cond_stmt(p):
    '''cond_stmt : KEYWORD LPAREN expr RPAREN block
                 | KEYWORD LPAREN expr RPAREN block KEYWORD block'''
    if len(p) == 6 and p[1].lower() == 'if':
        p[0] = ('if', p[3], p[5])
    elif len(p) == 8 and p[1].lower() == 'if' and p[6].lower() == 'else':
        p[0] = ('if_else', p[3], p[5], p[7])
    else:
        raise SyntaxError("Invalid conditional statement")



def p_break_stmt(p):
    '''break_stmt : KEYWORD SEMI'''
    if p[1].lower() == 'break':
        p[0] = ('break',)
    else:
        raise SyntaxError("Invalid break statement")

def p_continue_stmt(p):
    '''continue_stmt : KEYWORD SEMI'''
    if p[1].lower() == 'continue':
        p[0] = ('continue',)
    else:
        raise SyntaxError("Invalid continue statement")

def p_destruct_stmt(p):
    '''destruct_stmt : KEYWORD LBRACE RBRACE IDENTIFIER SEMI'''
    if p[1].lower() == 'destruct':
        p[0] = ('destruct', p[4])
    else:
        raise SyntaxError("Invalid destruct statement")

def p_sizeof_stmt(p):
    '''sizeof_stmt : KEYWORD LPAREN type RPAREN SEMI'''
    if p[1].lower() == 'sizeof':
        p[0] = ('sizeof', p[3])
    else:
        raise SyntaxError("Invalid sizeof statement")

def p_goto(p):
    '''goto : KEYWORD IDENTIFIER'''
    if p[1].lower() == 'goto':
        p[0] = ('goto', p[2])
    else:
        raise SyntaxError("Invalid goto statement")
    
def p_ft_dcl(p):
    '''ft_dcl : KEYWORD LBRACE ft_dcl_content RBRACE'''
    if p[1].lower() == 'declare':
        p[0] = ('ft_dcl', p[3])
    else:
        raise SyntaxError("Invalid declaration")
    
def p_func_def(p):
    '''func_def : KEYWORD IDENTIFIER COLON inout block'''
    if p[1].lower() == 'function':
        p[0] = ('func_def', p[2], p[4], p[5])
    else:
        raise SyntaxError("Invalid function definition")



def p_type_def(p):
    '''type_def : KEYWORD IDENTIFIER LBRACE field_list RBRACE'''
    if p[1].lower() == 'type':
        p[0] = ('type_def', p[2], p[4])
    else:
        raise SyntaxError("Invalid type definition")

def p_var_dcl(p):
    '''var_dcl : type var_dcl_cnt var_dcl_list SEMI
               | KEYWORD type var_dcl_cnt var_dcl_list SEMI'''
    if len(p) == 5:
        p[0] = ('var_dcl', p[1], p[2], p[3])
    elif len(p) == 6 and p[1].lower() == 'const':
        p[0] = ('const_var_dcl', p[2], p[3], p[4])
    else:
        raise SyntaxError("Invalid variable declaration")

def p_var_dcl_cnt(p):
    '''var_dcl_cnt : IDENTIFIER
                   | IDENTIFIER EQUALS expr
                   | IDENTIFIER EQUALS KEYWORD'''
    if len(p) == 2:
        p[0] = ('var', p[1])
    elif len(p) == 4:
        if p[3] == 'allocate':
            p[0] = ('var_allocate', p[1])
        else:
            p[0] = ('var_init', p[1], p[3])

def p_input_list(p):
    '''input_list : KEYWORD LPAREN params RPAREN
                  | KEYWORD LPAREN RPAREN'''
    if p[1].lower() == 'input':
        if len(p) == 5:
            p[0] = ('input', p[3])
        else:
            p[0] = ('input', None)
    else:
        raise SyntaxError("Invalid input list")

def p_output_list(p):
    '''output_list : KEYWORD LPAREN params RPAREN
                   | KEYWORD LPAREN RPAREN'''
    if p[1].lower() == 'output':
        if len(p) == 5:
            p[0] = ('output', p[3])
        else:
            p[0] = ('output', None)
    else:
        raise SyntaxError("Invalid output list")

def p_const_val(p):
    '''const_val : INTEGER
                 | FLOAT
                 | STRING
                 | KEYWORD'''  # KEYWORD for true/false
    if p[1].lower() in ['true', 'false']:
        p[0] = ('bool_const', p[1].lower() == 'true')
    else:
        p[0] = ('const', p[1])
        
# Updated global_var rule
def p_global_var(p):
    '''global_var : type IDENTIFIER SEMI'''
    p[0] = ('global_var', p[1], p[2])

# Remove or adjust the global_var_list if necessary
def p_global_var_list(p):
    '''global_var_list : global_var
                       | global_var global_var_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# Adjust func_prot to use args for return types if needed
def p_func_prot(p):
    '''func_prot : LPAREN args RPAREN MINUS GT LPAREN params RPAREN
                 | LPAREN RPAREN MINUS GT LPAREN params RPAREN
                 | LPAREN args RPAREN MINUS GT LPAREN RPAREN
                 | LPAREN RPAREN MINUS GT LPAREN RPAREN'''
    if len(p) == 9:  # (args) -> (params)
        p[0] = ('func_prot', p[2], p[7])
    elif len(p) == 8:
        if p[2] == ')':  # () -> (params)
            p[0] = ('func_prot', None, p[6])
        else:  # (args) -> ()
            p[0] = ('func_prot', p[2], None)
    elif len(p) == 7:  # () -> ()
        p[0] = ('func_prot', None, None)
        
def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ({p.value}) on line {p.lineno}")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Test function
def parse(data):
    result = parser.parse(data)
    return result

if __name__ == "__main__":
    test_input = """
 x = 12
 y = 0x1A
 if(x<=3):
     print("yes")
 """.strip("").strip("\n")

    test_lexer(test_input)
    # Test input
    test_input = """
    declare {
        (int, float) -> (bool result);
        int global_var;
    }
    
    function test_func: input(int a, float b) output(bool result) {
        if (a > b) {
            result = true;
        } else {
            result = false;
        }
    }
    """
    
    result = parse(test_input)
    print(result)
