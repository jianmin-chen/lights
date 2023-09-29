from flask import Flask, render_template, request
from lightlexer import Lexer, scan_tokens
from lightparser import Parser, program
from lighteval import run
from json import dumps

DEBUG = True

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/flash", methods=["POST"])
def flash():
    data = request.form
    if data.get("code"):
        # Code was provided, so run it
        source = data.get("code")
        lexer = Lexer(source)
        scan_tokens(lexer)
        if DEBUG:
            with open("lexer.out", "w") as f:
                f.write(dumps(lexer.tokens, indent=4))
        parser = Parser(lexer.tokens)
        ast = program(parser)
        # Now that we have the AST, what do we do now?
        print(ast)
        return ast


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
