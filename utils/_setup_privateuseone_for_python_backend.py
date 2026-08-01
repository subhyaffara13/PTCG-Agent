
def _setup_privateuseone_for_python_backend(
    rename=None, backend_module=None, hook=None, device_guard=None
) -> None:
    """This function will prepare the PrivateUse1 dispatch key to be used as a python backend.

    WARNING: this API is experimental and might change without notice.

    Formally, this registers things that Pytorch expects a registered backend
    in C++ to have: including device guards, hooks, and backend modules and what not.

    after this call, one can use `torch.library` to write Ops for this dispatch key
    and expect it to behave like a backend registered in C++.

    See the unit test at test/test_privateuseone_python_backend.py for more details.

    Args:
        rename: str | None, if passed in, we will rename privateuseone backend to
           the name given.
        backend_module: object | None, if passed in None, we will use DummyBackendModule
        hook: object | None, if passed in None, we will use DummyPrivateUse1Hook
        device_guard: object | None, if passed in None, we will use DummyDeviceGuard
    """
    # NOTE: the ordering of which these functions are called is important.
    if rename is not None:
        torch.utils.rename_privateuse1_backend(rename)
    else:
        rename = "privateuseone"
    torch.utils.generate_methods_for_privateuse1_backend()
    if backend_module is None:
        backend_module = _DummyBackendModule()
    if hook is None:
        hook = _DummyPrivateUse1Hook()
    if device_guard is None:
        device_guard = _DummyDeviceGuard()
    torch._register_device_module(rename, backend_module)
    torch._C._acc.register_python_privateuseone_hook(hook)
    torch._C._acc.register_python_privateuseone_device_guard(device_guard)

