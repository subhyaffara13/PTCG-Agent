
def inline_everything_mode(should_inline):
    old = torch._C._jit_get_inline_everything_mode()
    torch._C._jit_set_inline_everything_mode(should_inline)
    try:
        yield
    finally:
        torch._C._jit_set_inline_everything_mode(old)

