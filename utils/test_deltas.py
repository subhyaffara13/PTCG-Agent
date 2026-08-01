
def test_deltas():
    assert xpretty(DiracDelta(x), use_unicode=True) == 'δ(x)'
    assert xpretty(DiracDelta(x, 1), use_unicode=True) == \
"""\
 (1)    \n\
δ    (x)\
"""
    assert xpretty(x*DiracDelta(x, 1), use_unicode=True) == \
"""\
   (1)    \n\
x⋅δ    (x)\
"""

