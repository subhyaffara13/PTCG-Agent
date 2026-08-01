
def test_pretty_Feedback():
    tf = TransferFunction(1, 1, y)
    tf1 = TransferFunction(x + y, x - 2*y, y)
    tf2 = TransferFunction(x - y, x + y, y)
    tf3 = TransferFunction(y**2 - 2*y + 1, y + 5, y)
    tf4 = TransferFunction(x - 2*y**3, x + y, x)
    tf5 = TransferFunction(1 - x, x - y, y)
    tf6 = TransferFunction(2, 2, x)
    expected1 = \
"""\
     ⎛1⎞     \n\
     ⎜─⎟     \n\
     ⎝1⎠     \n\
─────────────\n\
1   ⎛ x + y ⎞\n\
─ + ⎜───────⎟\n\
1   ⎝x - 2⋅y⎠\
"""
    expected2 = \
"""\
                ⎛1⎞                 \n\
                ⎜─⎟                 \n\
                ⎝1⎠                 \n\
────────────────────────────────────\n\
                      ⎛ 2          ⎞\n\
1   ⎛x - y⎞ ⎛ x + y ⎞ ⎜y  - 2⋅y + 1⎟\n\
─ + ⎜─────⎟⋅⎜───────⎟⋅⎜────────────⎟\n\
1   ⎝x + y⎠ ⎝x - 2⋅y⎠ ⎝   y + 5    ⎠\
"""
    expected3 = \
"""\
                 ⎛ x + y ⎞                  \n\
                 ⎜───────⎟                  \n\
                 ⎝x - 2⋅y⎠                  \n\
────────────────────────────────────────────\n\
                      ⎛ 2          ⎞        \n\
1   ⎛ x + y ⎞ ⎛x - y⎞ ⎜y  - 2⋅y + 1⎟ ⎛1 - x⎞\n\
─ + ⎜───────⎟⋅⎜─────⎟⋅⎜────────────⎟⋅⎜─────⎟\n\
1   ⎝x - 2⋅y⎠ ⎝x + y⎠ ⎝   y + 5    ⎠ ⎝x - y⎠\
"""
    expected4 = \
"""\
  ⎛ x + y ⎞ ⎛x - y⎞  \n\
  ⎜───────⎟⋅⎜─────⎟  \n\
  ⎝x - 2⋅y⎠ ⎝x + y⎠  \n\
─────────────────────\n\
1   ⎛ x + y ⎞ ⎛x - y⎞\n\
─ + ⎜───────⎟⋅⎜─────⎟\n\
1   ⎝x - 2⋅y⎠ ⎝x + y⎠\
"""
    expected5 = \
"""\
      ⎛ x + y ⎞ ⎛x - y⎞      \n\
      ⎜───────⎟⋅⎜─────⎟      \n\
      ⎝x - 2⋅y⎠ ⎝x + y⎠      \n\
─────────────────────────────\n\
1   ⎛ x + y ⎞ ⎛x - y⎞ ⎛1 - x⎞\n\
─ + ⎜───────⎟⋅⎜─────⎟⋅⎜─────⎟\n\
1   ⎝x - 2⋅y⎠ ⎝x + y⎠ ⎝x - y⎠\
"""
    expected6 = \
"""\
           ⎛ 2          ⎞                   \n\
           ⎜y  - 2⋅y + 1⎟ ⎛1 - x⎞           \n\
           ⎜────────────⎟⋅⎜─────⎟           \n\
           ⎝   y + 5    ⎠ ⎝x - y⎠           \n\
────────────────────────────────────────────\n\
    ⎛ 2          ⎞                          \n\
1   ⎜y  - 2⋅y + 1⎟ ⎛1 - x⎞ ⎛x - y⎞ ⎛ x + y ⎞\n\
─ + ⎜────────────⎟⋅⎜─────⎟⋅⎜─────⎟⋅⎜───────⎟\n\
1   ⎝   y + 5    ⎠ ⎝x - y⎠ ⎝x + y⎠ ⎝x - 2⋅y⎠\
"""
    expected7 = \
"""\
    ⎛       3⎞    \n\
    ⎜x - 2⋅y ⎟    \n\
    ⎜────────⎟    \n\
    ⎝ x + y  ⎠    \n\
──────────────────\n\
    ⎛       3⎞    \n\
1   ⎜x - 2⋅y ⎟ ⎛2⎞\n\
─ + ⎜────────⎟⋅⎜─⎟\n\
1   ⎝ x + y  ⎠ ⎝2⎠\
"""
    expected8 = \
"""\
  ⎛1 - x⎞  \n\
  ⎜─────⎟  \n\
  ⎝x - y⎠  \n\
───────────\n\
1   ⎛1 - x⎞\n\
─ + ⎜─────⎟\n\
1   ⎝x - y⎠\
"""
    expected9 = \
"""\
      ⎛ x + y ⎞ ⎛x - y⎞      \n\
      ⎜───────⎟⋅⎜─────⎟      \n\
      ⎝x - 2⋅y⎠ ⎝x + y⎠      \n\
─────────────────────────────\n\
1   ⎛ x + y ⎞ ⎛x - y⎞ ⎛1 - x⎞\n\
─ - ⎜───────⎟⋅⎜─────⎟⋅⎜─────⎟\n\
1   ⎝x - 2⋅y⎠ ⎝x + y⎠ ⎝x - y⎠\
"""
    expected10 = \
"""\
  ⎛1 - x⎞  \n\
  ⎜─────⎟  \n\
  ⎝x - y⎠  \n\
───────────\n\
1   ⎛1 - x⎞\n\
─ - ⎜─────⎟\n\
1   ⎝x - y⎠\
"""
    assert upretty(Feedback(tf, tf1)) == expected1
    assert upretty(Feedback(tf, tf2*tf1*tf3)) == expected2
    assert upretty(Feedback(tf1, tf2*tf3*tf5)) == expected3
    assert upretty(Feedback(tf1*tf2, tf)) == expected4
    assert upretty(Feedback(tf1*tf2, tf5)) == expected5
    assert upretty(Feedback(tf3*tf5, tf2*tf1)) == expected6
    assert upretty(Feedback(tf4, tf6)) == expected7
    assert upretty(Feedback(tf5, tf)) == expected8

    assert upretty(Feedback(tf1*tf2, tf5, 1)) == expected9
    assert upretty(Feedback(tf5, tf, 1)) == expected10

