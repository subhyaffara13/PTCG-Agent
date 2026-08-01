
def test_Print():
    fmt = "%d %.3f"
    ps = Print([n, x], fmt)
    assert str(ps.format_string) == fmt
    assert ps.print_args == Tuple(n, x)
    assert ps.args == (Tuple(n, x), QuotedString(fmt), none)
    assert ps == Print((n, x), fmt)
    assert ps != Print([x, n], fmt)
    assert ps.func(*ps.args) == ps

    ps2 = Print([n, x])
    assert ps2 == Print([n, x])
    assert ps2 != ps
    assert ps2.format_string == None

