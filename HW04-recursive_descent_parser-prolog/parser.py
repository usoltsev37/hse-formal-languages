from lexer import Lex
import sys


class parser:
    def __init__(self, s):
        self.lex = Lex(s)
        self.current = next(self.lex)
        self.data = s

        while self.current:
            ans = self.Def()
            if not ans:
                return

        print("================ OK ================")

    def __print_coloum(self):
        line_start = self.data.rfind('\n', 0, next(self.lex, None).lexpos - 2) + 1
        pos_err = next(self.lex, None).lexpos
        return pos_err - line_start

    def accept(self, c):
        if self.current is None:
            return False

        if self.current.value == c:
            self.current = next(self.lex)
            return True

        return False

    def expect(self, c):
        if self.current is None:
            print("Syntax error", self.current, "\nExpected '", c, "'")
            return False

        if self.current.value == c:
            self.current = next(self.lex)
            return True

        print("Syntax error - line:", self.current.lineno, " - col:", self.__print_coloum(), "\nExpected '", c, "'")
        return False

    def Id(self):
        l = self.current

        if self.accept('('):
            if self.Disj() and self.expect(')'):
                return True
            return False

        if self.current.type != 'ID':
            print("Syntax error - line:", self.current.lineno, "\nExpected literal")
            return False

        self.current = next(self.lex)
        return True

    def Disj(self):
        l = self.Conj()

        if not l:
            return False

        if self.accept(';'):
            r = self.Disj()
            if not r:
                return False

        return True

    def Conj(self):
        l = self.Id()

        if not l:
            return False

        if self.accept(','):
            r = self.Conj()
            if not r:
                return False

        return True

    def Def(self):
        l = self.Id()
        if not l:
            return False

        if self.accept(':-'):
            r = self.Disj()
            if r and self.expect('.'):
                return True
            return False

        if not self.expect('.'):
            return False

        return True


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, 'r') as file:
        parser(file.read())
