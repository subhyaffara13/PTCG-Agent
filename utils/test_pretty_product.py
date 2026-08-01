
def test_pretty_product():
    n, m, k, l = symbols('n m k l')
    f = symbols('f', cls=Function)
    expr = Product(f((n/3)**2), (n, k**2, l))

    unicode_str = \
"""\
    l           \n\
─┬──────┬─      \n\
 │      │   ⎛ 2⎞\n\
 │      │   ⎜n ⎟\n\
 │      │  f⎜──⎟\n\
 │      │   ⎝9 ⎠\n\
 │      │       \n\
       2        \n\
  n = k         """
    ascii_str = \
"""\
    l           \n\
__________      \n\
 |      |   / 2\\\n\
 |      |   |n |\n\
 |      |  f|--|\n\
 |      |   \\9 /\n\
 |      |       \n\
       2        \n\
  n = k         """

    expr = Product(f((n/3)**2), (n, k**2, l), (l, 1, m))

    unicode_str = \
"""\
    m          l           \n\
─┬──────┬─ ─┬──────┬─      \n\
 │      │   │      │   ⎛ 2⎞\n\
 │      │   │      │   ⎜n ⎟\n\
 │      │   │      │  f⎜──⎟\n\
 │      │   │      │   ⎝9 ⎠\n\
 │      │   │      │       \n\
  l = 1           2        \n\
             n = k         """
    ascii_str = \
"""\
    m          l           \n\
__________ __________      \n\
 |      |   |      |   / 2\\\n\
 |      |   |      |   |n |\n\
 |      |   |      |  f|--|\n\
 |      |   |      |   \\9 /\n\
 |      |   |      |       \n\
  l = 1           2        \n\
             n = k         """

    assert pretty(expr) == ascii_str
    assert upretty(expr) == unicode_str

