#! usr/bin/env python3

import argparse
import os
import sys
from tokenize import generate_tokens

sys.path.insert(0, os.getcwd())
from toylepegen.calc import CalcParser
from toylepegen.tokenizer import Tokenizer
from toylepegen.exceptions import ExceptionType


argparser = argparse.ArgumentParser()
argparser.add_argument("program", nargs="?", default="toylepegen/calc.txt", help="Sample program (in.txt)")
argparser.add_argument("-s", "--start", default="start", help="Start symbol (start)")


def main():
    args = argparser.parse_args()
    filename = args.program
    startname = args.start

    tree = None
    with open(filename) as f:
        tokengen = generate_tokens(f.readline)
        tok = Tokenizer(tokengen)
        p = CalcParser(tok)
        start = getattr(p, startname)
        tree = start()

    if tree:
        print(tree)
    else:
        if p.error_stack:
            print(f"Numer of errors: {len(p.error_stack)}")
            error = p.error_stack[0]
            print(f"Line {error.line}:")
            print(error.token.line)
            print(" "*error.col + "^")
            print(f"SyntaxError: {error}")
        else:
            print("SyntaxError: invalid syntax")
        sys.exit(1)


main()
