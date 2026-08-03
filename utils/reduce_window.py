from typing import Any, Callable

def reduce_window(result: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], init_values: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], window_dimensions: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, window_strides: _Optional[_Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr]] = None, base_dilations: _Optional[_Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr]] = None, window_dilations: _Optional[_Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr]] = None, padding: _Optional[_Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ReduceWindowOp]:
  op = ReduceWindowOp(result=result, inputs=inputs, init_values=init_values, window_dimensions=window_dimensions, window_strides=window_strides, base_dilations=base_dilations, window_dilations=window_dilations, padding=padding, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def reduce_window(result: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], init_values: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], window_dimensions: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, window_strides: _Optional[_Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr]] = None, base_dilations: _Optional[_Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr]] = None, window_dilations: _Optional[_Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr]] = None, padding: _Optional[_Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ReduceWindowOp]:
  op = ReduceWindowOp(result=result, inputs=inputs, init_values=init_values, window_dimensions=window_dimensions, window_strides=window_strides, base_dilations=base_dilations, window_dilations=window_dilations, padding=padding, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def reduce_window(operand, init_value, computation, window_dimensions,
                  window_strides, padding, base_dilation):
  op, dims, strides = operand, window_dimensions, window_strides
  if isinstance(padding, str):
    pads = padtype_to_pads(op.shape, dims, strides, padding)
  else:
    pads = padding
  op = op.reshape((1, 1) + op.shape)
  if base_dilation:
    op = _dilate(op, base_dilation, init_value)
  view = _conv_view(op, (1, 1) + dims, strides, pads,
                    pad_value=init_value)[0]
  view = view.reshape(view.shape[1:1+len(dims)] + (-1,))
  reducer = _make_reducer(computation, init_value)
  return reducer(view, axis=-1)


def reduce_window(
    ctx: LoweringRuleContext,
    *,
    # Base name to be used for the reducer function
    reducer_name: str,
    # Compute the reducer body given the reducer.
    reducer_body: Callable[[ir.Block], Sequence[ir.Value]],
    operands: Sequence[ir.Value],
    init_values: Sequence[ir.Value],
    init_values_avals: Sequence[core.AbstractValue],
    out_avals: Sequence[core.AbstractValue],
    window_dimensions, window_strides, padding, base_dilation, window_dilation):
  """Builds a ReduceWindowOp, with support for dynamic shapes."""

  scalar_types, _ = ir_tree_registry.flatten(map(partial(_aval_to_ir_types, ctx.module_context), init_values_avals))
  flat_result_types, _ = ir_tree_registry.flatten(map(partial(_aval_to_ir_types, ctx.module_context), out_avals))
  if any(not core.is_constant_shape(s)
         for s in [window_dimensions, window_dilation, window_strides, base_dilation, *padding]):
    # d_padding will be an array i32[N, 2] with pad_lo and pad_hi for each
    # spatial dimension.
    int2d = aval_to_ir_type(ctx.module_context, core.ShapedArray((1, 2), np.int32))
    def prep_one_pad(pad_lo_hi: tuple[core.DimSize, core.DimSize]):
      pads = eval_dynamic_shape_as_tensor(ctx, pad_lo_hi)  # i32[2]
      return hlo.reshape(int2d, pads)
    d_padding = hlo.concatenate(list(map(prep_one_pad, padding)), i64_attr(0))
    # Build the reducer
    reducer_type = ir.FunctionType.get(
      scalar_types + scalar_types, scalar_types)
    with ir.InsertionPoint.at_block_begin(ctx.module_context.module.body):
      reducer = func_dialect.FuncOp(reducer_name, reducer_type)
    ctx.module_context.symbol_table.insert(reducer)
    entry_block = reducer.add_entry_block()
    with ir.InsertionPoint(entry_block):
      hlo.return_(reducer_body(entry_block))

    rw = custom_call(
      "stablehlo.dynamic_reduce_window",
      result_types=flat_result_types,
      operands=[
        *operands, *init_values,
        eval_dynamic_shape_as_tensor(ctx, window_dimensions),
        eval_dynamic_shape_as_tensor(ctx, window_strides),
        eval_dynamic_shape_as_tensor(ctx, base_dilation),
        eval_dynamic_shape_as_tensor(ctx, window_dilation),
        d_padding],
       called_computations=[reducer.name.value],
    )
  else:  # Static shapes
    rw = hlo.ReduceWindowOp(
        flat_result_types,
        operands, init_values,
        dense_int_array(window_dimensions),
        window_strides=dense_int_array(window_strides),
        base_dilations=dense_int_array(base_dilation),
        window_dilations=dense_int_array(window_dilation),
        padding=ir.DenseIntElementsAttr.get(np.asarray(padding, np.int64),
                                            shape=[len(padding), 2]))
    reducer = rw.regions[0].blocks.append(*(scalar_types + scalar_types))
    with ir.InsertionPoint(reducer):
      hlo.return_(reducer_body(reducer))
  return [lower_with_sharding_in_types(ctx, r, aval)
          for r, aval in zip(rw.results, ctx.avals_out)]


def reduce_window(
    operand: Any,
    init_value: Any,
    computation: Callable,
    window_dimensions: core.Shape,
    window_strides: Sequence[int] | None = None,
    padding: str | Sequence[tuple[int, int]] = "VALID",
    base_dilation: Sequence[int] | None = None,
    window_dilation: Sequence[int] | None = None,
) -> Any:
  """Reduction over padded windows.

  Wraps XLA's ReduceWindowWithGeneralPadding_ operator.

  Args:
    operand: input array or tree of arrays.
    init_value: value or tree of values. Tree structure must match that
      of ``operand``. The values in ``init_value`` must be scalars.
    computation: callable function over which to reduce. Input and output must be
      a tree of the same structure as ``operand``.
    window_dimensions: sequence of integers specifying the window size.
    window_strides: optional sequence of integers specifying the strides, of
      the same length as ``window_dimensions``.  Default (``None``) indicates
      a unit stride in each window dimension.
    padding: string or sequence of integer tuples specifying the type of padding
      to use (default: "VALID"). If a string, must be one of "VALID", "SAME", or
      "SAME_LOWER". See the :func:`jax.lax.padtype_to_pads` utility.
    base_dilation: optional sequence of integers for base dilation values, of
      the same length as ``window_dimensions``. Default (``None``) indicates unit
      dilation in each window dimension.
    window_dilation: optional sequence of integers for window dilation values, of
      the same length as ``window_dimensions``. Default (``None``) indicates unit
      dilation in each window dimension.

  Returns:
    A tree of arrays with the same structure as ``operand``.

  Example:
    Here is a simple example of a windowed product over pairs in a 1-dimensional array:

    >>> import jax
    >>> x = jax.numpy.arange(10, dtype='float32')
    >>> x
    Array([0., 1., 2., 3., 4., 5., 6., 7., 8., 9.], dtype=float32)

    >>> initial = jax.numpy.float32(1)
    >>> jax.lax.reduce_window(x, initial, jax.lax.mul, window_dimensions=(2,))
    Array([ 0.,  2.,  6., 12., 20., 30., 42., 56., 72.], dtype=float32)

  .. _ReduceWindowWithGeneralPadding: https://www.openxla.org/xla/operation_semantics#reducewindow
  """
  return _reduce_window(
      operand,
      init_value,
      computation,
      window_dimensions,
      window_strides,
      padding,
      base_dilation,
      window_dilation,
  )

