from flask import Flask, render_template, request
from lightlexer import Lexer, scan_tokens
from lightparser import Parser, program
from lighteval import run
from json import dumps, loads

DEBUG = True

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ast", methods=["GET"])
def ast():
    with open("parser.out", "r") as f:
        return loads(f.read())


@app.route("/flash", methods=["POST"])
def flash():
    data = request.form
    if data.get("code"):
        try:
            # Code was provided, so run it
            source = data.get("code")
            lexer = Lexer(source)
            scan_tokens(lexer)
            if DEBUG:
                with open("lexer.out", "w") as f:
                    f.write(dumps(lexer.tokens, indent=4))
            parser = Parser(lexer.tokens)
            ast = program(parser)
            if DEBUG:
                with open("ast.out", "w") as f:
                    f.write(dumps(ast, indent=4))
            # Now that we have the AST, write to where CircuitPython reads
            return {"success": True, "ast": ast}
        except Exception as e:
            return {"success": False, "reason": str(e)}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
