
def shutdown(graceful=True, timeout=DEFAULT_SHUTDOWN_TIMEOUT):
    r"""
    Perform a shutdown of the RPC agent, and then destroy the RPC agent. This
    stops the local agent from accepting outstanding requests, and shuts
    down the RPC framework by terminating all RPC threads. If ``graceful=True``,
    this will block until all local and remote RPC processes reach this method
    and wait for all outstanding work to complete. Otherwise, if
    ``graceful=False``, this is a local shutdown, and it does not wait for other
    RPC processes to reach this method.

    .. warning::
        For :class:`~torch.futures.Future` objects returned by
        :meth:`~torch.distributed.rpc.rpc_async`, ``future.wait()`` should not
        be called after ``shutdown()``.

    Args:
        graceful (bool): Whether to do a graceful shutdown or not. If True,
                         this will 1) wait until there is no pending system
                         messages for ``UserRRefs`` and delete them; 2) block
                         until all local and remote RPC processes have reached
                         this method and wait for all outstanding work to
                         complete.

    Example::
        Make sure that ``MASTER_ADDR`` and ``MASTER_PORT`` are set properly
        on both workers. Refer to :meth:`~torch.distributed.init_process_group`
        API for more details. For example,

        export MASTER_ADDR=localhost
        export MASTER_PORT=5678

        Then run the following code in two different processes:

        >>> # xdoctest: +SKIP
        >>> # On worker 0:
        >>> import torch
        >>> import torch.distributed.rpc as rpc
        >>> rpc.init_rpc("worker0", rank=0, world_size=2)
        >>> # do some work
        >>> result = rpc.rpc_sync("worker1", torch.add, args=(torch.ones(1), 1))
        >>> # ready to shutdown
        >>> rpc.shutdown()

        >>> # On worker 1:
        >>> import torch.distributed.rpc as rpc
        >>> rpc.init_rpc("worker1", rank=1, world_size=2)
        >>> # wait for worker 0 to finish work, and then shutdown.
        >>> rpc.shutdown()
    """
    if graceful:
        try:
            agent = _get_current_rpc_agent()
            from torch._C._distributed_rpc import TensorPipeAgent

            if not isinstance(agent, TensorPipeAgent) or agent.is_static_group:
                _wait_all_workers(timeout)
                _delete_all_user_and_unforked_owner_rrefs()
                agent.join(shutdown=True, timeout=timeout)
            else:
                # This is a dynamic group so we need to grab the token for the operation
                my_worker_info = agent.get_worker_info()
                my_name = my_worker_info.name
                with _group_membership_management(agent.store, my_name, False):
                    all_worker_infos = agent.get_worker_infos()
                    for worker in all_worker_infos:
                        if worker.name != my_name:
                            rpc_sync(
                                worker.name,
                                _update_group_membership,
                                args=(my_worker_info, [], {}, False),
                            )
                    agent.join(shutdown=True, timeout=timeout)
        finally:
            # In case of errors, continue to complete the local shutdown.
            _finalize_shutdown()
    else:
        _finalize_shutdown()


def shutdown():
  """Shuts down the distributed system.

  Does nothing if the distributed system is not running.
  """
  global_state.shutdown()

