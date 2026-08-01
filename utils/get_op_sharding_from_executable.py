
def get_op_sharding_from_executable(
    executable) -> tuple[Sequence[xc.OpSharding], Sequence[xc.OpSharding]]:
  in_op_shardings: list[xc.OpSharding] = []
  parameter_shardings_from_xla = executable.get_parameter_shardings()
  if parameter_shardings_from_xla is not None:
    in_op_shardings = parameter_shardings_from_xla

  out_op_shardings: list[xc.OpSharding] = []
  output_shardings_from_xla = executable.get_output_shardings()
  if output_shardings_from_xla is not None:
    out_op_shardings = output_shardings_from_xla

  return in_op_shardings, out_op_shardings

