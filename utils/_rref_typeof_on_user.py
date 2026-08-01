
def _rref_typeof_on_user(
    rref, timeout: float = UNSET_RPC_TIMEOUT, blocking: bool = True
):
    fut = rpc_async(rref.owner(), _rref_typeof_on_owner, args=(rref,), timeout=timeout)
    if blocking:
        return fut.wait()
    else:
        return fut

