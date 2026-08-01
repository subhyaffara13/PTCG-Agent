
def _disable_jit_autocast() -> Generator[None, None, None]:
    # pyrefly: ignore [missing-attribute]
    old_jit_autocast_flag = torch._C._jit_set_autocast_mode(False)
    try:
        yield
    finally:
        # pyrefly: ignore [missing-attribute]
        torch._C._jit_set_autocast_mode(old_jit_autocast_flag)

