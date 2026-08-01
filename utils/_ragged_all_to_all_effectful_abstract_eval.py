
def _ragged_all_to_all_effectful_abstract_eval(
    operand, output, input_offsets, send_sizes, output_offsets, recv_sizes,
    axis_name, axis_index_groups
):
  del operand, axis_index_groups
  if not dtypes.issubdtype(input_offsets.dtype, np.integer):
    raise ValueError("ragged_all_to_all input_offsets must be integer type.")
  if not dtypes.issubdtype(send_sizes.dtype, np.integer):
    raise ValueError("ragged_all_to_all send_sizes must be integer type.")
  if not dtypes.issubdtype(output_offsets.dtype, np.integer):
    raise ValueError("ragged_all_to_all output_offsets must be integer type.")
  if not dtypes.issubdtype(recv_sizes.dtype, np.integer):
    raise ValueError("ragged_all_to_all recv_sizes must be integer type.")
  if len(input_offsets.shape) != 1 or input_offsets.shape[0] < 1:
    raise ValueError(
        "ragged_all_to_all input_offsets must be rank 1 with positive dimension"
        " size, but got shape {}".format(input_offsets.shape)
    )
  if len(send_sizes.shape) != 1 or send_sizes.shape[0] < 1:
    raise ValueError(
        "ragged_all_to_all send_sizes must be rank 1 with positive dimension"
        " size, but got shape {}".format(send_sizes.shape)
    )
  if len(output_offsets.shape) != 1 or output_offsets.shape[0] < 1:
    raise ValueError(
        "ragged_all_to_all output_offsets must be rank 1 with positive"
        " dimension size, but got shape {}".format(output_offsets.shape)
    )
  if len(recv_sizes.shape) != 1 or recv_sizes.shape[0] < 1:
    raise ValueError(
        "ragged_all_to_all recv_sizes must be rank 1 with positive dimension"
        " size, but got shape {}".format(recv_sizes.shape)
    )

  _check_axis_names(axis_name, 'ragged_all_to_all')
  out_aval = output.update(shape=output.shape, weak_type=False)
  effects = {*map(core.NamedAxisEffect, axis_name)}
  return out_aval, effects

