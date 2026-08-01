
def wait():
    """wait() -> Event
    wait for an event
    """
    _ft_init_check()
    return pygame.event.wait()


def wait(future):
    r"""
    Force completion of a `torch.jit.Future[T]` asynchronous task, returning the result of the task.

    .. deprecated:: 2.5
        TorchScript is deprecated, please use ``torch.compile`` instead.

    See :func:`~fork` for docs and examples.
    Args:
        future (torch.jit.Future[T]): an asynchronous task reference, created through `torch.jit.fork`
    Returns:
        `T`: the return value of the completed task
    """
    warnings.warn(
        "`torch.jit.wait` is deprecated. Please use `torch.compile` instead.",
        DeprecationWarning,
    )
    return torch._C.wait(future)


def wait(barrier: _ods_ir.Value[_ods_ir.MemRefType], parity: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> WaitOp:
  return WaitOp(barrier=barrier, parity=parity, loc=loc, ip=ip)


def wait(async_token: _Optional[_ods_ir.Type], async_dependencies: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, WaitOp]:
  op = WaitOp(asyncToken=async_token, asyncDependencies=async_dependencies, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def wait(
    async_dependencies: Optional[List[Value]] = None, *, loc=None, ip=None
) -> Union[Value, List[Value], WaitOp]:
    if async_dependencies is None:
        async_dependencies = []
    return get_op_result_or_op_results(
        WaitOp(gpu_async_token(), async_dependencies, loc=loc, ip=ip)
    )

