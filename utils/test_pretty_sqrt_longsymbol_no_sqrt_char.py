
def test_pretty_sqrt_longsymbol_no_sqrt_char():
    # Do not use unicode sqrt char for long symbols (see PR #9234).
    expr = sqrt(Symbol('C1'))
    ucode_str = \
"""\
  ____\n\
╲╱ C₁ \
"""
    assert upretty(expr) == ucode_str

