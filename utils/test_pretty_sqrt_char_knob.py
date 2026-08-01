
def test_pretty_sqrt_char_knob():
    # See PR #9234.
    expr = sqrt(2)
    ucode_str1 = \
"""\
  ___\n\
╲╱ 2 \
"""
    ucode_str2 = \
"√2"
    assert xpretty(expr, use_unicode=True,
                   use_unicode_sqrt_char=False) == ucode_str1
    assert xpretty(expr, use_unicode=True,
                   use_unicode_sqrt_char=True) == ucode_str2

