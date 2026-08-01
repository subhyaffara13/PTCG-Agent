
def test_PrettyModules():
    R = QQ.old_poly_ring(x, y)
    F = R.free_module(2)
    M = F.submodule([x, y], [1, x**2])

    ucode_str = \
"""\
       2\n\
ℚ[x, y] \
"""
    ascii_str = \
"""\
        2\n\
QQ[x, y] \
"""

    assert upretty(F) == ucode_str
    assert pretty(F) == ascii_str

    ucode_str = \
"""\
╱        ⎡    2⎤╲\n\
╲[x, y], ⎣1, x ⎦╱\
"""
    ascii_str = \
"""\
              2  \n\
<[x, y], [1, x ]>\
"""

    assert upretty(M) == ucode_str
    assert pretty(M) == ascii_str

    I = R.ideal(x**2, y)

    ucode_str = \
"""\
╱ 2   ╲\n\
╲x , y╱\
"""

    ascii_str = \
"""\
  2    \n\
<x , y>\
"""

    assert upretty(I) == ucode_str
    assert pretty(I) == ascii_str

    Q = F / M

    ucode_str = \
"""\
           2     \n\
    ℚ[x, y]      \n\
─────────────────\n\
╱        ⎡    2⎤╲\n\
╲[x, y], ⎣1, x ⎦╱\
"""

    ascii_str = \
"""\
            2    \n\
    QQ[x, y]     \n\
-----------------\n\
              2  \n\
<[x, y], [1, x ]>\
"""

    assert upretty(Q) == ucode_str
    assert pretty(Q) == ascii_str

    ucode_str = \
"""\
╱⎡    3⎤                                                ╲\n\
│⎢   x ⎥   ╱        ⎡    2⎤╲           ╱        ⎡    2⎤╲│\n\
│⎢1, ──⎥ + ╲[x, y], ⎣1, x ⎦╱, [2, y] + ╲[x, y], ⎣1, x ⎦╱│\n\
╲⎣   2 ⎦                                                ╱\
"""

    ascii_str = \
"""\
      3                                                  \n\
     x                   2                           2   \n\
<[1, --] + <[x, y], [1, x ]>, [2, y] + <[x, y], [1, x ]>>\n\
     2                                                   \
"""

