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
        if p.error.type != ExceptionType.OK:
            last = tok.tokens[-1]
            print(f"Line {p.error.line}:")
            print(p.error.token.line)
            print(" "*p.error.col + "^")
            print(f"SyntaxError: {p.error}")
        sys.exit(1)


main()
