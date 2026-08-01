
def test_inspect_signature_property():

    # By adding AddX to our signature registry, we can inspect the class
    # itself and objects of the class.  `inspect.signature` doesn't like
    # it when `obj.__signature__` is a property.
    class AddX:
        def __init__(self, func):
            self.func = func

        def __call__(self, addx, *args, **kwargs):
            return addx + self.func(*args, **kwargs)

        @property
        def __signature__(self):
            sig = inspect.signature(self.func)
            params = list(sig.parameters.values())
            kind = inspect.Parameter.POSITIONAL_OR_KEYWORD
            newparam = inspect.Parameter('addx', kind)
            params = [newparam] + params
            return sig.replace(parameters=params)

    addx = AddX(lambda x: x)
    sig = inspect.signature(addx)
    assert sig == inspect.Signature(parameters=[
        inspect.Parameter('addx', inspect.Parameter.POSITIONAL_OR_KEYWORD),
        inspect.Parameter('x', inspect.Parameter.POSITIONAL_OR_KEYWORD)])

    assert num_required_args(AddX) is False
    _sigs.signatures[AddX] = (_sigs.expand_sig((0, lambda func: None)),)
    assert num_required_args(AddX) == 1
    del _sigs.signatures[AddX]

