
def iter_tensors(
    args: tuple[Any], kwargs: dict[str, Any], allowed_nesting: int = 1
) -> Iterator[torch.Tensor]:
    def check(arg):
        if isinstance(arg, torch.Tensor):
            yield arg
        elif allowed_nesting > 0 and isinstance(arg, (tuple, list)):
            yield from iter_tensors(tuple(arg), {}, allowed_nesting - 1)

    for arg in args:
        yield from check(arg)
    for kwarg in kwargs.values():
        yield from check(kwarg)

