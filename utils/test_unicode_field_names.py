import os

def test_unicode_field_names(tmpdir):
    # gh-7391
    arr = np.array([
        (1, 3),
        (1, 2),
        (1, 3),
        (1, 2)
    ], dtype=[
        ('int', int),
        ('\N{CJK UNIFIED IDEOGRAPH-6574}\N{CJK UNIFIED IDEOGRAPH-5F62}', int)
    ])
    fname = os.path.join(tmpdir, "unicode.npy")
    with open(fname, 'wb') as f:
        format.write_array(f, arr, version=(3, 0))
    with open(fname, 'rb') as f:
        arr2 = format.read_array(f)
    assert_array_equal(arr, arr2)

    # notifies the user that 3.0 is selected
    with open(fname, 'wb') as f:
        with pytest.warns(UserWarning):
            format.write_array(f, arr, version=None)

