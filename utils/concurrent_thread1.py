
def concurrent_thread1(get_module, event):
    get_module.set_secret_data_policy()
    assert np._core.multiarray.get_handler_name() == 'secret_data_allocator'
    event.set()

