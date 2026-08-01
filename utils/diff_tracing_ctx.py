
def diff_tracing_ctx(new_ctx, old_ctx) -> tuple[int, int, str] | None:
  if new_ctx == old_ctx: return None
  diffs: list[str] = []
  msg = "Tracing context doesn't match, e.g. due to config or context manager."
  if len(new_ctx) != len(old_ctx):
    num_diff = abs(len(new_ctx) - len(old_ctx))
    diffs.append("  * number of tracing context values differs: "
                f"now {len(new_ctx)} and before {len(old_ctx)}")
    return 0, num_diff, msg + "\n" + "\n".join(diffs)

  num_diff = sum(map(op.ne, new_ctx, old_ctx))
  if jaxlib_extension_version < 455:
    return 0, num_diff, msg

  context_names = config.trace_context_names()
  if len(context_names) != len(new_ctx):
    diffs.append("  * number of tracing context names differs: "
                  f"context_names {len(context_names)} vs "
                  f"context length {len(new_ctx)}")
    return 0, num_diff, msg + "\n" + "\n".join(diffs)
  for name, new, old in zip(context_names, new_ctx, old_ctx):
    if new != old:
      diffs.append(f"  * {name} differs: now {new} and before {old}")
  return 0, num_diff, msg + "\n" + "\n".join(diffs)

