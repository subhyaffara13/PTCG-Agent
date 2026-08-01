
def nested_tensor_from_jagged(
    values: Tensor,
    offsets: Tensor | None = None,
    lengths: Tensor | None = None,
    jagged_dim: int | None = None,
    min_seqlen: int | None = None,
    max_seqlen: int | None = None,
) -> Tensor:
    r"""
    Constructs a jagged layout nested tensor from the given jagged components. The jagged layout
    consists of a required values buffer with the jagged dimension packed into a single dimension.
    The offsets / lengths metadata determines how this dimension is split into batch elements
    and are expected to be allocated on the same device as the values buffer.

    Expected metadata formats:
        * offsets: Indices within the packed dimension splitting it into heterogeneously-sized
          batch elements. Example: [0, 2, 3, 6] indicates that a packed jagged dim of size 6
          should be conceptually split into batch elements of length [2, 1, 3]. Note that both the
          beginning and ending offsets are required for kernel convenience (i.e. shape batch_size + 1).
        * lengths: Lengths of the individual batch elements; shape == batch_size. Example: [2, 1, 3]
          indicates that a packed jagged dim of size 6 should be conceptually split into batch
          elements of length [2, 1, 3].

    Note that it can be useful to provide both offsets and lengths. This describes a nested tensor
    with "holes", where the offsets indicate the start position of each batch item and the length
    specifies the total number of elements (see example below).

    The returned jagged layout nested tensor will be a view of the input values tensor.

    Args:
        values (:class:`torch.Tensor`): The underlying buffer in the shape of
            (sum_B(*), D_1, ..., D_N). The jagged dimension is packed into a single dimension,
            with the offsets / lengths metadata used to distinguish batch elements.
        offsets (optional :class:`torch.Tensor`): Offsets into the jagged dimension of shape B + 1.
        lengths (optional :class:`torch.Tensor`): Lengths of the batch elements of shape B.
        jagged_dim (optional int): Indicates which dimension in values is the packed jagged
            dimension. Must be >= 1 as the batch dimension (dim=0) cannot be ragged.
            If None, this is set to dim=1 (i.e. the dimension immediately following the batch dimension). Default: None
        min_seqlen (optional int): If set, uses the specified value as the cached minimum sequence
            length for the returned nested tensor. This can be a useful alternative to computing
            this value on-demand, possibly avoiding a GPU -> CPU sync. Default: None
        max_seqlen (optional int): If set, uses the specified value as the cached maximum sequence
            length for the returned nested tensor. This can be a useful alternative to computing
            this value on-demand, possibly avoiding a GPU -> CPU sync. Default: None

    Example::

        >>> values = torch.randn(12, 5)
        >>> offsets = torch.tensor([0, 3, 5, 6, 10, 12])
        >>> nt = nested_tensor_from_jagged(values, offsets)
        >>> # 3D shape with the middle dimension jagged
        >>> nt.shape
        torch.Size([5, j2, 5])
        >>> # Length of each item in the batch:
        >>> offsets.diff()
        tensor([3, 2, 1, 4, 2])

        >>> values = torch.randn(6, 5)
        >>> offsets = torch.tensor([0, 2, 3, 6])
        >>> lengths = torch.tensor([1, 1, 2])
        >>> # NT with holes
        >>> nt = nested_tensor_from_jagged(values, offsets, lengths)
        >>> a, b, c = nt.unbind()
        >>> # Batch item 1 consists of indices [0, 1)
        >>> torch.equal(a, values[0:1, :])
        True
        >>> # Batch item 2 consists of indices [2, 3)
        >>> torch.equal(b, values[2:3, :])
        True
        >>> # Batch item 3 consists of indices [3, 5)
        >>> torch.equal(c, values[3:5, :])
        True
    """
    from torch.fx._symbolic_trace import is_fx_tracing

    if is_fx_tracing():
        raise RuntimeError(
            "torch.nested.nested_tensor_from_jagged does not support tracing with fx.symbolic_trace. "
            "Use fx.wrap to wrap the function that calls nested_tensor_from_jagged."
        )

    if offsets is None:
        if lengths is None:
            raise RuntimeError(
                "nested_tensor_from_jagged(): At least one of offsets or lengths is required."
            )
        else:
            # TODO: Truly support offsets=None at some point?
            # For now, just convert lengths -> offsets for kernel convenience
            offsets = F.pad(lengths.cumsum(0), (1, 0))
            lengths = None

    if jagged_dim is None:
        jagged_dim = 1
    elif jagged_dim < 1:
        raise ValueError(f"Expected jagged_dim >=1, but got {jagged_dim}.")

    from torch.nested._internal.nested_tensor import (
        nested_view_from_values_offsets_lengths,
    )

    return nested_view_from_values_offsets_lengths(
        values,
        offsets,
        lengths,
        ragged_idx=jagged_dim,
        min_seqlen=min_seqlen,
        max_seqlen=max_seqlen,
    )

