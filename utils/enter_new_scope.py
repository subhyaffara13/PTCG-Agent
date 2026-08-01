
def enter_new_scope() -> Generator[None, None, None]:
    global _current_scope_id
    try:
        _current_scope_id.value = current_scope_id() + 1
        yield
    finally:
        _current_scope_id.value = current_scope_id() - 1

