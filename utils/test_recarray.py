
def test_recarray(simple_dtype, packed_dtype):
    elements = [(False, 0, 0.0, -0.0), (True, 1, 1.5, -2.5), (False, 2, 3.0, -5.0)]

    for func, dtype in [
        (m.create_rec_simple, simple_dtype),
        (m.create_rec_packed, packed_dtype),
    ]:
        arr = func(0)
        assert arr.dtype == dtype
        assert_equal(arr, [], simple_dtype)
        assert_equal(arr, [], packed_dtype)

        arr = func(3)
        assert arr.dtype == dtype
        assert_equal(arr, elements, simple_dtype)
        assert_equal(arr, elements, packed_dtype)

        # Show what recarray's look like in NumPy.
        assert type(arr[0]) == np.void
        assert type(arr[0].item()) == tuple

        if dtype == simple_dtype:
            assert m.print_rec_simple(arr) == [
                "s:0,0,0,-0",
                "s:1,1,1.5,-2.5",
                "s:0,2,3,-5",
            ]
        else:
            assert m.print_rec_packed(arr) == [
                "p:0,0,0,-0",
                "p:1,1,1.5,-2.5",
                "p:0,2,3,-5",
            ]

    nested_dtype = np.dtype([("a", simple_dtype), ("b", packed_dtype)])

    arr = m.create_rec_nested(0)
    assert arr.dtype == nested_dtype
    assert_equal(arr, [], nested_dtype)

    arr = m.create_rec_nested(3)
    assert arr.dtype == nested_dtype
    assert_equal(
        arr,
        [
            ((False, 0, 0.0, -0.0), (True, 1, 1.5, -2.5)),
            ((True, 1, 1.5, -2.5), (False, 2, 3.0, -5.0)),
            ((False, 2, 3.0, -5.0), (True, 3, 4.5, -7.5)),
        ],
        nested_dtype,
    )
    assert m.print_rec_nested(arr) == [
        "n:a=s:0,0,0,-0;b=p:1,1,1.5,-2.5",
        "n:a=s:1,1,1.5,-2.5;b=p:0,2,3,-5",
        "n:a=s:0,2,3,-5;b=p:1,3,4.5,-7.5",
    ]

    arr = m.create_rec_partial(3)
    assert str(arr.dtype).replace(" ", "") == partial_dtype_fmt()
    partial_dtype = arr.dtype
    assert "" not in arr.dtype.fields
    assert partial_dtype.itemsize > simple_dtype.itemsize
    assert_equal(arr, elements, simple_dtype)
    assert_equal(arr, elements, packed_dtype)

    arr = m.create_rec_partial_nested(3)
    assert str(arr.dtype).replace(" ", "") == partial_nested_fmt()
    assert "" not in arr.dtype.fields
    assert "" not in arr.dtype.fields["a"][0].fields
    assert arr.dtype.itemsize > partial_dtype.itemsize
    np.testing.assert_equal(arr["a"], m.create_rec_partial(3))


def test_recarray():
    # check roundtrip of structured array
    dt = [('f1', 'f8'),
          ('f2', 'S10')]
    arr = np.zeros((2,), dtype=dt)
    arr[0]['f1'] = 0.5
    arr[0]['f2'] = 'python'
    arr[1]['f1'] = 99
    arr[1]['f2'] = 'not perl'
    stream = BytesIO()
    savemat(stream, {'arr': arr})
    d = loadmat(stream, struct_as_record=False)
    a20 = d['arr'][0,0]
    assert_equal(a20.f1, 0.5)
    assert_equal(a20.f2, 'python')
    d = loadmat(stream, struct_as_record=True)
    a20 = d['arr'][0,0]
    assert_equal(a20['f1'], 0.5)
    assert_equal(a20['f2'], 'python')
    # structs always come back as object types
    assert_equal(a20.dtype, np.dtype([('f1', 'O'),
                                      ('f2', 'O')]))
    a21 = d['arr'].flat[1]
    assert_equal(a21['f1'], 99)
    assert_equal(a21['f2'], 'not perl')

