
def make_lazy_class(cls):

    def lazy_init(self, cb):
        self._cb = cb
        self._value = None

    cls.__init__ = lazy_init

    for basename in [
        "add", "sub", "mul", "truediv", "floordiv", "mod", "divmod", "pow",
        "lshift", "rshift", "and", "or", "xor", "neg", "pos", "abs", "invert",
        "eq", "ne", "lt", "le", "gt", "ge", "bool", "int", "index",
    ]:
        name = f"__{basename}__"

        def inner_wrapper(name):
            use_operator = basename not in ("bool", "int")

            def wrapped(self, *args, **kwargs):
                if self._cb is not None:
                    self._value = self._cb()
                    self._cb = None
                if not use_operator:
                    return getattr(self._value, name)(*args, **kwargs)
                else:
                    return getattr(operator, name)(self._value, *args, **kwargs)
            return wrapped

        setattr(cls, name, inner_wrapper(name))

    return cls

