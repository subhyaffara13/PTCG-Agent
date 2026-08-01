
def test_print_builtin_set():
    assert pretty(set()) == 'set()'
    assert upretty(set()) == 'set()'

    assert pretty(frozenset()) == 'frozenset()'
    assert upretty(frozenset()) == 'frozenset()'

    s1 = {1/x, x}
    s2 = frozenset(s1)

    assert pretty(s1) == \
"""\
 1    \n\
{-, x}
 x    \
"""
    assert upretty(s1) == \
"""\
⎧1   ⎫
⎨─, x⎬
⎩x   ⎭\
"""

    assert pretty(s2) == \
"""\
           1     \n\
frozenset({-, x})
           x     \
"""
    assert upretty(s2) == \
"""\
         ⎛⎧1   ⎫⎞
frozenset⎜⎨─, x⎬⎟
         ⎝⎩x   ⎭⎠\
"""

