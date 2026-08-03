from typing import Optional

def slice(
    self: list[int], dim: int, start: Optional[int], end: Optional[int], step: int
):
    ndim = len(self)
    if ndim == 0:
        raise AssertionError("Cannot slice a 0-dimensional tensor")
    dim = maybe_wrap_dim(dim, ndim)
    start_val = start if start is not None else 0
    end_val = end if end is not None else max_int()
    if step <= 0:
        raise AssertionError(f"Expected step > 0, but got {step}")
    if start_val == max_int():
        start_val = 0
    if start_val < 0:
        start_val += self[dim]
    if end_val < 0:
        end_val += self[dim]
    if start_val < 0:
        start_val = 0
    elif start_val > self[dim]:
        start_val = self[dim]
    if end_val < start_val:
        end_val = start_val
    elif end_val >= self[dim]:
        end_val = self[dim]
    slice_len = end_val - start_val
    out = _copy(self)
    out[dim] = (slice_len + step - 1) // step
    return out


def slice(g: jit_utils.GraphContext, self, *args):
    if len(args) == 4:
        # aten::slice(Tensor self, int dim, int? start=None, int? end=None, int step=1) -> Tensor
        dims, start, end, step = args
    elif len(args) == 3:
        # aten::slice(t[] l, int? start=None, int? end=None, int step=1) -> t[]
        start, end, step = args
        dims = [0]
    else:
        raise errors.SymbolicValueError("Unknown aten::slice signature", self)

    return symbolic_helper._slice_helper(
        g,
        self,
        axes=dims,
        starts=start,
        ends=end,
        steps=step,
    )


def slice(g: jit_utils.GraphContext, self, *args):
    if len(args) == 4:
        # aten::slice(Tensor self, int dim, int start, int end, int step) -> Tensor
        dim, start, end, step = args
        step = symbolic_helper._parse_arg(step, "i")
        if step != 1:
            raise errors.SymbolicValueError("step!=1 is currently not supported", self)
        is_start_none = start.node().kind() == "prim::Constant" and isinstance(
            start.type(), _C.NoneType
        )
        is_end_none = end.node().kind() == "prim::Constant" and isinstance(
            end.type(), _C.NoneType
        )
        is_start_onnx_const = start.node().kind() == "onnx::Constant"
        is_end_onnx_const = end.node().kind() == "onnx::Constant"
        if (
            ((not is_start_none) and (not is_start_onnx_const))
            or ((not is_end_none) and (not is_end_onnx_const))
            or dim.node().kind() != "onnx::Constant"
        ):
            if GLOBALS.operator_export_type == _C_onnx.OperatorExportTypes.ONNX:
                raise errors.SymbolicValueError(
                    "Unsupported: ONNX export of Slice with dynamic inputs. DynamicSlice "
                    "is a deprecated experimental op. Please use statically allocated "
                    "variables or export to a higher opset version.",
                    self,
                )
            else:
                start_unsqueezed = symbolic_helper._unsqueeze_helper(g, start, [0])
                end_unsqueezed = symbolic_helper._unsqueeze_helper(g, end, [0])
                dim_unsqueezed = symbolic_helper._unsqueeze_helper(g, dim, [0])
                return g.op(
                    "DynamicSlice",
                    self,
                    start_unsqueezed,
                    end_unsqueezed,
                    dim_unsqueezed,
                )
        else:
            start = 0 if is_start_none else symbolic_helper._parse_arg(start, "i")
            end = (
                _constants.INT64_MAX
                if is_end_none
                else symbolic_helper._parse_arg(end, "i")
            )
            dim = symbolic_helper._parse_arg(dim, "i")
            return symbolic_helper._slice_helper(
                g, self, axes=[dim], starts=[start], ends=[end]
            )
    elif len(args) == 3:
        # aten::slice(t[] l, int start, int end, int step) -> t[]
        start, end, step = args
        dim = 0
        is_start_none = start.node().kind() == "prim::Constant" and isinstance(
            start.type(), _C.NoneType
        )
        is_end_none = end.node().kind() == "prim::Constant" and isinstance(
            end.type(), _C.NoneType
        )
        start = 0 if is_start_none else symbolic_helper._parse_arg(start, "i")
        end = (
            _constants.INT64_MAX
            if is_end_none
            else symbolic_helper._parse_arg(end, "i")
        )
        return symbolic_helper._slice_helper(
            g, self, axes=[dim], starts=[start], ends=[end]
        )

    return symbolic_helper._unimplemented("aten::slice", f"with {len(args)} arguments")


