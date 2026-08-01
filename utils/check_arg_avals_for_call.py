
def check_arg_avals_for_call(ref_avals, arg_avals,
                             jaxpr_debug_info: core.DebugInfo):
  if len(ref_avals) != len(arg_avals):
    raise TypeError(
        f"Computation compiled for {len(ref_avals)} inputs "
        f"but called with {len(arg_avals)}")

  arg_names = [f"'{name}'" for name in jaxpr_debug_info.safe_arg_names(len(ref_avals))]

  errors = []
  for ref_aval, arg_aval, name in safe_zip(ref_avals, arg_avals, arg_names):
    # Don't compare shardings of avals because you can lower with
    # numpy arrays + in_shardings and call compiled executable with
    # sharded arrays. We also have sharding checks downstream.
    if (ref_aval.shape, ref_aval.dtype) != (arg_aval.shape, arg_aval.dtype):
      errors.append(
          f"Argument {name} compiled with {ref_aval.str_short()} and called "
          f"with {arg_aval.str_short()}")
  if errors:
    max_num_errors = 5
    str_errors = "\n".join(errors[:max_num_errors])
    if len(errors) >= max_num_errors:
      num_mismatch_str = f"The first {max_num_errors} of {len(errors)}"
    else:
      num_mismatch_str = "The"
    raise TypeError(
        "Argument types differ from the types for which this computation was "
        "compiled. Perhaps you are calling the compiled executable with a "
        "different enable_x64 mode than when it was AOT compiled? "
        f"{num_mismatch_str} mismatches are:\n{str_errors}")

