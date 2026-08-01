
def count_subjaxpr_to_hlo_conversion(fun_name):
  assert thread_local_state.lower_jaxpr_to_fun_counts is None
  counts = collections.Counter()
  thread_local_state.lower_jaxpr_to_fun_counts = counts
  def get():
    key, *others = {k for k in counts if fun_name in k}
    if others: raise Exception(f"ambiguous name: {fun_name}")
    return counts[key]
  try:
    yield get
  finally:
    thread_local_state.lower_jaxpr_to_fun_counts = None

