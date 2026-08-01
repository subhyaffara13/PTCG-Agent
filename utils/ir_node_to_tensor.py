
def ir_node_to_tensor(x: None, replace_symbols_with_hints: bool = False) -> None: ...


def ir_node_to_tensor(
    x: IRNode, replace_symbols_with_hints: bool = False
) -> torch.Tensor: ...


def ir_node_to_tensor(
    x: IRNode | None, replace_symbols_with_hints: bool = False
) -> torch.Tensor | None:
    # When replace_symbols_with_hints=False (default), sizes/strides remain as
    # symbolic expressions, so downstream operations on the resulting tensor (e.g.,
    # shape comparisons inside a kernel's meta function) may install guards. When
    # True, symbolic expressions are replaced with concrete integer hints via
    # size_hint, preventing any downstream guards.
    if x is None:
        return None

    shape_fn: Callable[[int | Expr], int | Expr]
    if replace_symbols_with_hints:
        shape_fn = V.graph.sizevars.optimization_hint
    else:
        shape_fn = identity
    size = [shape_fn(s) for s in x.get_size()]
    stride: StrideType
    if is_storage_and_layout(x):
        stride = [shape_fn(s) for s in x.get_layout().stride]
    else:
        stride = FlexibleLayout.contiguous_strides(size)
    dtype = x.get_dtype()
    device = x.get_device()
    size = convert_shape_to_symint(size)
    # pyrefly: ignore [bad-assignment]
    stride = convert_shape_to_symint(stride)
    with V.graph.sizevars.shape_env.suppress_guards():
        t = torch.empty_strided(
            size=size, stride=stride, dtype=dtype, device=device
        ).zero_()
    return t

