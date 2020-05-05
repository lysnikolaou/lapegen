from tokenize import TokenInfo
from typing import Any
from enum import Enum

class ExceptionType:
    OK = 'No Error'
    InvalidOperator = 'An invalid operator was parsed: %(node)s'
    InvalidAtom = 'An invalid atom was parsed: %(node)s'

    def __str__(self):
        return self.value

class PegenException:
    def __init__(
        self,
        token: TokenInfo = None,
        pos: int = -1,
        type: ExceptionType = ExceptionType.OK,
    ):
        self.token: TokenInfo = token
        self.line: int = token.start[0] if token is not None else -1
        self.col: int = token.start[1] if token is not None else -1
        self.pos = pos
        self.type: ExceptionType = type

    def __str__(self):
        if self.token is not None:
            return str(self.type) % dict(node=self.token.string)
        else:
            return str(self.type)
