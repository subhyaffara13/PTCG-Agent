import itertools

def test_nat_casts():
    s = 'nat'
    all_nats = itertools.product(*zip(s.upper(), s.lower()))
    all_nats = list(map(''.join, all_nats))
    NaT_dt = np.datetime64('NaT', 'D')
    NaT_td = np.timedelta64('NaT', 's')
    for na_object in [np._NoValue, None, np.nan, 'nat', '']:
        # numpy treats empty string and all case combinations of 'nat' as NaT
        dtype = StringDType(na_object=na_object)
        arr = np.array([''] + all_nats, dtype=dtype)
        dt_array = arr.astype('M8[s]')
        td_array = arr.astype('m8[s]')
        assert_array_equal(dt_array, NaT_dt)
        assert_array_equal(td_array, NaT_td)

        if na_object is np._NoValue:
            output_object = 'NaT'
        else:
            output_object = na_object

        for arr in [dt_array, td_array]:
            assert_array_equal(
                arr.astype(dtype),
                np.array([output_object] * arr.size, dtype=dtype))

