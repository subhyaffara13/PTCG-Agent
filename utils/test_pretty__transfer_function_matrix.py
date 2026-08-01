
def test_pretty_TransferFunctionMatrix():
    tf1 = TransferFunction(x + y, x - 2*y, y)
    tf2 = TransferFunction(x - y, x + y, y)
    tf3 = TransferFunction(y**2 - 2*y + 1, y + 5, y)
    tf4 = TransferFunction(y, x**2 + x + 1, y)
    tf5 = TransferFunction(1 - x, x - y, y)
    tf6 = TransferFunction(2, 2, y)
    expected1 = \
"""\
⎡ x + y ⎤ \n\
⎢───────⎥ \n\
⎢x - 2⋅y⎥ \n\
⎢       ⎥ \n\
⎢ x - y ⎥ \n\
⎢ ───── ⎥ \n\
⎣ x + y ⎦τ\
"""
    expected2 = \
"""\
⎡    x + y     ⎤ \n\
⎢   ───────    ⎥ \n\
⎢   x - 2⋅y    ⎥ \n\
⎢              ⎥ \n\
⎢    x - y     ⎥ \n\
⎢    ─────     ⎥ \n\
⎢    x + y     ⎥ \n\
⎢              ⎥ \n\
⎢   2          ⎥ \n\
⎢- y  + 2⋅y - 1⎥ \n\
⎢──────────────⎥ \n\
⎣    y + 5     ⎦τ\
"""
    expected3 = \
"""\
⎡   x + y        x - y   ⎤ \n\
⎢  ───────       ─────   ⎥ \n\
⎢  x - 2⋅y       x + y   ⎥ \n\
⎢                        ⎥ \n\
⎢ 2                      ⎥ \n\
⎢y  - 2⋅y + 1      y     ⎥ \n\
⎢────────────  ──────────⎥ \n\
⎢   y + 5       2        ⎥ \n\
⎢              x  + x + 1⎥ \n\
⎢                        ⎥ \n\
⎢   1 - x          2     ⎥ \n\
⎢   ─────          ─     ⎥ \n\
⎣   x - y          2     ⎦τ\
"""
    expected4 = \
"""\
⎡    x - y        x + y       y     ⎤ \n\
⎢    ─────       ───────  ──────────⎥ \n\
⎢    x + y       x - 2⋅y   2        ⎥ \n\
⎢                         x  + x + 1⎥ \n\
⎢                                   ⎥ \n\
⎢   2                               ⎥ \n\
⎢- y  + 2⋅y - 1   x - 1      -2     ⎥ \n\
⎢──────────────   ─────      ───    ⎥ \n\
⎣    y + 5        x - y       2     ⎦τ\
"""
    expected5 = \
"""\
⎡ x + y  x - y   x + y       y     ⎤ \n\
⎢───────⋅─────  ───────  ──────────⎥ \n\
⎢x - 2⋅y x + y  x - 2⋅y   2        ⎥ \n\
⎢                        x  + x + 1⎥ \n\
⎢                                  ⎥ \n\
⎢  1 - x   2     x + y      -2     ⎥ \n\
⎢  ───── + ─    ───────     ───    ⎥ \n\
⎣  x - y   2    x - 2⋅y      2     ⎦τ\
"""

    assert upretty(TransferFunctionMatrix([[tf1], [tf2]])) == expected1
    assert upretty(TransferFunctionMatrix([[tf1], [tf2], [-tf3]])) == expected2
    assert upretty(TransferFunctionMatrix([[tf1, tf2], [tf3, tf4], [tf5, tf6]])) == expected3
    assert upretty(TransferFunctionMatrix([[tf2, tf1, tf4], [-tf3, -tf5, -tf6]])) == expected4
    assert upretty(TransferFunctionMatrix([[Series(tf2, tf1), tf1, tf4], [Parallel(tf6, tf5), tf1, -tf6]])) == \
        expected5

