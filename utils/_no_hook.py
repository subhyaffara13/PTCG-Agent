
def _no_hook(module: nn.Module, user_ctx: AbstractContextManager | None = None):
    r"""
    Disable hooks installed by checkpoint to avoid unintentional recursion
    during backward recomputation.
    """

    with user_ctx if user_ctx else nullcontext():
        orig_enable_hook = checkpoint.state(module).enable_hook
        checkpoint.state(module).enable_hook = False
        try:
            yield
        finally:
            checkpoint.state(module).enable_hook = orig_enable_hook

