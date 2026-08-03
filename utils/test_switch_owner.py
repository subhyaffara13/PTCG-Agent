import os

def test_switch_owner(get_module, policy):
    a = get_module.get_array()
    assert np._core.multiarray.get_handler_name(a) is None
    get_module.set_own(a)

    if policy is None:
        # See what we expect to be set based on the env variable
        policy = os.getenv("NUMPY_WARN_IF_NO_MEM_POLICY", "0") == "1"
        oldval = None
    else:
        policy = policy == "1"
        oldval = np._core._multiarray_umath._set_numpy_warn_if_no_mem_policy(
            policy)
    try:
        # The policy should be NULL, so we have to assume we can call
        # "free".  A warning is given if the policy == "1"
        if policy:
            with pytest.warns(RuntimeWarning) as w:
                del a
                gc.collect()
        else:
            del a
            gc.collect()

    finally:
        if oldval is not None:
            np._core._multiarray_umath._set_numpy_warn_if_no_mem_policy(oldval)

