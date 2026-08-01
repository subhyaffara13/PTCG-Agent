
def test_SingularityFunction():
    assert xpretty(SingularityFunction(x, 0, n), use_unicode=True) == (
"""\
   n\n\
<x> \
""")
    assert xpretty(SingularityFunction(x, 1, n), use_unicode=True) == (
"""\
       n\n\
<x - 1> \
""")
    assert xpretty(SingularityFunction(x, -1, n), use_unicode=True) == (
"""\
       n\n\
<x + 1> \
""")
    assert xpretty(SingularityFunction(x, a, n), use_unicode=True) == (
"""\
        n\n\
<-a + x> \
""")
    assert xpretty(SingularityFunction(x, y, n), use_unicode=True) == (
"""\
       n\n\
<x - y> \
""")
    assert xpretty(SingularityFunction(x, 0, n), use_unicode=False) == (
"""\
   n\n\
<x> \
""")
    assert xpretty(SingularityFunction(x, 1, n), use_unicode=False) == (
"""\
       n\n\
<x - 1> \
""")
    assert xpretty(SingularityFunction(x, -1, n), use_unicode=False) == (
"""\
       n\n\
<x + 1> \
""")
    assert xpretty(SingularityFunction(x, a, n), use_unicode=False) == (
"""\
        n\n\
<-a + x> \
""")
    assert xpretty(SingularityFunction(x, y, n), use_unicode=False) == (
"""\
       n\n\
<x - y> \
""")

