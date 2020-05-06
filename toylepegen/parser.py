from typing import List

from toylepegen.memo import memoize
from toylepegen.exceptions import PegenException, ExceptionType

class Parser:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.memos = {}
        self.error_stack: List[PegenException] = []

    def mark(self):
        return self.tokenizer.mark()

    def reset(self, pos):
        self.tokenizer.reset(pos)

    def show_rule(self, name, alts):
        # alts is a list of lists of strings
        vis = self.tokenizer.vis
        if vis:
            vis.show_rule(name, alts)

    def show_index(self, alt_index, item_index, num_items=1):
        vis = self.tokenizer.vis
        if vis:
            vis.show_index(alt_index, item_index, num_items)
        return True

    def expect(self, arg):
        token = self.tokenizer.peek_token()
        if token.type == arg or token.string == arg:
            return self.tokenizer.get_token()
        return None

    def loop(self, nonempty, func, *args):
        mark = self.mark()
        nodes = []
        while node := func(*args) is not None:
            nodes.append(node)
        if len(nodes) >= nonempty:
            return nodes
        self.reset(mark)
        return None

    def lookahead(self, positive, func, *args):
        mark = self.mark()
        ok = func(*args) is not None
        self.reset(mark)
        return ok == positive

    def throw(self, exception):
        self.error_stack.append(
            PegenException(
                token=self.tokenizer.tokens[self.tokenizer.pos],
                pos=self.tokenizer.pos,
                type=exception
            )
        )

    def catch(self, exceptions, func, *args):
        mark = self.mark()
        types = [error.type for error in self.error_stack]
        if any(exception in types for exception in exceptions):
            while True:
                if ((error := self.error_stack.pop())
                    and error.type in exceptions
                    and (node := func(*args) is not None)
                ):
                    return node
        self.reset(mark)
        return None
