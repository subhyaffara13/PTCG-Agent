
def dist_init(
    old_test_method=None,
    setup_rpc: bool = True,
    clean_shutdown: bool = True,
    faulty_messages=None,
    messages_to_delay=None,
):
    """
    We use this decorator for setting up and tearing down state since
    MultiProcessTestCase runs each `test*` method in a separate process and
    each process just runs the `test*` method without actually calling
    'setUp' and 'tearDown' methods of unittest.

    Note: pass the string representation of MessageTypes that should be used
    with the faulty agent's send function. By default, all retriable messages
    ("RREF_FORK_REQUEST", "RREF_CHILD_ACCEPT", "RREF_USER_DELETE",
    "CLEANUP_AUTOGRAD_CONTEXT_REQ") will use the faulty send (this default is
    set from faulty_rpc_agent_test_fixture.py).
    """
    # If we use dist_init without arguments (ex: @dist_init), old_test_method is
    # appropriately set and we return the wrapper appropriately. On the other
    # hand if dist_init has arguments (ex: @dist_init(clean_shutdown=False)),
    # old_test_method is None and we return a functools.partial which is the real
    # decorator that is used and as a result we recursively call dist_init with
    # old_test_method and the rest of the arguments appropriately set.
    if old_test_method is None:
        return partial(
            dist_init,
            setup_rpc=setup_rpc,
            clean_shutdown=clean_shutdown,
            faulty_messages=faulty_messages,
            messages_to_delay=messages_to_delay,
        )

    @wraps(old_test_method)
    def new_test_method(self, *arg, **kwargs):
        # Setting _ignore_rref_leak to make sure OwnerRRefs are properly deleted
        # in tests.
        import torch.distributed.rpc.api as api

        api._ignore_rref_leak = False
        self.worker_id = self.rank
        self.setup_fault_injection(faulty_messages, messages_to_delay)

        rpc_backend_options = self.rpc_backend_options
        if setup_rpc:
            if TEST_WITH_TSAN:
                # TSAN runs much slower.
                rpc_backend_options.rpc_timeout = rpc.constants.DEFAULT_RPC_TIMEOUT_SEC * 5
                rpc.constants.DEFAULT_SHUTDOWN_TIMEOUT = 60

            rpc.init_rpc(
                name=f"worker{self.rank:d}",
                backend=self.rpc_backend,
                rank=self.rank,
                world_size=self.world_size,
                rpc_backend_options=rpc_backend_options,
            )

        return_value = old_test_method(self, *arg, **kwargs)

        if setup_rpc:
            rpc.shutdown(graceful=clean_shutdown)

        return return_value

    return new_test_method

