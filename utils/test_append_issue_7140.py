
def test_append_issue_7140(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    p1 = plot(x, adaptive=adaptive, n=10)
    p2 = plot(x**2, adaptive=adaptive, n=10)
    plot(x + 2, adaptive=adaptive, n=10)

    # append a series
    p2.append(p1[0])
    assert len(p2._series) == 2

    with raises(TypeError):
        p1.append(p2)

    with raises(TypeError):
        p1.append(p2._series)

