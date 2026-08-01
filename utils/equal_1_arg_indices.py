
def equal_1_arg_indices(
    args: list[KernelArgType],
    *,
    indices: list[int] | None = None,
) -> tuple[int, ...]:
    if indices is None:
        indices = list(range(len(args)))

    equal_to_1 = tuple(i for i, arg in zip(indices, args) if _arg_equals_1(arg))

    return equal_to_1

