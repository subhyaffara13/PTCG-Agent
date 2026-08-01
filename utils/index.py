
def index(request):
    """
    Fixture for many "simple" kinds of indices.

    These indices are unlikely to cover corner cases, e.g.
        - no names
        - no NaTs/NaNs
        - no values near implementation bounds
        - ...
    """
    # copy to avoid mutation, e.g. setting .name
    return indices_dict[request.param].copy(deep=False)


def index(x, indices):
    try:
        return index_impl(x, indices, check=True)
    except NotImplementedError:
        # Fallback to ATen for boolean indexing
        x.realize()
        return fallback_handler(aten.index.Tensor, add_to_fallback_set=False)(
            x, indices
        )


def index(
    iterator: Iterator[T], item: T, start: int = 0, end: int | None = None
) -> int:
    from itertools import islice

    for i, elem in islice(enumerate(iterator), start, end):
        if item == elem:
            return i
    # This will not run in dynamo
    raise ValueError(f"{item} is not in {type(iterator)}")


def index(g: jit_utils.GraphContext, self, index):
    if symbolic_helper._is_packed_list(index):
        indices = symbolic_helper._unpack_list(index)
    else:
        indices = [index]

    # Handle single mask index.
    if len(indices) == 1:
        index = indices[0]
        if not symbolic_helper._is_none(index) and (
            symbolic_helper._is_bool(index)
            or _type_utils.JitScalarType.from_value(index)
            == _type_utils.JitScalarType.UINT8
        ):
            index = opset9.nonzero(g, index)
            return g.op("GatherND", self, index)
    return opset9.index(g, self, index)


def index(g: jit_utils.GraphContext, self, index):
    if symbolic_helper._is_packed_list(index):
        indices = symbolic_helper._unpack_list(index)
    else:
        indices = [index]

    def try_mask_to_index(index):
        if not symbolic_helper._is_none(index) and (
            _type_utils.JitScalarType.from_value(
                index, _type_utils.JitScalarType.UNDEFINED
            )
            == _type_utils.JitScalarType.UINT8
            or symbolic_helper._is_bool(index)
        ):
            if g.opset < 9:
                raise errors.SymbolicValueError(
                    "Exporting masked indices are only supported after ONNX opset 9.",
                    self,
                )
            warnings.warn(
                "Exporting aten::index operator with indices of type Byte. "
                "Only 1-D indices are supported. In any other case, "
                "this will produce an incorrect ONNX graph.",
                stacklevel=2,
            )
            index = symbolic_helper._squeeze_helper(g, nonzero(g, index), [1])
        return index

    indices = [try_mask_to_index(idx) for idx in indices]
    if len(indices) == 1:
        return symbolic_helper._select_helper(
            g, self, 0, indices[0], apply_reshape=False
        )
    else:
        # Multiple tensors as indices. Each tensor could either be
        #   1. prim::Constant()
        #           representing ":" in python indexing. E.g. tensor[:, :]
        #   2. prim::Constant[value=...] or tensor output
        #           representing advanced indexing. E.g. tensor[[0, 1], [2, 0]].
        # For more info on advanced indexing,
        # check https://numpy.org/doc/stable/user/basics.indexing.html#advanced-indexing

        # Consider a general case of
        #       t: [x_1, y_1, y_2, ..., x_m, ..., y_n]
        # where t is a tensor of rank m+n, {x_i} are axes where tensor index is provided, and {y_i} are axes for ":".
        # Same results can be achieved through transposing t into
        #       t: [x_1, x_2, ..., x_m, y_1, y_2, ..., y_n]
        # and use gatherND. However ONNX does not have gatherND, to use 1d gather we'll need to flatten t
        # and process the tensor indices.
        #       t: [x_1 * x_2 * ... * x_m, y_1 * y_2 * ... * y_n]
        #       tensor index = \sum_{i=1}^m (ind_i * \prod_{j=i+1}^m (x_j))
        # After gather, reshape and transpose back.
        adv_idx_indices = [
            i for i, idx in enumerate(indices) if not symbolic_helper._is_none(idx)
        ]

        if len(adv_idx_indices) == 0:
            return self
        elif len(adv_idx_indices) == 1:
            return index_select(
                g, self, adv_idx_indices[0], indices[adv_idx_indices[0]]
            )
        else:
            rank = symbolic_helper._get_tensor_rank(self)
            if rank is None:
                return symbolic_helper._unimplemented(
                    "aten::index",
                    "operator of advanced indexing on tensor of unknown rank. ",
                    self,
                )
            # TODO: If indexing is supported natively in ONNX in future opsets,
            #       update the warning to recommend exporting with higher opset version.
            warnings.warn(
                "Exporting aten::index operator of advanced indexing in opset "
                f"{GLOBALS.export_onnx_opset_version}"
                " is achieved by combination of multiple ONNX operators, "
                "including Reshape, Transpose, Concat, and Gather. "
                "If indices include negative values, the exported graph will produce incorrect results.",
                stacklevel=2,
            )
            adv_idx_count = len(adv_idx_indices)
            shape_tensor = _shape_as_tensor(g, self)
            dim_tensor_list = [
                g.op(
                    "Gather",
                    shape_tensor,
                    g.op("Constant", value_t=torch.LongTensor([dim])),
                    axis_i=0,
                )
                for dim in range(rank)
            ]

            self = g.op(
                "Transpose",
                self,
                perm_i=adv_idx_indices
                + [i for i in range(rank) if i not in adv_idx_indices],
            )
            self = g.op("Flatten", self, axis_i=adv_idx_count)

            # Note that tensor indices will be broadcasted while accumulating. Thus we get the final subarray shape as well.
            cum_adv_index = indices[adv_idx_indices[-1]]
            multiplier = dim_tensor_list[adv_idx_indices[-1]]
            for i in range(adv_idx_count - 2, -1, -1):
                adv_index = g.op("Mul", indices[adv_idx_indices[i]], multiplier)
                cum_adv_index = g.op("Add", cum_adv_index, adv_index)
                multiplier = g.op(
                    "Mul", multiplier, dim_tensor_list[adv_idx_indices[i]]
                )

            # perform gather
            self = index_select(g, self, 0, cum_adv_index)

            cum_adv_index_shape_tensor = _shape_as_tensor(g, cum_adv_index)
            # check if all advanced indices are consecutive.
            # Refer to https://numpy.org/doc/stable/user/basics.indexing.html#combining-advanced-and-basic-indexing
            # to understand how the subarray position is decided.
            if adv_idx_indices == list(
                range(adv_idx_indices[0], adv_idx_indices[-1] + 1)
            ):
                # unfold regular index axes
                folded_adv_idx_shape_list = [
                    g.op("Constant", value_t=torch.LongTensor([-1]))
                ] + [
                    dim_tensor_list[i] for i in range(rank) if i not in adv_idx_indices
                ]
                folded_adv_idx_shape = g.op(
                    "Concat", *folded_adv_idx_shape_list, axis_i=0
                )
                self = symbolic_helper._reshape_helper(g, self, folded_adv_idx_shape)

                # Transpose folded advanced indexed axis to its original location.
                adv_idx_permute = (
                    list(range(1, adv_idx_indices[0] + 1))
                    + [0]
                    + list(range(adv_idx_indices[0] + 1, rank - adv_idx_count + 1))
                )
                self = g.op("Transpose", self, perm_i=adv_idx_permute)

                # unfold advanced index axes
                final_shape_list = (
                    [dim_tensor_list[i] for i in range(adv_idx_indices[0])]
                    + [cum_adv_index_shape_tensor]
                    + [
                        dim_tensor_list[i]
                        for i in range(adv_idx_indices[0], rank)
                        if i not in adv_idx_indices
                    ]
                )
                final_shape = g.op("Concat", *final_shape_list, axis_i=0)
            else:
                final_shape = g.op(
                    "Concat",
                    cum_adv_index_shape_tensor,
                    *[
                        dim_tensor_list[i]
                        for i in range(rank)
                        if i not in adv_idx_indices
                    ],
                    axis_i=0,
                )

            return symbolic_helper._reshape_helper(g, self, final_shape)


