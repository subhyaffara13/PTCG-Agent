
def pop_on_exit(stack: list[tuple[T, T]], left: T, right: T) -> Iterator[None]:
    stack.append((left, right))
    yield
    stack.pop()

