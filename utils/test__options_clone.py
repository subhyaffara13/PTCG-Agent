
def test_Options_clone():
    opt = Options((x, y, z), {'domain': 'ZZ'})

    assert opt.gens == (x, y, z)
    assert opt.domain == ZZ
    assert ('order' in opt) is False

    new_opt = opt.clone({'gens': (x, y), 'order': 'lex'})

    assert opt.gens == (x, y, z)
    assert opt.domain == ZZ
    assert ('order' in opt) is False

    assert new_opt.gens == (x, y)
    assert new_opt.domain == ZZ
    assert ('order' in new_opt) is True

