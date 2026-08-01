
def test_warn_len_equal_call_scenarios():
    # assert_warn_len_equal is called under
    # varying circumstances depending on serial
    # vs. parallel test scenarios; this test
    # simply aims to probe both code paths and
    # check that no assertion is uncaught

    # parallel scenario -- no warning issued yet
    class mod:
        pass

    mod_inst = mod()

    assert_warn_len_equal(mod=mod_inst,
                          n_in_context=0)

    # serial test scenario -- the __warningregistry__
    # attribute should be present
    class mod:
        def __init__(self):
            self.__warningregistry__ = {'warning1': 1,
                                        'warning2': 2}

    mod_inst = mod()
    assert_warn_len_equal(mod=mod_inst,
                          n_in_context=2)

