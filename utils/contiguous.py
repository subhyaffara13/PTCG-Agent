
def contiguous(
    a: Tensor, *, memory_format: torch.memory_format = torch.contiguous_format
) -> Tensor:
    torch._check(
        memory_format != torch.preserve_format,
        lambda: "preserve memory format is unsupported by the contiguous operator",
    )

    # TODO: make logic consistent with aten contiguous
    if is_contiguous_for_memory_format_or_false(a, memory_format=memory_format):
        return a

    return torch.clone(a, memory_format=memory_format)


def contiguous(g: jit_utils.GraphContext, input, memory_format):
    if memory_format > 2:  # allower values are any, preserve and contiguous_format
        raise errors.SymbolicValueError(
            "onnx memory_format support is not implemented", input
        )
    return input


def contiguous(func, *args, **kwargs):
    if _get_data(args[0]).is_sparse:
        raise ValueError("MaskedTensors with sparse data do not have contiguous")
    return _MaskedContiguous.apply(args[0])

