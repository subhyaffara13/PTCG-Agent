
def test_string_fallbacks():
    # We can (currently?) use numpy strings to test the "slow" fallbacks
    # that should normally not be taken due to string interning.
    arg2 = np.str_("arg2")
    missing_arg = np.str_("missing_arg")
    func(1, **{arg2: 3})
    with pytest.raises(TypeError,
            match="got an unexpected keyword argument 'missing_arg'"):
        func(2, **{missing_arg: 3})

