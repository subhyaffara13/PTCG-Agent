
def test_new_policy(get_module):
    a = np.arange(10)
    orig_policy_name = np._core.multiarray.get_handler_name(a)

    orig_policy = get_module.set_secret_data_policy()

    b = np.arange(10)
    assert np._core.multiarray.get_handler_name(b) == 'secret_data_allocator'

    # test array manipulation. This is slow
    if orig_policy_name == 'default_allocator':
        # when the np._core.test tests recurse into this test, the
        # policy will be set so this "if" will be false, preventing
        # infinite recursion
        #
        # if needed, debug this by
        # - running tests with -- -s (to not capture stdout/stderr
        # - setting verbose=2
        # - setting extra_argv=['-vv'] here
        assert np._core.test('full', verbose=1, extra_argv=[])
        # also try the ma tests, the pickling test is quite tricky
        assert np.ma.test('full', verbose=1, extra_argv=[])

    get_module.set_old_policy(orig_policy)

    c = np.arange(10)
    assert np._core.multiarray.get_handler_name(c) == orig_policy_name

