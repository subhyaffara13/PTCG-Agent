
def test_pretty_MIMOFeedback():
    tf1 = TransferFunction(x + y, x - 2*y, y)
    tf2 = TransferFunction(x - y, x + y, y)
    tfm_1 = TransferFunctionMatrix([[tf1, tf2], [tf2, tf1]])
    tfm_2 = TransferFunctionMatrix([[tf2, tf1], [tf1, tf2]])
    tfm_3 = TransferFunctionMatrix([[tf1, tf1], [tf2, tf2]])

    expected1 = \
"""\
⎛    ⎡ x + y    x - y ⎤  ⎡ x - y    x + y ⎤ ⎞-1   ⎡ x + y    x - y ⎤ \n\
⎜    ⎢───────   ───── ⎥  ⎢ ─────   ───────⎥ ⎟     ⎢───────   ───── ⎥ \n\
⎜    ⎢x - 2⋅y   x + y ⎥  ⎢ x + y   x - 2⋅y⎥ ⎟     ⎢x - 2⋅y   x + y ⎥ \n\
⎜I - ⎢                ⎥ ⋅⎢                ⎥ ⎟   ⋅ ⎢                ⎥ \n\
⎜    ⎢ x - y    x + y ⎥  ⎢ x + y    x - y ⎥ ⎟     ⎢ x - y    x + y ⎥ \n\
⎜    ⎢ ─────   ───────⎥  ⎢───────   ───── ⎥ ⎟     ⎢ ─────   ───────⎥ \n\
⎝    ⎣ x + y   x - 2⋅y⎦τ ⎣x - 2⋅y   x + y ⎦τ⎠     ⎣ x + y   x - 2⋅y⎦τ\
"""
    expected2 = \
"""\
⎛    ⎡ x + y    x - y ⎤  ⎡ x - y    x + y ⎤  ⎡ x + y    x + y ⎤ ⎞-1   ⎡ x + y    x - y ⎤  ⎡ x - y    x + y ⎤ \n\
⎜    ⎢───────   ───── ⎥  ⎢ ─────   ───────⎥  ⎢───────  ───────⎥ ⎟     ⎢───────   ───── ⎥  ⎢ ─────   ───────⎥ \n\
⎜    ⎢x - 2⋅y   x + y ⎥  ⎢ x + y   x - 2⋅y⎥  ⎢x - 2⋅y  x - 2⋅y⎥ ⎟     ⎢x - 2⋅y   x + y ⎥  ⎢ x + y   x - 2⋅y⎥ \n\
⎜I + ⎢                ⎥ ⋅⎢                ⎥ ⋅⎢                ⎥ ⎟   ⋅ ⎢                ⎥ ⋅⎢                ⎥ \n\
⎜    ⎢ x - y    x + y ⎥  ⎢ x + y    x - y ⎥  ⎢ x - y    x - y ⎥ ⎟     ⎢ x - y    x + y ⎥  ⎢ x + y    x - y ⎥ \n\
⎜    ⎢ ─────   ───────⎥  ⎢───────   ───── ⎥  ⎢ ─────    ───── ⎥ ⎟     ⎢ ─────   ───────⎥  ⎢───────   ───── ⎥ \n\
⎝    ⎣ x + y   x - 2⋅y⎦τ ⎣x - 2⋅y   x + y ⎦τ ⎣ x + y    x + y ⎦τ⎠     ⎣ x + y   x - 2⋅y⎦τ ⎣x - 2⋅y   x + y ⎦τ\
"""

    assert upretty(MIMOFeedback(tfm_1, tfm_2, 1)) == \
        expected1  # Positive MIMOFeedback
    assert upretty(MIMOFeedback(tfm_1*tfm_2, tfm_3)) == \
        expected2  # Negative MIMOFeedback (Default)

