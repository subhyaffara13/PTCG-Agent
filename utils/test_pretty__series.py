
def test_pretty_Series():
    tf1 = TransferFunction(x + y, x - 2*y, y)
    tf2 = TransferFunction(x - y, x + y, y)
    tf3 = TransferFunction(x**2 + y, y - x, y)
    tf4 = TransferFunction(2, 3, y)

    tfm1 = TransferFunctionMatrix([[tf1, tf2], [tf3, tf4]])
    tfm2 = TransferFunctionMatrix([[tf3], [-tf4]])
    tfm3 = TransferFunctionMatrix([[tf1, -tf2, -tf3], [tf3, -tf4, tf2]])
    tfm4 = TransferFunctionMatrix([[tf1, tf2], [tf3, -tf4], [-tf2, -tf1]])
    tfm5 = TransferFunctionMatrix([[-tf2, -tf1], [tf4, -tf3], [tf1, tf2]])

    expected1 = \
"""\
          ⎛ 2    ⎞\n\
⎛ x + y ⎞ ⎜x  + y⎟\n\
⎜───────⎟⋅⎜──────⎟\n\
⎝x - 2⋅y⎠ ⎝-x + y⎠\
"""
    expected2 = \
"""\
⎛-x + y⎞ ⎛-x - y ⎞\n\
⎜──────⎟⋅⎜───────⎟\n\
⎝x + y ⎠ ⎝x - 2⋅y⎠\
"""
    expected3 = \
"""\
⎛ 2    ⎞                            \n\
⎜x  + y⎟ ⎛ x + y ⎞ ⎛-x - y    x - y⎞\n\
⎜──────⎟⋅⎜───────⎟⋅⎜─────── + ─────⎟\n\
⎝-x + y⎠ ⎝x - 2⋅y⎠ ⎝x - 2⋅y   x + y⎠\
"""
    expected4 = \
"""\
                  ⎛         2    ⎞\n\
⎛ x + y    x - y⎞ ⎜x - y   x  + y⎟\n\
⎜─────── + ─────⎟⋅⎜───── + ──────⎟\n\
⎝x - 2⋅y   x + y⎠ ⎝x + y   -x + y⎠\
"""
    expected5 = \
"""\
⎡ x + y   x - y⎤  ⎡ 2    ⎤ \n\
⎢───────  ─────⎥  ⎢x  + y⎥ \n\
⎢x - 2⋅y  x + y⎥  ⎢──────⎥ \n\
⎢              ⎥  ⎢-x + y⎥ \n\
⎢ 2            ⎥ ⋅⎢      ⎥ \n\
⎢x  + y     2  ⎥  ⎢ -2   ⎥ \n\
⎢──────     ─  ⎥  ⎢ ───  ⎥ \n\
⎣-x + y     3  ⎦τ ⎣  3   ⎦τ\
"""
    expected6 = \
"""\
                                               ⎛⎡ x + y    x - y ⎤    ⎡ x - y    x + y ⎤ ⎞\n\
                                               ⎜⎢───────   ───── ⎥    ⎢ ─────   ───────⎥ ⎟\n\
⎡ x + y   x - y⎤  ⎡                    2    ⎤  ⎜⎢x - 2⋅y   x + y ⎥    ⎢ x + y   x - 2⋅y⎥ ⎟\n\
⎢───────  ─────⎥  ⎢ x + y   -x + y  - x  - y⎥  ⎜⎢                ⎥    ⎢                ⎥ ⎟\n\
⎢x - 2⋅y  x + y⎥  ⎢───────  ──────  ────────⎥  ⎜⎢ 2              ⎥    ⎢          2     ⎥ ⎟\n\
⎢              ⎥  ⎢x - 2⋅y  x + y    -x + y ⎥  ⎜⎢x  + y     -2   ⎥    ⎢  -2     x  + y ⎥ ⎟\n\
⎢ 2            ⎥ ⋅⎢                         ⎥ ⋅⎜⎢──────     ───  ⎥  + ⎢  ───    ────── ⎥ ⎟\n\
⎢x  + y     2  ⎥  ⎢ 2                       ⎥  ⎜⎢-x + y      3   ⎥    ⎢   3     -x + y ⎥ ⎟\n\
⎢──────     ─  ⎥  ⎢x  + y    -2      x - y  ⎥  ⎜⎢                ⎥    ⎢                ⎥ ⎟\n\
⎣-x + y     3  ⎦τ ⎢──────    ───     ─────  ⎥  ⎜⎢-x + y   -x - y ⎥    ⎢-x - y   -x + y ⎥ ⎟\n\
                  ⎣-x + y     3      x + y  ⎦τ ⎜⎢──────   ───────⎥    ⎢───────  ────── ⎥ ⎟\n\
                                               ⎝⎣x + y    x - 2⋅y⎦τ   ⎣x - 2⋅y  x + y  ⎦τ⎠\
"""

    assert upretty(Series(tf1, tf3)) == expected1
    assert upretty(Series(-tf2, -tf1)) == expected2
    assert upretty(Series(tf3, tf1, Parallel(-tf1, tf2))) == expected3
    assert upretty(Series(Parallel(tf1, tf2), Parallel(tf2, tf3))) == expected4
    assert upretty(MIMOSeries(tfm2, tfm1)) == expected5
    assert upretty(MIMOSeries(MIMOParallel(tfm4, -tfm5), tfm3, tfm1)) == expected6

