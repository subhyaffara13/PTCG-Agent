
def _rnn_bwd_lowering(_rnn, platform, ctx, dy, dhn, dcn, x, h0, c0, w, y,
                           reserve_space, seq_lengths, *, input_size: int,
                           hidden_size: int, num_layers: int, dropout: bool,
                           bidirectional: bool, cudnn_allow_tf32: bool):
  """CuDnn RNN Backward pass."""
  batch_size = ctx.avals_in[3].shape[0]
  max_seq_length = ctx.avals_in[3].shape[1]
  workspace_size, _ = compute_rnn_workspace_reserve_space_sizes(
      input_size, hidden_size, num_layers, batch_size, max_seq_length,
      dropout, bidirectional, cudnn_allow_tf32)
  workspace_shape = (workspace_size,)
  workspace_type = ir.RankedTensorType.get(workspace_shape, ir.F32Type.get())
  reserve_space_shape = ctx.avals_in[8].shape

  if _rnn is None:
    raise RuntimeError("cuda couldn't be imported")
  opaque = _rnn.build_rnn_descriptor(input_size, hidden_size, num_layers,
                                     batch_size, max_seq_length, dropout,
                                     bidirectional, cudnn_allow_tf32,
                                     workspace_shape[0],
                                     reserve_space_shape[0])

  i32_type = ir.IntegerType.get_signless(32)
  zeroed_dw = _hlo_zeros_f32(ctx.avals_out[3].shape)
  out = hlo.CustomCallOp(
      [x.type, h0.type, c0.type, w.type, workspace_type], [
          dy, dhn, dcn, x, h0, c0, w, y, reserve_space, zeroed_dw,
          seq_lengths
      ],
      call_target_name=ir.StringAttr.get(f"{platform}dnn_rnn_bwd_ffi"),
      has_side_effect=ir.BoolAttr.get(False),
      backend_config=ir.DictAttr.get({"opaque": ir.StringAttr.get(opaque)}),
      api_version=ir.IntegerAttr.get(i32_type, 4),
      called_computations=ir.ArrayAttr.get([]),
      output_operand_aliases=ir.ArrayAttr.get([
          hlo.OutputOperandAlias.get(
              output_tuple_indices=[3],
              operand_index=9,
              operand_tuple_indices=[])
      ]))
  return out.results[:-1]  # drop workspace output

