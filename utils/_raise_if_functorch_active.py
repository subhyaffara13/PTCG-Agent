
def _raise_if_functorch_active() -> None:
    # not ideal but prevent the user from seeing a nasty traceback - See #138422
    stack = torch._C._functorch.peek_interpreter_stack()
    torch._check(
        stack is None,
        lambda: (
            "It looks like you're trying to call a compiled backward function within vmap/grad/vjp, "
            "which isn't supported. Try wrapping vmap inside torch.compile, or skip compiling the "
            "backward function."
        ),
    )

