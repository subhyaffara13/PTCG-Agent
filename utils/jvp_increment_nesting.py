
def jvp_increment_nesting() -> Generator[int, None, None]:
    try:
        yield enter_jvp_nesting()
    finally:
        exit_jvp_nesting()

