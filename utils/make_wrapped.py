import functools

def make_wrapped(fn, ctxs):
    @functools.wraps(fn)
    def wrapped(self):
        torch._dynamo.reset()
        stack = contextlib.ExitStack()
        for ctx in ctxs:
            if callable(ctx):
                stack.enter_context(ctx(self))
            else:
                stack.enter_context(ctx)
        try:
            out = fn(self)
        finally:
            stack.close()
        return out

    return wrapped

