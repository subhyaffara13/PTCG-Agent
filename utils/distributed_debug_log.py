
def distributed_debug_log(*pairs):
  """Format and log `pairs` if config.jax_distributed_debug is enabled.

  Args:
    pairs: A sequence of label/value pairs to log. The first pair is treated as
    a heading for subsequent pairs.
  """
  if config.distributed_debug.value:
    lines = ["\nDISTRIBUTED_DEBUG_BEGIN"]
    try:
      lines.append(f"{pairs[0][0]}: {pairs[0][1]}")
      for label, value in pairs[1:]:
        lines.append(f"  {label}: {value}")
    except Exception as e:
      lines.append("DISTRIBUTED_DEBUG logging failed!")
      lines.append(f"{e}")
    lines.append("DISTRIBUTED_DEBUG_END")
    logger.warning("\n".join(lines))

