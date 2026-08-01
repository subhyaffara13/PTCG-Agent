
def test_policy_propagation(get_module):
    # The memory policy goes hand-in-hand with flags.owndata

    class MyArr(np.ndarray):
        pass

    get_handler_name = np._core.multiarray.get_handler_name
    orig_policy_name = get_handler_name()
    a = np.arange(10).view(MyArr).reshape((2, 5))
    assert get_handler_name(a) is None
    assert a.flags.owndata is False

    assert get_handler_name(a.base) is None
    assert a.base.flags.owndata is False

    assert get_handler_name(a.base.base) == orig_policy_name
    assert a.base.base.flags.owndata is True

