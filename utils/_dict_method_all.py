import functools

def _dict_method_all(dict_method: F) -> F:
    @functools.wraps(dict_method)
    def f_all(self: "Context") -> t.Any:
        return dict_method(self.get_all())

    return t.cast(F, f_all)

