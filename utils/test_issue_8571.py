
def test_issue_8571():
    for t in (S.true, S.false):
        raises(TypeError, lambda: +t)
        raises(TypeError, lambda: -t)
        raises(TypeError, lambda: abs(t))
        # use int(bool(t)) to get 0 or 1
        raises(TypeError, lambda: int(t))

        for o in [S.Zero, S.One, x]:
            for _ in range(2):
                raises(TypeError, lambda: o + t)
                raises(TypeError, lambda: o - t)
                raises(TypeError, lambda: o % t)
                raises(TypeError, lambda: o * t)
                raises(TypeError, lambda: o / t)
                raises(TypeError, lambda: o ** t)
                o, t = t, o  # do again in reversed order

