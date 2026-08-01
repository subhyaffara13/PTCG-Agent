
def temporarily_pop_interpreter_stack() -> Generator[None, None, None]:
    try:
        saved = pop_dynamic_layer_stack()
        yield
    finally:
        push_dynamic_layer_stack(saved)

