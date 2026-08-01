
def enable_inplace_requires_grad(enabled: bool) -> Generator[None, None, None]:
    prev_state = get_inplace_requires_grad_allowed()
    set_inplace_requires_grad_allowed(enabled)
    try:
        yield
    finally:
        set_inplace_requires_grad_allowed(prev_state)

