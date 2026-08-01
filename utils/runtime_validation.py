
def runtime_validation(f):
    # TODO:
    # Can be extended to validate '__getitem__' and nonblocking
    if f.__name__ != "__iter__":
        raise TypeError(
            f"Can not decorate function {f.__name__} with 'runtime_validation'"
        )

    @wraps(f)
    def wrapper(self):
        global _runtime_validation_enabled
        if not _runtime_validation_enabled:
            yield from f(self)
        else:
            it = f(self)
            for d in it:
                if not self.type.issubtype_of_instance(d):
                    raise RuntimeError(
                        f"Expected an instance as subtype of {self.type}, but found {d}({type(d)})"
                    )
                yield d

    return wrapper

