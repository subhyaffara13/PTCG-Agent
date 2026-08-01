
def _find_arg_mismatch(arg_list, fails, fun_name):
  mismatched_args_msg = []
  def mismatch(err):
    for name, inp_da, aval in arg_list:
      if err.m_type == MismatchType.ARG_SHARDING and err.da == inp_da:
        mismatched_args_msg.append(
            f"argument {name} of {fun_name} with shape {aval.str_short()} and "
            f"{err._dev_ids_plat_str}")
        break
  first_err, second_err = fails
  mismatch(first_err)
  mismatch(second_err)
  return mismatched_args_msg

