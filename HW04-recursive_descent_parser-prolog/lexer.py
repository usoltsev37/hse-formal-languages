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

t_ID = r'[a-z_][a-z_]*'
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


def findColumn(self):
    line_start = self.data.rfind('\n', 0, self.lexpos) + 1
    return (self.lexpos.lexpos - line_start) + 1


def Lex(s):
    lexer = lex.lex()
    lexer.input(s)
    while True:
        token = lexer.token()
        if not token:
            while True:
                yield None
        yield token
