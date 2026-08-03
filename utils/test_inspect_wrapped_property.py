import sys

def test_inspect_wrapped_property():
    class Wrapped:
        def __init__(self, func):
            self.func = func

        def __call__(self, *args, **kwargs):
            return self.func(*args, **kwargs)

        @property
        def __wrapped__(self):
            return self.func

    func = lambda x: x
    wrapped = Wrapped(func)
    assert inspect.signature(func) == inspect.signature(wrapped)

    # inspect.signature did not used to work properly on wrappers,
    # but it was fixed in Python 3.11.9, Python 3.12.3 and Python
    # 3.13+
    inspectbroken = True
    if sys.version_info.major > 3:
        inspectbroken = False
    if sys.version_info.minor == 11 and sys.version_info.micro > 8:
        inspectbroken = False
    if sys.version_info.minor == 12 and sys.version_info.micro > 2:
        inspectbroken = False
    if sys.version_info.minor > 12:
        inspectbroken = False

    if inspectbroken:
        assert num_required_args(Wrapped) is None
        _sigs.signatures[Wrapped] = (_sigs.expand_sig((0, lambda func: None)),)

    assert num_required_args(Wrapped) == 1