def index(it, ind):
    """ Fancy indexing into an indexable iterable (tuple, list).

    Examples
    ========

    >>> from sympy.unify.core import index
    >>> index([10, 20, 30], (1, 2, 0))
    [20, 30, 10]
    """
    return type(it)([it[i] for i in ind])


def index():
    index = date_range(datetime(2005, 1, 1), datetime(2005, 1, 10), freq="D", unit="ns")
    index.name = "date"
    return index


def index(request):
    return request.param


def index(a, sub, start=0, end=None):
    """
    Like `find`, but raises :exc:`ValueError` when the substring is not found.

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype

    sub : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype

    start, end : array_like, with any integer dtype, optional

    Returns
    -------
    out : ndarray
        Output array of ints.

    See Also
    --------
    find, str.index

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array(["Computer Science"])
    >>> np.strings.index(a, "Science", start=0, end=None)
    array([9])

    """
    end = end if end is not None else MAX
    return _index_ufunc(a, sub, start, end)


def index(self: Any, positions: Any, dims: Any) -> _Tensor:
    """
    Index a regular tensor by binding specified positions to dims.

    This converts a regular tensor to a first-class tensor by binding
    the specified positional dimensions to Dim objects.

    Args:
        positions: Tuple of dimension positions to bind
        dims: Dim objects or tuple of Dim objects to bind to

    Returns:
        First-class tensor with specified dimensions bound
    """
    # If this is already a first-class tensor (_Tensor), call its index method directly
    if isinstance(self, _Tensor):
        return _Tensor.index(self, positions, dims)

    # Convert regular tensor to first-class tensor
    info = TensorInfo.create(self, ensure_batched=False, ensure_present=False)

    # Create the first-class tensor
    if info.tensor is None:
        raise AssertionError("Cannot index None tensor")
    result = Tensor.from_positional(info.tensor, info.levels, info.has_device)

    # Now call the index method on the first-class tensor
    # Cast result to _Tensor for the method call
    return _Tensor.index(result, positions, dims)  # type: ignore[arg-type]

