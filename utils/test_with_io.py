
def testWithIO(inp, out, f):
    """Calls the function `f` with ``sys.stdin`` changed to `inp`
    and ``sys.stdout`` changed to `out`.  They are restored when `f`
    returns.  This function returns whatever `f` returns.
    """

    import os

    try:
        oldin, sys.stdin = sys.stdin, inp
        oldout, sys.stdout = sys.stdout, out
        x = f()
    finally:
        sys.stdin = oldin
        sys.stdout = oldout
    if os.environ.get("PYPNG_TEST_TMP") and hasattr(out, "getvalue"):
        name = mycallersname()
        if name:
            w = open(name + ".png", "wb")
            w.write(out.getvalue())
            w.close()
    return x

