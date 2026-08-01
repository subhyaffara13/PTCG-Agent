
def test_pretty_piecewise():
    expr = Piecewise((x, x < 1), (x**2, True))
    ascii_str = \
"""\
/x   for x < 1\n\
|             \n\
< 2           \n\
|x   otherwise\n\
\\             \
"""
    ucode_str = \
"""\
⎧x   for x < 1\n\
⎪             \n\
⎨ 2           \n\
⎪x   otherwise\n\
⎩             \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = -Piecewise((x, x < 1), (x**2, True))
    ascii_str = \
"""\
 //x   for x < 1\\\n\
 ||             |\n\
-|< 2           |\n\
 ||x   otherwise|\n\
 \\\\             /\
"""
    ucode_str = \
"""\
 ⎛⎧x   for x < 1⎞\n\
 ⎜⎪             ⎟\n\
-⎜⎨ 2           ⎟\n\
 ⎜⎪x   otherwise⎟\n\
 ⎝⎩             ⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = x + Piecewise((x, x > 0), (y, True)) + Piecewise((x/y, x < 2),
    (y**2, x > 2), (1, True)) + 1
    ascii_str = \
"""\
                      //x            \\    \n\
                      ||-   for x < 2|    \n\
                      ||y            |    \n\
    //x  for x > 0\\   ||             |    \n\
x + |<            | + |< 2           | + 1\n\
    \\\\y  otherwise/   ||y   for x > 2|    \n\
                      ||             |    \n\
                      ||1   otherwise|    \n\
                      \\\\             /    \
"""
    ucode_str = \
"""\
                      ⎛⎧x            ⎞    \n\
                      ⎜⎪─   for x < 2⎟    \n\
                      ⎜⎪y            ⎟    \n\
    ⎛⎧x  for x > 0⎞   ⎜⎪             ⎟    \n\
x + ⎜⎨            ⎟ + ⎜⎨ 2           ⎟ + 1\n\
    ⎝⎩y  otherwise⎠   ⎜⎪y   for x > 2⎟    \n\
                      ⎜⎪             ⎟    \n\
                      ⎜⎪1   otherwise⎟    \n\
                      ⎝⎩             ⎠    \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = x - Piecewise((x, x > 0), (y, True)) + Piecewise((x/y, x < 2),
    (y**2, x > 2), (1, True)) + 1
    ascii_str = \
"""\
                      //x            \\    \n\
                      ||-   for x < 2|    \n\
                      ||y            |    \n\
    //x  for x > 0\\   ||             |    \n\
x - |<            | + |< 2           | + 1\n\
    \\\\y  otherwise/   ||y   for x > 2|    \n\
                      ||             |    \n\
                      ||1   otherwise|    \n\
                      \\\\             /    \
"""
    ucode_str = \
"""\
                      ⎛⎧x            ⎞    \n\
                      ⎜⎪─   for x < 2⎟    \n\
                      ⎜⎪y            ⎟    \n\
    ⎛⎧x  for x > 0⎞   ⎜⎪             ⎟    \n\
x - ⎜⎨            ⎟ + ⎜⎨ 2           ⎟ + 1\n\
    ⎝⎩y  otherwise⎠   ⎜⎪y   for x > 2⎟    \n\
                      ⎜⎪             ⎟    \n\
                      ⎜⎪1   otherwise⎟    \n\
                      ⎝⎩             ⎠    \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = x*Piecewise((x, x > 0), (y, True))
    ascii_str = \
"""\
  //x  for x > 0\\\n\
x*|<            |\n\
  \\\\y  otherwise/\
"""
    ucode_str = \
"""\
  ⎛⎧x  for x > 0⎞\n\
x⋅⎜⎨            ⎟\n\
  ⎝⎩y  otherwise⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Piecewise((x, x > 0), (y, True))*Piecewise((x/y, x < 2), (y**2, x >
    2), (1, True))
    ascii_str = \
"""\
                //x            \\\n\
                ||-   for x < 2|\n\
                ||y            |\n\
//x  for x > 0\\ ||             |\n\
|<            |*|< 2           |\n\
\\\\y  otherwise/ ||y   for x > 2|\n\
                ||             |\n\
                ||1   otherwise|\n\
                \\\\             /\
"""
    ucode_str = \
"""\
                ⎛⎧x            ⎞\n\
                ⎜⎪─   for x < 2⎟\n\
                ⎜⎪y            ⎟\n\
⎛⎧x  for x > 0⎞ ⎜⎪             ⎟\n\
⎜⎨            ⎟⋅⎜⎨ 2           ⎟\n\
⎝⎩y  otherwise⎠ ⎜⎪y   for x > 2⎟\n\
                ⎜⎪             ⎟\n\
                ⎜⎪1   otherwise⎟\n\
                ⎝⎩             ⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = -Piecewise((x, x > 0), (y, True))*Piecewise((x/y, x < 2), (y**2, x
        > 2), (1, True))
    ascii_str = \
"""\
                 //x            \\\n\
                 ||-   for x < 2|\n\
                 ||y            |\n\
 //x  for x > 0\\ ||             |\n\
-|<            |*|< 2           |\n\
 \\\\y  otherwise/ ||y   for x > 2|\n\
                 ||             |\n\
                 ||1   otherwise|\n\
                 \\\\             /\
"""
    ucode_str = \
"""\
                 ⎛⎧x            ⎞\n\
                 ⎜⎪─   for x < 2⎟\n\
                 ⎜⎪y            ⎟\n\
 ⎛⎧x  for x > 0⎞ ⎜⎪             ⎟\n\
-⎜⎨            ⎟⋅⎜⎨ 2           ⎟\n\
 ⎝⎩y  otherwise⎠ ⎜⎪y   for x > 2⎟\n\
                 ⎜⎪             ⎟\n\
                 ⎜⎪1   otherwise⎟\n\
                 ⎝⎩             ⎠\
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    expr = Piecewise((0, Abs(1/y) < 1), (1, Abs(y) < 1), (y*meijerg(((2, 1),
        ()), ((), (1, 0)), 1/y), True))
    ascii_str = \
"""\
/                                 1     \n\
|            0               for --- < 1\n\
|                                |y|    \n\
|                                       \n\
<            1               for |y| < 1\n\
|                                       \n\
|   __0, 2 /1, 2       | 1\\             \n\
|y*/__     |           | -|   otherwise \n\
\\  \\_|2, 2 \\      0, 1 | y/             \
"""
    ucode_str = \
"""\
⎧                                 1     \n\
⎪            0               for ─── < 1\n\
⎪                                │y│    \n\
⎪                                       \n\
⎨            1               for │y│ < 1\n\
⎪                                       \n\
⎪  ╭─╮0, 2 ⎛1, 2       │ 1⎞             \n\
⎪y⋅│╶┐     ⎜           │ ─⎟   otherwise \n\
⎩  ╰─╯2, 2 ⎝      0, 1 │ y⎠             \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

    # XXX: We have to use evaluate=False here because Piecewise._eval_power
    # denests the power.
    expr = Pow(Piecewise((x, x > 0), (y, True)), 2, evaluate=False)
    ascii_str = \
"""\
               2\n\
//x  for x > 0\\ \n\
|<            | \n\
\\\\y  otherwise/ \
"""
    ucode_str = \
"""\
               2\n\
⎛⎧x  for x > 0⎞ \n\
⎜⎨            ⎟ \n\
⎝⎩y  otherwise⎠ \
"""
    assert pretty(expr) == ascii_str
    assert upretty(expr) == ucode_str

