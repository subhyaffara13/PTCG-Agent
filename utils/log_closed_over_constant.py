
def log_closed_over_constant(v: core.Literal, eqn: core.JaxprEqn,
                             debug_info: core.DebugInfo):
  if getattr(v.val, "nbytes", 4) < config.captured_constants_warn_bytes.value:
    return
  msg = (f"Closed-over constant {type(v.val)}: {v.aval.str_short()} "
         f"in {debug_info.func_src_info}")
  if (num_frames := config.captured_constants_report_frames.value) > 0:
    eqn_si = source_info_util.summarize(eqn.source_info, num_frames)
    msg += (" used at:\n" +
           "  " * 2 + eqn_si.replace("\n", "\n" + "  " * 2) +
           "\n\n")
  warnings.warn(msg)

