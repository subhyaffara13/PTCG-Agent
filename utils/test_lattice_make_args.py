
def test_lattice_make_args():
    assert join.make_args(join(2, 3, 4)) == {S(2), S(3), S(4)}
    assert join.make_args(0) == {0}
    assert list(join.make_args(0))[0] is S.Zero
    assert Add.make_args(0)[0] is S.Zero

