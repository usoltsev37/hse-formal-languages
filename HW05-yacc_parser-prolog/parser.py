import ply.yacc as yacc
import sys
from lex import tokens


def p_ref(p):
    '''ref  : atom POINT
            | atom SPIN disj POINT'''
    if len(p) == 3:
        p[0] = f'{p[1]} POINT'
    else:
        p[0] = f'SPIN ( {p[1]}, {p[3]} ) POINT'


def p_disj(p):
    '''disj : conj DISJ disj
            | conj'''
    if len(p) == 4:
        p[0] = f'DISJ ({p[1]}, {p[3]})'
    else:
        p[0] = p[1]


def p_conj(p):
    '''conj : literal CONJ conj
            | literal'''
    if len(p) == 4:
        p[0] = f'CONJ ({p[1]}, {p[3]})'
    else:
        p[0] = p[1]


def p_literal(p):
    '''literal : atom
               | LBRACKET disj RBRACKET'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f'LBRACKET {p[2]} RBRACKET'


def p_atom(p):
    '''atom : ID
            | ID atom1'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + " " + p[2]


def p_atom1(p):
    '''atom1 : atom
             | LBRACKET atom2 RBRACKET
             | LBRACKET atom2 RBRACKET atom1'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = f'LBRACKET {p[2]} RBRACKET'
    else:
        p[0] = f'LBRACKET {p[2]} RBRACKET {p[4]}'


def p_atom2(p):
    '''atom2 : atom
             | LBRACKET atom2 RBRACKET'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f'LBRACKET {p[2]} RBRACKET'


def p_error(p):
    print('Syntax error')


parser = yacc.yacc()

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        file = (open(filename, 'r').read()).split('.')

        if filename.find('.'):
            filename = filename[: filename.find('.')]

        for i in range(len(file)):
            if i == len(file) - 1:
                break
            file[i] += '.'

        fileOUT = open(filename + '.out', 'w')

        for line in file:
            if line == '\n':
                continue
            result = parser.parse(line.strip())
            if result != None:
                fileOUT.write(result + '\n')
            else:
                fileOUT.write('Syntax error\n')

    except OSError:
        print('Can not open', sys.argv[1])
