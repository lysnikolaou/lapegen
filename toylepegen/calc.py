# This is @generated code; do not edit!

from token import ENDMARKER, NAME, NEWLINE, NUMBER, STRING

from toylepegen.memo import memoize, memoize_left_rec
from toylepegen.node import Node
from toylepegen.parser import Parser
from toylepegen.exceptions import ExceptionType, PegenException

from ast import literal_eval

class CalcParser(Parser):

    def start(self):
        pos = self.mark()
        if (True
            and (expr_stmt := self.loop(False, self.expr_stmt)) is not None
            and (endmarker := self.expect(ENDMARKER)) is not None
        ):
            return Node('start', [expr_stmt, endmarker])
        self.reset(pos)
        return None

    def expr_stmt(self):
        pos = self.mark()
        if (True
            and (expr := self.expr()) is not None
            and (newline := self.expect(NEWLINE)) is not None
        ):
            retval = expr
            if retval is not None:
                return retval
        self.reset(pos)
        return None

    @memoize_left_rec
    def expr(self):
        pos = self.mark()
        cut = False
        if (True
            and (expr := self.expr()) is not None
            and self.expect('+') is not None
            and (term := self.term()) is not None
        ):
            retval = expr + term
            if retval is not None:
                return retval
        self.reset(pos)
        if cut:
            return None
        if (True
            and (expr := self.expr()) is not None
            and self.expect('-') is not None
            and (term := self.term()) is not None
        ):
            retval = expr - term
            if retval is not None:
                return retval
        self.reset(pos)
        if cut:
            return None
        if (True
            and (term := self.term()) is not None
        ):
            retval = term
            if retval is not None:
                return retval
        self.reset(pos)
        return None

    @memoize_left_rec
    def term(self):
        pos = self.mark()
        cut = False
        if (True
            and self.expect('-') is not None
            and (term := self.term()) is not None
        ):
            retval = - term
            if retval is not None:
                return retval
        self.reset(pos)
        if cut:
            return None
        if (True
            and self.expect('+') is not None
            and (term := self.term()) is not None
        ):
            retval = + term
            if retval is not None:
                return retval
        self.reset(pos)
        if cut:
            return None
        if (True
            and (term := self.term()) is not None
            and self.expect('*') is not None
            and (factor := self.factor()) is not None
        ):
            retval = term * factor
            if retval is not None:
                return retval
        self.reset(pos)
        if cut:
            return None
        if (True
            and (term := self.term()) is not None
            and self.expect('/') is not None
            and (factor := self.factor()) is not None
        ):
            retval = term / factor
            if retval is not None:
                return retval
        self.reset(pos)
        if cut:
            return None
        if (True
            and (term := self.term()) is not None
            and self.expect('//') is not None
            and (factor := self.factor()) is not None
        ):
            retval = term // factor
            if retval is not None:
                return retval
        self.reset(pos)
        if cut:
            return None
        if (True
            and (factor := self.factor()) is not None
        ):
            retval = factor
            if retval is not None:
                return retval
        self.reset(pos)
        return None

    def factor(self):
        pos = self.mark()
        cut = False
        if (True
            and (atom := self.atom()) is not None
            and self.factor_operator() is not None
            and (factor := self.factor()) is not None
        ):
            retval = atom ** factor
            if retval is not None:
                return retval
        self.reset(pos)
        if cut:
            return None
        if (True
            and (atom := self.catch_exceptions(ExceptionType.InvalidOperator, self.atom)) is not None
        ):
            retval = atom
            if retval is not None:
                return retval
        self.reset(pos)
        return None

    def factor_operator(self):
        pos = self.mark()
        if (True
            and self.expect('**')
        ):
            return '**'
        self.reset(pos)
        if (True):
            self.raise_exception(ExceptionType.InvalidOperator)
            return None
        self.reset(pos)
        return None

    def atom(self):
        pos = self.mark()
        cut = False
        if (True
            and (string := self.expect(STRING)) is not None
        ):
            retval = literal_eval ( string . string )
            if retval is not None:
                return retval
        self.reset(pos)
        if (True
            and (number := self.expect(NUMBER)) is not None
        ):
            retval = literal_eval ( number . string )
            if retval is not None:
                return retval
        self.reset(pos)
        if (True
            and self.expect('(') is not None
            and (expr := self.expr()) is not None
            and self.expect(')') is not None
        ):
            retval = expr
            if retval is not None:
                return retval
        self.reset(pos)
        if (True):
            self.raise_exception(ExceptionType.InvalidAtom)
            return None
        self.reset(pos)
        if cut:
            return None
        return None
