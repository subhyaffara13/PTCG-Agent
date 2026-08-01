
def _rnn_fwd_lowering(_rnn, platform, ctx, input, h_0, c_0, weights, seq_lengths, *,
                       input_size: int, hidden_size: int, num_layers: int,
                       dropout: bool, bidirectional: bool,
                       cudnn_allow_tf32: bool):
  """CuDnn RNN."""
  out_dtype = ctx.avals_out[0].dtype
  if out_dtype == np.float32:
    out_type = ir.F32Type.get()
  elif out_dtype == np.float64:
    out_type = ir.F64Type.get()
  elif out_dtype == np.complex64:
    out_type = ir.ComplexType.get(ir.F32Type.get())
  elif out_dtype == np.complex128:
    out_type = ir.ComplexType.get(ir.F64Type.get())
  else:
    raise ValueError(f'Unknown output type {out_dtype}')

  output_type = ir.RankedTensorType.get(ctx.avals_out[0].shape, out_type)
  batch_size = ctx.avals_in[0].shape[0]
  max_seq_length = ctx.avals_in[0].shape[1]
  # workspace_shape = ctx.avals_out[3].shape
  workspace_size, _ = compute_rnn_workspace_reserve_space_sizes(
      input_size, hidden_size, num_layers, batch_size, max_seq_length,
      dropout, bidirectional, cudnn_allow_tf32)
  workspace_shape = (workspace_size,)
  workspace_type = ir.RankedTensorType.get(workspace_shape, ir.F32Type.get())
  reserve_space_shape = ctx.avals_out[3].shape
  reserve_space_type = ir.RankedTensorType.get(reserve_space_shape,
                                               ir.F32Type.get())
  if not _rnn:
    raise GpuLibNotLinkedError()

  opaque = _rnn.build_rnn_descriptor(input_size, hidden_size, num_layers,
                                     batch_size, max_seq_length, dropout,
                                     bidirectional, cudnn_allow_tf32,
                                     workspace_shape[0],
                                     reserve_space_shape[0])

  i32_type = ir.IntegerType.get_signless(32)
  out = hlo.CustomCallOp(
      [output_type, h_0.type, c_0.type, workspace_type, reserve_space_type],
      [input, h_0, c_0, weights, seq_lengths],
      call_target_name=ir.StringAttr.get(f"{platform}dnn_rnn_ffi"),
      has_side_effect=ir.BoolAttr.get(False),
      backend_config=ir.DictAttr.get({"opaque": ir.StringAttr.get(opaque)}),
      api_version=ir.IntegerAttr.get(i32_type, 4),
      called_computations=ir.ArrayAttr.get([]),
  )
  return out.results[:-2] + out.results[-1:]  # drop workspace output

