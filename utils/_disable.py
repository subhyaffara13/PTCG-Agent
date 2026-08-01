
def _disable() -> Generator[None, None, None]:
    (
        prior_compiler,
        prior_dynamic,
    ) = torch._C._dynamo.compiled_autograd.set_autograd_compiler(None, False)
    global compiled_autograd_enabled
    compiled_autograd_enabled = False
    global active_disable_ctx
    if not active_disable_ctx:
        active_disable_ctx = True
    try:
        yield
    finally:
        if prior_compiler:
            compiled_autograd_enabled = True
        active_disable_ctx = False
        torch._C._dynamo.compiled_autograd.set_autograd_compiler(
            prior_compiler, prior_dynamic
        )

