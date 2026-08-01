
def _assert_functionalize_not_active(msg: str) -> None:
    is_included = torch._C._dispatch_tls_is_dispatch_key_included(
        torch._C.DispatchKey.Functionalize
    )
    is_excluded = torch._C._dispatch_tls_is_dispatch_key_excluded(
        torch._C.DispatchKey.Functionalize
    )
    if not is_excluded and is_included:
        raise AssertionError(msg)

