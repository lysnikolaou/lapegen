from toylepegen.memo import memoize
from toylepegen.exceptions import PegenException, ExceptionType

class Parser:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.memos = {}
        self.error = PegenException()

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

    def raise_exception(self, exception):
        if self.error.type != ExceptionType.OK:
            return # Only raise, if no exception is set
        self.error = PegenException(
            token=self.tokenizer.tokens[self.tokenizer.pos],
            type=exception
        )

    def catch_exceptions(self, exceptions, func, *args):
        mark = self.mark()
        if self.error.type in exceptions:
            if node := func(*args) is not None:
                self.error = PegenException() # Clear error
                return node
        self.reset(mark)
        return None
