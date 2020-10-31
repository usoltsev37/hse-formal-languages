from parsita import *
import sys


class PrologParser(TextParsers, whitespace='[ \t\n]*'):
    MODULE = lit('module') > (lambda x: 'Module')
    TYPE = lit('type') > (lambda x: 'Type')
    ID = reg(r'[a-z][A-Za-z_0-9]*')
    VAR = reg(r'[A-Z][A-Za-z_0-9]*') > (lambda x: f'(Var {x})')
    DISJ = lit(';') > (lambda x: '+')
    CONJ = lit(',') > (lambda x: '*')
    LBR = lit('(')
    RBR = lit(')')
    LBR_LIST = lit('[')
    RBR_LIST = lit(']')
    SEP_LIST = lit('|')
    SPIN = lit(':-')
    POINT = lit('.')
    ARROW = lit('->')

    id = pred(ID, lambda x: x != 'module' and x != 'type',
              '\n======\nERROR: Key words can\'t be an Identifier\n======\n') \
         > (lambda x: f'(Id {x})')

    out_prog = lambda x: sum(x, [])
    out_module = lambda x: f'({x[0]} {x[1]})'
    out_ref = lambda x: f'(Def {x[0]})' if type(x[0]) == str else f'(Def {x[0][0]}{x[0][2]})'
    out_disj = lambda x: f'(Disj {x[0]}{x[2]})' if len(x) == 3 else f'{x}'
    out_conj = lambda x: f'(Conj {x[0]}{x[2]})' if len(x) == 3 else f'{x}'
    out_literal = lambda x: f'{x}' if type(x) is str else '(' + ''.join(str(el) for el in x) + ')'
    out_atom = lambda x: f'(Atom {x})' if type(x) is str else '(Atom ' + x[0] + ''.join(
        str(el) for el in x[1]) + ')'

    program = (opt(moduleRes) & typeRes & expr) > out_prog

    moduleRes = (MODULE & id & POINT) > out_module
    expr = rep(rel)
    rel = (((atom & SPIN & disj) | atom) & POINT) > out_ref
    disj = ((conj & DISJ & disj) | conj) > out_disj
    conj = ((literal & CONJ & conj) | literal) > out_conj
    literal = ((LBR >> disj << RBR) | atom) > out_literal
    atom = (id & rep((id | VAR | subatom | listElem))) > out_atom
    subatom = ((LBR >> id << RBR) > (lambda x: f'(Atom {x})')) | ((LBR >> atom << RBR) > (lambda x: f'({x})')) | (
                LBR >> subatom << RBR) | atom

    format_console_keys = (lambda x: [x])
    atom_cosole = atom > format_console_keys
    subtype_cosole = subtype > format_console_keys
    rel_cosole = rel > format_console_keys
    module = moduleRes > format_console_keys

    out_typeExpr = lambda x: '(' + x[0] + ' ' + ' '.join(x[1:]) + ')'
    out_subtype1 = lambda x: f'{x}' if type(x) == str else f'(Arrow ' + x[0] + x[2] + ')'
    out_subtype3 = lambda x: f'(Arrow {" ".join(x)})'
    typeRes = rep(typeExpr)
    typeExpr = (TYPE & id & subtype1 << POINT) > out_typeExpr
    subtype1 = ((subtype2 & ARROW & subtype1) | subtype2) > out_subtype1
    subtype2 = (LBR >> subtype2 << RBR) | ((LBR >> subtype3 << RBR) > out_subtype3) | (atom | VAR | id)
    subtype3 = rep1sep(subtype2, ARROW)

    out_list = lambda x: f'(List {x[0]})' if len(x) == 1 \
        else f'(List {"".join(x[0])}{x[2]})' if x[1] == '|' else '(List ' + ''.join(x) + ')'

    list = ((LBR_LIST >> rep1sep((atom | VAR | listElem), ',') & SEP_LIST & VAR << RBR_LIST)
            | (LBR_LIST >> repsep((atom | VAR | listElem), ',') << RBR_LIST)) > out_list
    empty_list = lit('[]') > (lambda x: f'(List {x})')
    listElem = empty_list | list
    list_cosole = rep(empty_list | list)


def main():
    switcher = {'--atom': PrologParser.atom_cosole.parse,
                '--typeexpr': PrologParser.subtype_cosole.parse,
                '--type': PrologParser.typeRes.parse,
                '--module': PrologParser.module.parse,
                '--relation': PrologParser.rel_cosole.parse,
                '--list': PrologParser.list_cosole.parse,
                '--prog': PrologParser.program.parse}

    filename = 'filename'
    key = 'key'

    if sys.argv[1][0:2] != '--':
        filename = sys.argv[1]
        key = '--prog'
    else:
        filename = sys.argv[2]
        key = sys.argv[1]

    sys.stdout = open(filename + '.out', 'w')

    with open(filename, 'r') as data:
        result = switcher[key](data.read())
        if result == Success:
            for el in result.value:
                print(el)
        else:
            print('Syntax Error')


if __name__ == "__main__":
    main()
