############################  childSoft ##############################


SYİ, TPLM, CKRM, CRPM, BLM, EOF = (
    'SYİ', 'TPLM', 'CKRM', 'CRPM', 'BLM', 'EOF'
)


class Simge(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Simge({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.mevcutKarakter = self.text[self.pos]

    def hata(self):
        raise Exception('Geçersiz karakter.')

    def ilerle(self):

        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.mevcutKarakter = None 
        else:
            self.mevcutKarakter = self.text[self.pos]

    def bosluklari_atla(self):
        while self.mevcutKarakter is not None and self.mevcutKarakter.isspace():
            self.advance()

    def syi(self):

        result = ''
        while self.mevcutKarakter is not None and self.mevcutKarakter.isdigit():
            result += self.mevcutKarakter
            self.advance()
        return int(result)

    def siradaki_simgeye_gec(self):
        while self.mevcutKarakter is not None:

            if self.mevcutKarakter.isspace():
                self.bosluklari_atla()
                continue

            if self.mevcutKarakter.isdigit():
                return Simge(SYİ, self.syi())

            if self.mevcutKarakter == '+':
                self.ilerle()
                return Simge(TPLM, '+')

            if self.mevcutKarakter == '-':
                self.ilerle()
                return Simge(CKRM, '-')

            if self.mevcutKarakter == '*':
                self.ilerle()
                return Simge(CRPM, '*')

            if self.mevcutKarakter == '/':
                self.ilerle()
                return Simge(BLM, '/')

            self.hata()

        return Simge(EOF, None)


class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer

        self.mevcutKarakter = self.lexer.siradaki_simgeye_gec()

    def hata(self):
        raise Exception('Geçersiz Sözdizimi')

    def eat(self, simge_type):

        if self.mevcutKarakter.type == simge_type:
            self.mevcutKarakter = self.lexer.siradaki_simgeye_gec()
        else:
            self.hata()

    def faktor(self):
    
        simge = self.mevcutKarakter
        self.eat(SYİ)
        return simge.value

    def terim(self):

        result = self.factor()

        while self.mevcutKarakter.type in (CRPM, DIV):
            simge = self.mevcutKarakter
            if simge.type == CRPM:
                self.eat(CRPM)
                result = result * self.faktor()
            elif simge.type == BLM:
                self.eat(BLM)
                result = result / self.faktor()

        return result

    def expr(self):

        result = self.terim()

        while self.mevcutKarakter.type in (TPLM, CKRM):
            simge = self.mevcutKarakter
            if simge.type == TPLM:
                self.eat(TPLM)
                result = result + self.terim()
            elif simge.type == CKRM:
                self.eat(CKRM)
                result = result - self.terim()

        return result


def main():
    while True:
        try:

            text =input('hspl> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
