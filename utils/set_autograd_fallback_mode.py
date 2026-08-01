
def set_autograd_fallback_mode(mode):
    prev = torch._C._get_autograd_fallback_mode()
    try:
        torch._C._set_autograd_fallback_mode(mode)
        yield
    finally:
        torch._C._set_autograd_fallback_mode(prev)

