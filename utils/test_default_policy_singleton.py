
def test_default_policy_singleton(get_module):
    get_handler_name = np._core.multiarray.get_handler_name

    # set the policy to default
    orig_policy = get_module.set_old_policy(None)

    assert get_handler_name() == 'default_allocator'

    # re-set the policy to default
    def_policy_1 = get_module.set_old_policy(None)

    assert get_handler_name() == 'default_allocator'

    # set the policy to original
    def_policy_2 = get_module.set_old_policy(orig_policy)

    # since default policy is a singleton,
    # these should be the same object
    assert def_policy_1 is def_policy_2 is get_module.get_default_policy()

