
def test_set_policy(get_module):

    get_handler_name = np._core.multiarray.get_handler_name
    get_handler_version = np._core.multiarray.get_handler_version
    orig_policy_name = get_handler_name()

    a = np.arange(10).reshape((2, 5))  # a doesn't own its own data
    assert get_handler_name(a) is None
    assert get_handler_version(a) is None
    assert get_handler_name(a.base) == orig_policy_name
    assert get_handler_version(a.base) == 1

    orig_policy = get_module.set_secret_data_policy()

    b = np.arange(10).reshape((2, 5))  # b doesn't own its own data
    assert get_handler_name(b) is None
    assert get_handler_version(b) is None
    assert get_handler_name(b.base) == 'secret_data_allocator'
    assert get_handler_version(b.base) == 1

    if orig_policy_name == 'default_allocator':
        get_module.set_old_policy(None)  # tests PyDataMem_SetHandler(NULL)
        assert get_handler_name() == 'default_allocator'
    else:
        get_module.set_old_policy(orig_policy)
        assert get_handler_name() == orig_policy_name

    with pytest.raises(ValueError,
                       match="Capsule must be named 'mem_handler'"):
        get_module.set_wrong_capsule_name_data_policy()

