
def set_enable_dynamic(enable: bool) -> Generator[None, None, None]:
    cleanup = make_set_enable_dynamic(enable)()
    try:
        yield
    finally:
        cleanup()

