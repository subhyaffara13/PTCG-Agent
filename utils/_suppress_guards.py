
def _suppress_guards(shape_env: ShapeEnv) -> Generator[None, None, None]:
    shape_env._suppress_guards_enter()
    try:
        yield
    finally:
        shape_env._suppress_guards_exit()