def slice(a, start=None, stop=np._NoValue, step=None, /):
    """
    Slice the strings in `a` by slices specified by `start`, `stop`, `step`.
    Like in the regular Python `slice` object, if only `start` is
    specified then it is interpreted as the `stop`.

    Parameters
    ----------
    a : array-like, with ``StringDType``, ``bytes_``, or ``str_`` dtype
        Input array

    start : None, an integer or an array of integers
        The start of the slice, broadcasted to `a`'s shape

    stop : None, an integer or an array of integers
        The end of the slice, broadcasted to `a`'s shape

    step : None, an integer or an array of integers
        The step for the slice, broadcasted to `a`'s shape

    Returns
    -------
    out : ndarray
        Output array of ``StringDType``, ``bytes_`` or ``str_`` dtype,
        depending on input type

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array(['hello', 'world'])
    >>> np.strings.slice(a, 2)
    array(['he', 'wo'], dtype='<U5')

    >>> np.strings.slice(a, 2, None)
    array(['llo', 'rld'], dtype='<U5')

    >>> np.strings.slice(a, 1, 5, 2)
    array(['el', 'ol'], dtype='<U5')

    One can specify different start/stop/step for different array entries:

    >>> np.strings.slice(a, np.array([1, 2]), np.array([4, 5]))
    array(['ell', 'rld'], dtype='<U5')

    Negative slices have the same meaning as in regular Python:

    >>> b = np.array(['hello world', 'γεια σου κόσμε', '你好世界', '👋 🌍'],
    ...              dtype=np.dtypes.StringDType())
    >>> np.strings.slice(b, -2)
    array(['hello wor', 'γεια σου κόσ', '你好', '👋'], dtype=StringDType())

    >>> np.strings.slice(b, -2, None)
    array(['ld', 'με', '世界', ' 🌍'], dtype=StringDType())

    >>> np.strings.slice(b, [3, -10, 2, -3], [-1, -2, -1, 3])
    array(['lo worl', ' σου κόσ', '世', '👋 🌍'], dtype=StringDType())

    >>> np.strings.slice(b, None, None, -1)
    array(['dlrow olleh', 'εμσόκ υοσ αιεγ', '界世好你', '🌍 👋'],
          dtype=StringDType())

    """
    # Just like in the construction of a regular slice object, if only start
    # is specified then start will become stop, see logic in slice_new.
    if stop is np._NoValue:
        stop = start
        start = None

    # adjust start, stop, step to be integers, see logic in PySlice_Unpack
    if step is None:
        step = 1
    step = np.asanyarray(step)
    if not np.issubdtype(step.dtype, np.integer):
        raise TypeError(f"unsupported type {step.dtype} for operand 'step'")
    if np.any(step == 0):
        raise ValueError("slice step cannot be zero")

    if start is None:
        start = np.where(step < 0, np.iinfo(np.intp).max, 0)

    if stop is None:
        stop = np.where(step < 0, np.iinfo(np.intp).min, np.iinfo(np.intp).max)

    return _slice(a, start, stop, step)


def slice(operand: _ods_ir.Value[_ods_ir.RankedTensorType], start_indices: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], limit_indices: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], strides: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SliceOp(operand=operand, start_indices=start_indices, limit_indices=limit_indices, strides=strides, results=results, loc=loc, ip=ip).result


def slice(operand: _ods_ir.Value[_ods_ir.RankedTensorType], start_indices: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], limit_indices: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], strides: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return SliceOp(operand=operand, start_indices=start_indices, limit_indices=limit_indices, strides=strides, results=results, loc=loc, ip=ip).result


def slice(operand, start_indices, limit_indices, strides=None):
  if strides is None:
    strides = np.ones(len(start_indices)).astype(int)
  slices = tuple(_map(_slice, start_indices, limit_indices, strides))
  return operand[slices]


def slice(operand: ArrayLike, start_indices: Sequence[int],
          limit_indices: Sequence[int],
          strides: Sequence[int] | None = None) -> Array:
  """Wraps XLA's `Slice
  <https://www.openxla.org/xla/operation_semantics#slice>`_
  operator.

  Args:
    operand: an array to slice
    start_indices: a sequence of ``operand.ndim`` start indices.
    limit_indices: a sequence of ``operand.ndim`` limit indices.
    strides: an optional sequence of ``operand.ndim`` strides.

  Returns:
    The sliced array

  Examples:
    Here are some examples of simple two-dimensional slices:

    >>> x = jnp.arange(12).reshape(3, 4)
    >>> x
    Array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11]], dtype=int32)

    >>> lax.slice(x, (1, 0), (3, 2))
    Array([[4, 5],
           [8, 9]], dtype=int32)

    >>> lax.slice(x, (0, 0), (3, 4), (1, 2))
    Array([[ 0,  2],
           [ 4,  6],
           [ 8, 10]], dtype=int32)

    These two examples are equivalent to the following Python slicing syntax:

    >>> x[1:3, 0:2]
    Array([[4, 5],
           [8, 9]], dtype=int32)

    >>> x[0:3, 0:4:2]
    Array([[ 0,  2],
           [ 4,  6],
           [ 8, 10]], dtype=int32)

  See Also:
    - :attr:`jax.numpy.ndarray.at`
    - :func:`jax.lax.slice_in_dim`
    - :func:`jax.lax.index_in_dim`
    - :func:`jax.lax.dynamic_slice`
  """
  return slice_p.bind(operand, start_indices=tuple(start_indices),
                      limit_indices=tuple(limit_indices),
                      strides=None if strides is None else tuple(strides))

