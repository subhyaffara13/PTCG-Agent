
def test_pretty_sets():
    s = FiniteSet
    assert pretty(s(*[x*y, x**2])) == \
"""\
  2      \n\
{x , x*y}\
"""
    assert pretty(s(*range(1, 6))) == "{1, 2, 3, 4, 5}"
    assert pretty(s(*range(1, 13))) == "{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}"

    assert pretty({x*y, x**2}) == \
"""\
  2      \n\
{x , x*y}\
"""
    assert pretty(set(range(1, 6))) == "{1, 2, 3, 4, 5}"
    assert pretty(set(range(1, 13))) == \
        "{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}"

    assert pretty(frozenset([x*y, x**2])) == \
"""\
            2       \n\
frozenset({x , x*y})\
"""
    assert pretty(frozenset(range(1, 6))) == "frozenset({1, 2, 3, 4, 5})"
    assert pretty(frozenset(range(1, 13))) == \
        "frozenset({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12})"

    assert pretty(Range(0, 3, 1)) == '{0, 1, 2}'

    ascii_str = '{0, 1, ..., 29}'
    ucode_str = '{0, 1, …, 29}'
    assert pretty(Range(0, 30, 1)) == ascii_str
    assert upretty(Range(0, 30, 1)) == ucode_str

    ascii_str = '{30, 29, ..., 2}'
    ucode_str = '{30, 29, …, 2}'
    assert pretty(Range(30, 1, -1)) == ascii_str
    assert upretty(Range(30, 1, -1)) == ucode_str

    ascii_str = '{0, 2, ...}'
    ucode_str = '{0, 2, …}'
    assert pretty(Range(0, oo, 2)) == ascii_str
    assert upretty(Range(0, oo, 2)) == ucode_str

    ascii_str = '{..., 2, 0}'
    ucode_str = '{…, 2, 0}'
    assert pretty(Range(oo, -2, -2)) == ascii_str
    assert upretty(Range(oo, -2, -2)) == ucode_str

    ascii_str = '{-2, -3, ...}'
    ucode_str = '{-2, -3, …}'
    assert pretty(Range(-2, -oo, -1)) == ascii_str
    assert upretty(Range(-2, -oo, -1)) == ucode_str

