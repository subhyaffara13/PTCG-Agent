
def test_lambdify_docstring():
    func = lambdify((w, x, y, z), w + x + y + z)
    ref = (
        "Created with lambdify. Signature:\n\n"
        "func(w, x, y, z)\n\n"
        "Expression:\n\n"
        "w + x + y + z"
    ).splitlines()
    assert func.__doc__.splitlines()[:len(ref)] == ref
    syms = symbols('a1:26')
    func = lambdify(syms, sum(syms))
    ref = (
        "Created with lambdify. Signature:\n\n"
        "func(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15,\n"
        "        a16, a17, a18, a19, a20, a21, a22, a23, a24, a25)\n\n"
        "Expression:\n\n"
        "a1 + a10 + a11 + a12 + a13 + a14 + a15 + a16 + a17 + a18 + a19 + a2 + a20 +..."
    ).splitlines()
    assert func.__doc__.splitlines()[:len(ref)] == ref

