
def test_pretty_Parallel():
    tf1 = TransferFunction(x + y, x - 2*y, y)
    tf2 = TransferFunction(x - y, x + y, y)
    tf3 = TransferFunction(x**2 + y, y - x, y)
    tf4 = TransferFunction(y**2 - x, x**3 + x, y)

    tfm1 = TransferFunctionMatrix([[tf1, tf2], [tf3, -tf4], [-tf2, -tf1]])
    tfm2 = TransferFunctionMatrix([[-tf2, -tf1], [tf4, -tf3], [tf1, tf2]])
    tfm3 = TransferFunctionMatrix([[-tf1, tf2], [-tf3, tf4], [tf2, tf1]])
    tfm4 = TransferFunctionMatrix([[-tf1, -tf2], [-tf3, -tf4]])

    expected1 = \
"""\
 x + y    x - y\n\
─────── + ─────\n\
x - 2⋅y   x + y\
"""
    expected2 = \
"""\
-x + y   -x - y \n\
────── + ───────
x + y    x - 2⋅y\
"""
    expected3 = \
"""\
 2                                  \n\
x  + y    x + y    ⎛-x - y ⎞ ⎛x - y⎞
────── + ─────── + ⎜───────⎟⋅⎜─────⎟
-x + y   x - 2⋅y   ⎝x - 2⋅y⎠ ⎝x + y⎠\
"""

    expected4 = \
"""\
                            ⎛ 2    ⎞\n\
⎛ x + y ⎞ ⎛x - y⎞   ⎛x - y⎞ ⎜x  + y⎟\n\
⎜───────⎟⋅⎜─────⎟ + ⎜─────⎟⋅⎜──────⎟\n\
⎝x - 2⋅y⎠ ⎝x + y⎠   ⎝x + y⎠ ⎝-x + y⎠\
"""
    expected5 = \
"""\
⎡ x + y   -x + y ⎤    ⎡ x - y    x + y ⎤    ⎡ x + y    x - y ⎤ \n\
⎢───────  ────── ⎥    ⎢ ─────   ───────⎥    ⎢───────   ───── ⎥ \n\
⎢x - 2⋅y  x + y  ⎥    ⎢ x + y   x - 2⋅y⎥    ⎢x - 2⋅y   x + y ⎥ \n\
⎢                ⎥    ⎢                ⎥    ⎢                ⎥ \n\
⎢ 2            2 ⎥    ⎢     2    2     ⎥    ⎢ 2            2 ⎥ \n\
⎢x  + y   x - y  ⎥    ⎢x - y    x  + y ⎥    ⎢x  + y   x - y  ⎥ \n\
⎢──────   ────── ⎥  + ⎢──────   ────── ⎥  + ⎢──────   ────── ⎥ \n\
⎢-x + y    3     ⎥    ⎢ 3       -x + y ⎥    ⎢-x + y    3     ⎥ \n\
⎢         x  + x ⎥    ⎢x  + x          ⎥    ⎢         x  + x ⎥ \n\
⎢                ⎥    ⎢                ⎥    ⎢                ⎥ \n\
⎢-x + y   -x - y ⎥    ⎢-x - y   -x + y ⎥    ⎢-x + y   -x - y ⎥ \n\
⎢──────   ───────⎥    ⎢───────  ────── ⎥    ⎢──────   ───────⎥ \n\
⎣x + y    x - 2⋅y⎦τ   ⎣x - 2⋅y  x + y  ⎦τ   ⎣x + y    x - 2⋅y⎦τ\
"""
    expected6 = \
"""\
⎡ x - y    x + y ⎤                        ⎡-x + y   -x - y  ⎤ \n\
⎢ ─────   ───────⎥                        ⎢──────   ─────── ⎥ \n\
⎢ x + y   x - 2⋅y⎥  ⎡-x - y    -x + y⎤    ⎢x + y    x - 2⋅y ⎥ \n\
⎢                ⎥  ⎢───────   ──────⎥    ⎢                 ⎥ \n\
⎢     2    2     ⎥  ⎢x - 2⋅y   x + y ⎥    ⎢      2     2    ⎥ \n\
⎢x - y    x  + y ⎥  ⎢                ⎥    ⎢-x + y   - x  - y⎥ \n\
⎢──────   ────── ⎥ ⋅⎢   2           2⎥  + ⎢───────  ────────⎥ \n\
⎢ 3       -x + y ⎥  ⎢- x  - y  x - y ⎥    ⎢ 3        -x + y ⎥ \n\
⎢x  + x          ⎥  ⎢────────  ──────⎥    ⎢x  + x           ⎥ \n\
⎢                ⎥  ⎢ -x + y    3    ⎥    ⎢                 ⎥ \n\
⎢-x - y   -x + y ⎥  ⎣          x  + x⎦τ   ⎢ x + y    x - y  ⎥ \n\
⎢───────  ────── ⎥                        ⎢───────   ─────  ⎥ \n\
⎣x - 2⋅y  x + y  ⎦τ                       ⎣x - 2⋅y   x + y  ⎦τ\
"""
    assert upretty(Parallel(tf1, tf2)) == expected1
    assert upretty(Parallel(-tf2, -tf1)) == expected2
    assert upretty(Parallel(tf3, tf1, Series(-tf1, tf2))) == expected3
    assert upretty(Parallel(Series(tf1, tf2), Series(tf2, tf3))) == expected4
    assert upretty(MIMOParallel(-tfm3, -tfm2, tfm1)) == expected5
    assert upretty(MIMOParallel(MIMOSeries(tfm4, -tfm2), tfm2)) == expected6

