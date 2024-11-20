# dsl/parser.py

import ply.lex as lex
import ply.yacc as yacc

# List of token names. All should be uppercase
tokens = (
    'IDENTIFIER',  # Must be first to avoid conflicts
    'QUBIT',
    'H',
    'X',
    'S',
    'T',
    'RZ',
    'CNOT',
    'MEASURE',
    'PRINT',
    'ALICE_SEND',
    'BOB_MEASURE',
    'SIFT_KEYS',
    'CHECK_EAVESDROPPING',
    'GENERATE_KEY',
    'EAVESDROP',
    'NUMBER',
    'RANDOM_GATE',
)

# Reserved words dictionary
reserved = {
    'qubit': 'QUBIT',
    'h': 'H',
    'x': 'X',
    's': 'S',
    't': 'T',
    'rz': 'RZ',
    'cnot': 'CNOT',
    'measure': 'MEASURE',
    'print': 'PRINT',
    'alice_send': 'ALICE_SEND',
    'bob_measure': 'BOB_MEASURE',
    'sift_keys': 'SIFT_KEYS',
    'check_eavesdropping': 'CHECK_EAVESDROPPING',
    'generate_key': 'GENERATE_KEY',
    'eavesdrop': 'EAVESDROP',
}

# Regular expression rules for simple tokens
t_H = r'h'
t_X = r'x'
t_S = r's'
t_T = r't'
t_RZ = r'rz'
t_CNOT = r'cnot'
t_MEASURE = r'measure'
t_PRINT = r'print'
t_ALICE_SEND = r'alice_send'
t_BOB_MEASURE = r'bob_measure'
t_SIFT_KEYS = r'sift_keys'
t_CHECK_EAVESDROPPING = r'check_eavesdropping'
t_GENERATE_KEY = r'generate_key'
t_EAVESDROP = r'eavesdrop'

# A regular expression rule with some action code
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Check for reserved words
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Comment rule: Ignore comments
def t_COMMENT(t):
    r'\#.*'
    pass  # Token discarded

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules

def p_script(p):
    '''script : statements'''
    p[0] = p[1]

def p_statements_multiple(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]

def p_statement_qubit(p):
    '''statement : QUBIT IDENTIFIER'''
    p[0] = ('qubit', p[2])

def p_statement_h(p):
    '''statement : H IDENTIFIER'''
    p[0] = ('h', p[2])

def p_statement_x(p):
    '''statement : X IDENTIFIER'''
    p[0] = ('x', p[2])

def p_statement_s(p):
    '''statement : S IDENTIFIER'''
    p[0] = ('s', p[2])

def p_statement_t(p):
    '''statement : T IDENTIFIER'''
    p[0] = ('t', p[2])

def p_statement_rz(p):
    '''statement : RZ IDENTIFIER NUMBER'''
    p[0] = ('rz', p[2], p[3])

def p_statement_cnot(p):
    '''statement : CNOT IDENTIFIER IDENTIFIER'''
    p[0] = ('cnot', p[2], p[3])

def p_statement_measure(p):
    '''statement : MEASURE IDENTIFIER IDENTIFIER'''
    p[0] = ('measure', p[2], p[3])

def p_statement_print(p):
    '''statement : PRINT IDENTIFIER'''
    p[0] = ('print', p[2])

def p_statement_alice_send(p):
    '''statement : ALICE_SEND IDENTIFIER'''
    p[0] = ('alice_send', p[2])

def p_statement_bob_measure(p):
    '''statement : BOB_MEASURE IDENTIFIER IDENTIFIER'''
    p[0] = ('bob_measure', p[2], p[3])

def p_statement_sift_keys(p):
    '''statement : SIFT_KEYS'''
    p[0] = ('sift_keys',)

def p_statement_check_eavesdropping(p):
    '''statement : CHECK_EAVESDROPPING'''
    p[0] = ('check_eavesdropping',)

def p_statement_generate_key(p):
    '''statement : GENERATE_KEY IDENTIFIER'''
    p[0] = ('generate_key', p[2])

def p_statement_eavesdrop(p):
    '''statement : EAVESDROP'''
    p[0] = ('eavesdrop',)

def p_statement_random_gate(p):
    '''statement : RANDOM_GATE IDENTIFIER'''
    p[0] = ('random_gate', p[2])
    
def p_statement_random_cnot(p):
    '''statement : RANDOM_GATE IDENTIFIER IDENTIFIER'''
    p[0] = ('random_gate', p[2], p[3])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Parse function
def parse(data):
    return parser.parse(data)
