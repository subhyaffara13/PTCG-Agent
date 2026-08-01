
def event_listener(name, *args):
  counts = thread_local_state.counts
  counts[name] = counts.get(name, 0) + 1

  # device_put handlers might call `dispatch.device_put` (e.g. on an
  # underlying payload or several). We only want to count these
  # recursive puts once, so we skip counting more than the outermost
  # one in such a call stack.
  if name == "batched_device_put_start":
    if thread_local_state.nested_device_put_count == 0:
      counts["batched_device_put"] = counts.get("batched_device_put", 0) + 1
    thread_local_state.nested_device_put_count += 1
  elif name == "batched_device_put_end":
    thread_local_state.nested_device_put_count -= 1

  elif name == "lower_jaxpr_to_fun":
    # For infer_params, we collect per-function data, but only while a context
    # manager is active.
    lower_counts = thread_local_state.lower_jaxpr_to_fun_counts
    if lower_counts is not None:
      (fun,) = args
      lower_counts[fun] += 1
  elif name == "mlir.collect_lowered_jaxprs":
    collection = thread_local_state.collect_lowered_jaxprs
    if collection is not None:
      collection.append(args)

