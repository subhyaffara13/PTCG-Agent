from typing import Any

def assert_blobs_same(x: Any, y: Any, trail: tuple[Any, ...]) -> None:
    """Compare two blobs of IR as best we can.

    FuncDecls, FuncIRs, and ClassIRs are compared by fullname to avoid
    infinite recursion.
    (More detailed comparisons should be done manually.)

    Types and signatures are compared using mypyc.sametype.

    Containers are compared recursively.

    Anything else is compared with ==.

    The `trail` argument is used in error messages.
    """

    assert type(x) is type(y), (f"Type mismatch at {trail}", type(x), type(y))
    if isinstance(x, (FuncDecl, FuncIR, ClassIR)):
        assert x.fullname == y.fullname, f"Name mismatch at {trail}"
    elif isinstance(x, dict):
        assert len(x.keys()) == len(y.keys()), f"Keys mismatch at {trail}"
        for (xk, xv), (yk, yv) in zip(x.items(), y.items()):
            assert_blobs_same(xk, yk, trail + ("keys",))
            assert_blobs_same(xv, yv, trail + (xk,))
    elif isinstance(x, Iterable) and not isinstance(x, (str, set)):
        # Special case iterables to generate better assert error messages.
        # We can't use this for sets since the ordering is unpredictable,
        # and strings should be treated as atomic values.
        for i, (xv, yv) in enumerate(zip(x, y)):
            assert_blobs_same(xv, yv, trail + (i,))
    elif isinstance(x, RType):
        assert is_same_type(x, y), f"RType mismatch at {trail}"
    elif isinstance(x, FuncSignature):
        assert is_same_signature(x, y), f"Signature mismatch at {trail}"
    else:
        assert x == y, f"Value mismatch at {trail}"

