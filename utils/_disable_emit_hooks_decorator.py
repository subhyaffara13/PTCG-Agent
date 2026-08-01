
def _disable_emit_hooks_decorator(_DecoratorContextManager) -> None:  # noqa: F811
    # noqa: F841
    def __enter__(self) -> None:
        self.hooks = torch._C._jit_get_emit_hooks()
        torch._C._jit_set_emit_hooks(None, None)

    def __exit__(self, *args) -> None:
        torch._C._jit_set_emit_hooks(self.hooks[0], self.hooks[1])

