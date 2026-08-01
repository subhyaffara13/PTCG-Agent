
def test_ManagedProperties():
    # ManagedProperties is now deprecated. Here we do our best to check that if
    # someone is using it then it does work in the way that it previously did
    # but gives a deprecation warning.
    from sympy.core.assumptions import ManagedProperties

    myclasses = []

    class MyMeta(ManagedProperties):
        def __init__(cls, *args, **kwargs):
            myclasses.append('executed')
            super().__init__(*args, **kwargs)

    code = """
class MySubclass(Basic, metaclass=MyMeta):
    pass
"""
    with warns_deprecated_sympy():
        exec(code)

    assert myclasses == ['executed']

