
def test_rewrite_same():
    # Rewrite to same basis
    assert JxBra(1, 1).rewrite('Jx') == JxBra(1, 1)
    assert JxBra(j, m).rewrite('Jx') == JxBra(j, m)
    assert JxKet(1, 1).rewrite('Jx') == JxKet(1, 1)
    assert JxKet(j, m).rewrite('Jx') == JxKet(j, m)

