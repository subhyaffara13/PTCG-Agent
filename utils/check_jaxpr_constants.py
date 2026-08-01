
def check_jaxpr_constants(closed_jaxpr: core.ClosedJaxpr):
  """Check if a JAXPR contains an excessive amount of constants, if so, report where they were captured"""
  if (threshold := config.captured_constants_warn_bytes.value) == -1:
    return

  # need the unaesthetic getter here as some of the consts in the test suite are arbitrary objects
  total_iter, nbytes_iter = itertools.tee(
      map(lambda c: getattr(c, "nbytes", 0), closed_jaxpr.consts)
  )

  if (total_bytes := sum(total_iter)) < threshold:
    return

  message = (
      "A large amount of constants were captured during lowering"
      f" ({util.pprint_bytes(total_bytes)} total). If this is intentional,"
      " disable this warning by setting JAX_CAPTURED_CONSTANTS_WARN_BYTES=-1. "
  )

  if not (num_frames := config.captured_constants_report_frames.value):
    message += (
        "To obtain a report of where these constants were encountered, "
        "set JAX_CAPTURED_CONSTANTS_REPORT_FRAMES=-1."
    )
    warnings.warn(message)
    return

  message += (
      "The subsequent report may be disabled by setting JAX_CAPTURED_CONSTANTS_REPORT_FRAMES=0.\n\n"
      f"Largest {min(num_frames, len(closed_jaxpr.consts))} allocation(s):\n"
  )
  try:
    nbytes_var_const = zip(nbytes_iter, closed_jaxpr.jaxpr.constvars, closed_jaxpr.consts)
    for nbytes, var, const in heapq.nlargest(5, nbytes_var_const, key=operator.itemgetter(0)):
      message += f"  Constant {type(const)}, {var.aval.str_short()}, {util.pprint_bytes(nbytes)} captured at:\n"

      for eqn in jaxpr_util.eqns_using_var(closed_jaxpr.jaxpr, var):
        call_frame_source_info = source_info_util.summarize(eqn.source_info, num_frames)
        message += "  " * 2 + call_frame_source_info.replace("\n", "\n" + "  " * 2) + "\n\n"

    warnings.warn(message)
  except Exception as exc:
    warnings.warn(message + f" Exception raised while generating report: {exc}")

