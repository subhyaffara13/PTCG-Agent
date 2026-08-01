
def masked_select(tensor: Tensor, mask: Tensor) -> Tensor:
    r"""
    Constructs a nested tensor given a strided tensor input and a strided mask, the resulting jagged layout nested tensor
    will have values retain values where the mask is equal to True. The dimensionality of the mask is preserved and is
    represented with the offsets, this is unlike :func:`masked_select` where the output is collapsed to a 1D tensor.

    Args:
    tensor (:class:`torch.Tensor`): a strided tensor from which the jagged layout nested tensor is constructed from.
    mask (:class:`torch.Tensor`): a strided mask tensor which is applied to the tensor input

    Example::

        >>> tensor = torch.randn(3, 3)
        >>> mask = torch.tensor([[False, False, True], [True, False, True], [False, False, True]])
        >>> nt = torch.nested.masked_select(tensor, mask)
        >>> nt.shape
        torch.Size([3, j4])
        >>> # Length of each item in the batch:
        >>> nt.offsets().diff()
        tensor([1, 2, 1])

        >>> tensor = torch.randn(6, 5)
        >>> mask = torch.tensor([False])
        >>> nt = torch.nested.masked_select(tensor, mask)
        >>> nt.shape
        torch.Size([6, j5])
        >>> # Length of each item in the batch:
        >>> nt.offsets().diff()
        tensor([0, 0, 0, 0, 0, 0])
    """
    if tensor.layout != torch.strided:
        raise RuntimeError(
            f"torch.nested.masked_select requires a strided tensor, given {tensor.layout}"
        )

    if mask.layout != torch.strided:
        raise RuntimeError(
            f"torch.nested.masked_select requires a strided mask, given: {mask.layout}"
        )
    res_values = tensor.masked_select(mask)
    expanded_mask = mask.expand(tensor.shape)
    res_lengths = expanded_mask.sum(dim=tensor.ndim - 1).view(-1)

    from torch.nested._internal.nested_tensor import nested_view_from_values_offsets

    return nested_view_from_values_offsets(
        values=res_values,
        offsets=F.pad(res_lengths.cumsum(dim=0), (1, 0)),
    )


def masked_select(
    fake_mode: FakeTensorMode, func: OpOverload, self: FakeTensor, mask: FakeTensor
) -> FakeTensor:
    if (
        fake_mode.shape_env is None
        or not fake_mode.shape_env.allow_dynamic_output_shape_ops
    ):
        # Without symints/symfloats, cannot handle this
        raise DynamicOutputShapeException(func)

    nnz = fake_mode.shape_env.create_unbacked_symint()

    # see nonzero for commentary
    maxval = sys.maxsize - 1

    # Avoid importing sympy at a module level
    from torch.fx.experimental.symbolic_shapes import (
        _constrain_range_for_size,
        has_free_symbols,
    )
    from torch.utils._sympy.numbers import IntInfinity
    from torch.utils._sympy.value_ranges import bound_sympy

    # If num elements is expressed symbolically, calculate
    # the concrete value based on upper bounds. Otherwise,
    # we can set max val directly.
    if not has_free_symbols(self.numel()):
        num_elements = int(self.numel())
    else:
        prod_node = math.prod(self.shape).node  # type: ignore[union-attr]
        prod_range = bound_sympy(prod_node.expr, prod_node.shape_env.var_to_range)
        if isinstance(prod_range.upper, IntInfinity):
            num_elements = sys.maxsize - 1
        else:
            num_elements = prod_range.upper
    if num_elements > 2:
        maxval = num_elements

    _constrain_range_for_size(nnz, max=maxval)

    return self.new_empty((nnz,))  # type: ignore[return]


def masked_select(g: jit_utils.GraphContext, self, mask):
    index = opset9.nonzero(g, opset9.expand_as(g, mask, self))
    return g.op("GatherND", self, index)

