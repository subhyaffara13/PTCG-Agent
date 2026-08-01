
def test_Homomorphism():
    from sympy.polys.agca import homomorphism

    R = QQ.old_poly_ring(x)

    expr = homomorphism(R.free_module(1), R.free_module(1), [0])

    ucode_str = \
"""\
          1         1\n\
[0] : ℚ[x]  ──> ℚ[x] \
"""

    ascii_str = \
"""\
           1          1\n\
[0] : QQ[x]  --> QQ[x] \
"""

    assert upretty(expr) == ucode_str
    assert pretty(expr) == ascii_str

    expr = homomorphism(R.free_module(2), R.free_module(2), [0, 0])

    ucode_str = \
"""\
⎡0  0⎤       2         2\n\
⎢    ⎥ : ℚ[x]  ──> ℚ[x] \n\
⎣0  0⎦                  \
"""

    ascii_str = \
"""\
[0  0]        2          2\n\
[    ] : QQ[x]  --> QQ[x] \n\
[0  0]                    \
"""

    assert upretty(expr) == ucode_str
    assert pretty(expr) == ascii_str

    expr = homomorphism(R.free_module(1), R.free_module(1) / [[x]], [0])

    ucode_str = \
"""\
                    1\n\
          1     ℚ[x] \n\
[0] : ℚ[x]  ──> ─────\n\
                <[x]>\
"""

    ascii_str = \
"""\
                      1\n\
           1     QQ[x] \n\
[0] : QQ[x]  --> ------\n\
                 <[x]> \
"""

    assert upretty(expr) == ucode_str
    assert pretty(expr) == ascii_str

