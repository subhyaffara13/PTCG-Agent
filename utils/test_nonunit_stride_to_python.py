
def test_nonunit_stride_to_python():
    assert np.all(m.diagonal(ref) == ref.diagonal())
    assert np.all(m.diagonal_1(ref) == ref.diagonal(1))
    for i in range(-5, 7):
        assert np.all(m.diagonal_n(ref, i) == ref.diagonal(i)), f"m.diagonal_n({i})"

    # Must be order="F", otherwise the type_caster will make a copy and
    # m.block() will return a dangling reference (heap-use-after-free).
    rof = np.asarray(ref, order="F")
    assert np.all(m.block(rof, 2, 1, 3, 3) == rof[2:5, 1:4])
    assert np.all(m.block(rof, 1, 4, 4, 2) == rof[1:, 4:])
    assert np.all(m.block(rof, 1, 4, 3, 2) == rof[1:4, 4:])

