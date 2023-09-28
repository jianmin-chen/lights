TOKEN_TYPE = {
    "Word": "Word",
    "Number": "Number",
    "String": "String",
    "Array": "Array",
    "Func": "Func",
    "Call": "Call",
    "Var": "Var",
    "If": "If",
    "Elif": "Elif",
    "Else": "Else",
    "While": "While",
    "For": "For",
    "True": "True",
    "False": "False",
    "And": "And",
    "Or": "Or",
    "Return": "Return",
    "LeftParen": "LeftParen",
    "RightParen": "RightParen",
    "LeftBrace": "LeftBrace",
    "RightBrace": "RightBrace",
    "LeftBracket": "LeftBracket",
    "RightBracket": "RightBracket",
    "Comma": "Comma",
    "Plus": "Plus",
    "Minus": "Minus",
    "Times": "Times",
    "Divide": "Divide",
    "Modulo": "Modulo",
    "Equal": "Equal",
    "Equality": "Equality",
    "LessThan": "LessThan",
    "LessThanOrEqual": "LessThanOrEqual",
    "GreaterThan": "GreaterThan",
    "GreaterThanOrEqual": "GreaterThanOrEqual",
    "Eof": "Eof",
    "Range": "Range",
    "Colon": "Colon",
    "Period": "Period",
    "Struct": "Struct",
    "Create": "Create",
}

KEYWORDS = {
    "return": TOKEN_TYPE["Return"],
    "var": TOKEN_TYPE["Var"],
    "for": TOKEN_TYPE["For"],
    "through": TOKEN_TYPE["Range"],
    "function": TOKEN_TYPE["Func"],
    "while": TOKEN_TYPE["While"],
    "define": TOKEN_TYPE["Struct"],
    "create": TOKEN_TYPE["Create"],
    "if": TOKEN_TYPE["If"],
    "elif": TOKEN_TYPE["Elif"],
    "True": TOKEN_TYPE["True"],
    "False": TOKEN_TYPE["False"],
    "and": TOKEN_TYPE["And"],
    "or": TOKEN_TYPE["Or"],
}


def new_token(kind, value, content):
    return {"type": kind, "value": value, "content": content}


class Lexer:
    def __init__(self, source="", current=0, tokens=[], line=0):
        self.current = current
        self.source = source
        self.tokens = tokens
        self.line = line

    def peek(self):
        if self.current >= len(self.source):
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def advance(self):
        if self.current >= len(self.source):
            return "\0"
        res = self.peek()
        self.current += 1
        return res

    def match(self, char):
        if self.peek() == char:
            self.advance()
            return True
        return False

    def add_token(self, kind, value, content):
        self.tokens.append(new_token(kind, value, content))


def scan_token(lexer):
    char = lexer.advance()

    def is_alphanumeric(char):
        return char != " " and (char.isalpha() or char.isnumeric() or char == "_")

    def string(kind):
        text = ""
        while lexer.peek() != kind and lexer.peek() != "\0":
            if lexer.peek() == "\n":
                lexer.line += 1
            text += lexer.advance()
        if lexer.peek() == "\0":
            # Reached end of file, but string hasn't been terminated
            raise Exception(f"Unterminated string: {lexer.line}")
        lexer.advance()  # Consume the closing quote
        lexer.add_token(TOKEN_TYPE["String"], text, text)

    def number():
        text = ""
        while lexer.peek().isnumeric():
            text += lexer.advance()
        if lexer.peek() == "." and lexer.peek_next().isnumeric():
            text += lexer.advance()
            while lexer.peek().isnumeric():
                text += lexer.advance()
        lexer.add_token(TOKEN_TYPE["Number"], float(text), text)

    def identifier():
        text = ""
        while is_alphanumeric(lexer.peek()):
            text += lexer.advance()
        kind = KEYWORDS.get(text, None)
        if kind is None:
            kind = TOKEN_TYPE["Word"]
        lexer.add_token(kind, text, text)

    if char == "(":
        lexer.add_token(TOKEN_TYPE["LeftParen"], "(", "(")
    elif char == ")":
        lexer.add_token(TOKEN_TYPE["RightParen"], ")", ")")
    elif char == "{":
        lexer.add_token(TOKEN_TYPE["LeftBrace"], "{", "{")
    elif char == "}":
        lexer.add_token(TOKEN_TYPE["RightBrace"], "}", "}")
    elif char == "[":
        lexer.add_token(TOKEN_TYPE["LeftBracket"], "[", "[")
    elif char == "]":
        lexer.add_token(TOKEN_TYPE["RightBracket"], "]", "]")
    elif char == ",":
        lexer.add_token(TOKEN_TYPE["Comma"], ",", ",")
    elif char == "+":
        lexer.add_token(TOKEN_TYPE["Plus"], "+", "+")
    elif char == "-":
        lexer.add_token(TOKEN_TYPE["Minus"], "-", "-")
    elif char == "*":
        lexer.add_token(TOKEN_TYPE["Times"], "*", "*")
    elif char == "/":
        lexer.add_token(TOKEN_TYPE["Divide"], "/", "/")
    elif char == "%":
        lexer.add_token(TOKEN_TYPE["Modulo"], "%", "%")
    elif char == "=":
        if lexer.peek() == "=":
            lexer.advance()
            lexer.add_token(TOKEN_TYPE["Equality"], "==", "==")
        else:
            lexer.add_token(TOKEN_TYPE["Equal"], "=", "=")
    elif char == '"':
        string('"')
    elif char == "'":
        string("'")
    elif char == "<":
        if lexer.peek() == "=":
            lexer.advance()
            lexer.add_token(TOKEN_TYPE["LessThanOrEqual"], "<=", "<=")
        else:
            lexer.add_token(TOKEN_TYPE["LessThan"], "<", "<")
    elif char == ">":
        if lexer.peek() == "=":
            lexer.advance()
            lexer.add_token(TOKEN_TYPE["GreaterThanOrEqual"], ">=")
        else:
            lexer.add_token(TOKEN_TYPE["GreaterThan"], ">", ">")
    elif char == ":":
        lexer.add_token(TOKEN_TYPE["Colon"], ":", ":")
    elif char == ".":
        lexer.add_token(TOKEN_TYPE["Period"], ".", ".")
    elif char == "#":
        while lexer.peek() != "\n" and lexer.peek() != "\0":
            lexer.advance()
        lexer.line += 1
    elif char == "\n":
        lexer.line += 1
    elif char == " ":
        return
    elif char == "\t":
        return
    else:
        if char.isalpha():
            lexer.current -= 1
            identifier()
        elif char.isnumeric():
            lexer.current -= 1
            number()
        else:
            raise Exception(f"Unexpected character: {char} at line {lexer.line + 1}")


def scan_tokens(lexer):
    while lexer.current < len(lexer.source):
        scan_token(lexer)
    lexer.add_token(TOKEN_TYPE["Eof"], "", "")
    return lexer.tokens
