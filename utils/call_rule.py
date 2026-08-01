
def call_rule(rule, axis_size, in_batched, args):
  return rule(axis_size, ensure_list(in_batched), *args)

