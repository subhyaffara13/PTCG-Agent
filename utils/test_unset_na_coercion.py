
def test_unset_na_coercion():
    # a dtype instance with an unset na object is compatible
    # with a dtype that has one set

    # this test uses the "add" and "equal" ufunc but all ufuncs that
    # accept more than one string argument and produce a string should
    # behave this way
    # TODO: generalize to more ufuncs
    inp = ["hello", "world"]
    arr = np.array(inp, dtype=StringDType(na_object=None))
    for op_dtype in [None, StringDType(), StringDType(coerce=False),
                     StringDType(na_object=None)]:
        if op_dtype is None:
            op = "2"
        else:
            op = np.array("2", dtype=op_dtype)
        res = arr + op
        assert_array_equal(res, ["hello2", "world2"])

    # dtype instances with distinct explicitly set NA objects are incompatible
    for op_dtype in [StringDType(na_object=pd_NA), StringDType(na_object="")]:
        op = np.array("2", dtype=op_dtype)
        with pytest.raises(TypeError):
            arr + op

    # comparisons only consider the na_object
    for op_dtype in [None, StringDType(), StringDType(coerce=True),
                     StringDType(na_object=None)]:
        if op_dtype is None:
            op = inp
        else:
            op = np.array(inp, dtype=op_dtype)
        assert_array_equal(arr, op)

    for op_dtype in [StringDType(na_object=pd_NA),
                     StringDType(na_object=np.nan)]:
        op = np.array(inp, dtype=op_dtype)
        with pytest.raises(TypeError):
            arr == op

