
def test_npzfile_dict():
    s = BytesIO()
    x = np.zeros((3, 3))
    y = np.zeros((3, 3))

    np.savez(s, x=x, y=y)
    s.seek(0)

    z = np.load(s)

    assert_('x' in z)
    assert_('y' in z)
    assert_('x' in z.keys())
    assert_('y' in z.keys())

    for f, a in z.items():
        assert_(f in ['x', 'y'])
        assert_equal(a.shape, (3, 3))

    for a in z.values():
        assert_equal(a.shape, (3, 3))

    assert_(len(z.items()) == 2)

    for f in z:
        assert_(f in ['x', 'y'])

    assert_('x' in z.keys())
    assert (z.get('x') == z['x']).all()

