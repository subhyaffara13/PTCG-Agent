
def in_kernel_invocation_manager(
    fake_mode: FakeTensorMode,
) -> Generator[None, None, None]:
    # See: note [Fake Tensor Dispatch Keys]
    prev_in_kernel = fake_mode.in_kernel_invocation
    meta_in_tls = torch._C._meta_in_tls_dispatch_include()
    if meta_in_tls != prev_in_kernel:
        raise AssertionError(f"{meta_in_tls}, {prev_in_kernel}")

    with torch._C._DisableTorchDispatch():
        fake_mode.in_kernel_invocation = True
        # Unfortunately _set_meta_in_tls_dispatch_include(False) can leave
        # `Dense` turned on (because it's implied by `Meta`)
        with torch._C._PreserveDispatchKeyGuard():
            torch._C._set_meta_in_tls_dispatch_include(True)
            try:
                yield
            finally:
                fake_mode.in_kernel_invocation = prev_in_kernel

