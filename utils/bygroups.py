
def bygroups(*args):
    """
    Callback that yields multiple actions for each group in the match.
    """
    def callback(lexer, match, ctx=None):
        for i, action in enumerate(args):
            if action is None:
                continue
            elif type(action) is _TokenType:
                data = match.group(i + 1)
                if data:
                    yield match.start(i + 1), action, data
            else:
                data = match.group(i + 1)
                if data is not None:
                    if ctx:
                        ctx.pos = match.start(i + 1)
                    for item in action(lexer,
                                       _PseudoMatch(match.start(i + 1), data), ctx):
                        if item:
                            yield item
        if ctx:
            ctx.pos = match.end()
    return callback


def bygroups(*args):
    """
    Callback that yields multiple actions for each group in the match.
    """
    def callback(lexer, match, ctx=None):
        for i, action in enumerate(args):
            if action is None:
                continue
            elif type(action) is _TokenType:
                data = match.group(i + 1)
                if data:
                    yield match.start(i + 1), action, data
            else:
                data = match.group(i + 1)
                if data is not None:
                    if ctx:
                        ctx.pos = match.start(i + 1)
                    for item in action(lexer,
                                       _PseudoMatch(match.start(i + 1), data), ctx):
                        if item:
                            yield item
        if ctx:
            ctx.pos = match.end()
    return callback

