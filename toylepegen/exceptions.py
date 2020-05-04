from tokenize import TokenInfo
from typing import Any
from enum import Enum

class ExceptionType:
    OK = 'No Error'
    InvalidAtom = 'An invalid atom was parsed: %(node)s'
    InvalidOperator = 'An invalid operator was parsed: %(node)s'
    NoNewline = 'Expected NEWLINE, parsed %(node)s instead'

    def __str__(self):
        return self.value

class PegenException:
    def __init__(self, token: TokenInfo = None, type: ExceptionType = ExceptionType.OK):
        self.token: TokenInfo = token
        self.line: int = token.start[0] if token is not None else -1
        self.col: int = token.start[1] if token is not None else -1
        self.type: ExceptionType = type

    def __str__(self):
        return str(self.type) % dict(node=self.token.string)
