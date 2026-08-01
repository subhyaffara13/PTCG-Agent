
def test_scalar_conversion():
    n = 3
    arrays = [
        m.create_rec_simple(n),
        m.create_rec_packed(n),
        m.create_rec_nested(n),
        m.create_enum_array(n),
    ]
    funcs = [m.f_simple, m.f_packed, m.f_nested]

    for i, func in enumerate(funcs):
        for j, arr in enumerate(arrays):
            if i == j and i < 2:
                assert [func(arr[k]) for k in range(n)] == [k * 10 for k in range(n)]
            else:
                with pytest.raises(TypeError) as excinfo:
                    func(arr[0])
                assert "incompatible function arguments" in str(excinfo.value)

