
def grad_increment_nesting() -> Generator[int, None, None]:
    try:
        grad_level = _grad_increment_nesting()
        yield grad_level
    finally:
        _grad_decrement_nesting()

