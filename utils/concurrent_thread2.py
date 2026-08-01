
def concurrent_thread2(get_module, event):
    event.wait()
    # the policy is not affected by changes in parallel threads
    assert np._core.multiarray.get_handler_name() == 'default_allocator'
    # change policy in the child thread
    get_module.set_secret_data_policy()

