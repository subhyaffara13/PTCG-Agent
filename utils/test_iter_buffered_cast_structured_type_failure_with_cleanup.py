
def test_iter_buffered_cast_structured_type_failure_with_cleanup():
    # make sure struct type -> struct type with different
    # number of fields fails
    sdt1 = [('a', 'f4'), ('b', 'i8'), ('d', 'O')]
    sdt2 = [('b', 'O'), ('a', 'f8')]
    a = np.array([(1, 2, 3), (4, 5, 6)], dtype=sdt1)

    for intent in ["readwrite", "readonly", "writeonly"]:
        # This test was initially designed to test an error at a different
        # place, but will now raise earlier due to the cast not being possible:
        # `assert np.can_cast(a.dtype, sdt2, casting="unsafe")` fails.
        # Without a faulty DType, there is probably no reliable
        # way to get the initial tested behaviour.
        simple_arr = np.array([1, 2], dtype="i,i")  # requires clean up
        with pytest.raises(TypeError):
            nditer((simple_arr, a), ['buffered', 'refs_ok'], [intent, intent],
                   casting='unsafe', op_dtypes=["f,f", sdt2])

