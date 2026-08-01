
def test_thread_locality(get_module):
    orig_policy_name = np._core.multiarray.get_handler_name()

    event = threading.Event()
    # the child threads do not inherit the parent policy
    concurrent_task1 = threading.Thread(target=concurrent_thread1,
                                        args=(get_module, event))
    concurrent_task2 = threading.Thread(target=concurrent_thread2,
                                        args=(get_module, event))
    concurrent_task1.start()
    concurrent_task2.start()
    concurrent_task1.join()
    concurrent_task2.join()

    # the parent thread is not affected by child policy changes
    assert np._core.multiarray.get_handler_name() == orig_policy_name

