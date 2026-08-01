
def reset_name_stack() -> Generator[None, None, None]:
  with set_name_stack(NameStack()):
    yield

