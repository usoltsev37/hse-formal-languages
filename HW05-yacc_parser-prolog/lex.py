import ply.lex as lex

tokens = [
    'SPIN',  # :-
    'DISJ',  # ;
    'CONJ',  # ,
    'POINT',
    'ID',
    'LBRACKET',
    'RBRACKET'
]

t_ID = r'[a-z_A-Z][a-z_A-Z0-9]*'
t_SPIN = r':-'
t_DISJ = r';'
t_CONJ = r','
t_POINT = r'\.'
t_LBRACKET = r'\('
t_RBRACKET = r'\)'

t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
