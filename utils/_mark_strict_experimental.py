
def _mark_strict_experimental(cls):
    def call(self, *args):
        return strict_mode(self, args)

    cls.__call__ = call
    return cls

