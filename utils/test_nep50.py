
def test_nep50(ufunc):
    # Test that functions with multiple arguments respect nep50 promotion rules.
    rng = np.random.default_rng(1234)
    # As in test_ufunc_signatures, filter out signatures involving integers.
    types = set(sig for sig in ufunc.types
                if not ("l" in sig or "i" in sig or "q" in sig or "p" in sig))
    for sig in types:
        input_types, output_types = sig.split("->")
        # since we only care about dtypes and not values here, just use an appropriately
        # typed nan for each argument.
        args = [_get_nan_val(typecode) for typecode in input_types]
        # swap out a random one of the nans with an appropriately typed numpy scalar.
        idx = rng.choice(len(args))
        args[idx] = float("nan") if np.isrealobj(args[idx]) else complex("nan")
        result = ufunc(*args)
        result = [result] if len(output_types) == 1 else result
        result = np.asarray(result)
        
        # Test that the output is an appropriately typed nan. This also implicitly
        # tests that ufuncs propagate nans correctly.
        assert_equal(
            result, np.asarray([_get_nan_val(typecode) for typecode in output_types]),
            strict=True
        )

