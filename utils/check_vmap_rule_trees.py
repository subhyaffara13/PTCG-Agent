
def check_vmap_rule_trees(rule, original_out_tree, out_tree, out_batched_tree):
  if out_tree != out_batched_tree:
    raise ValueError(
        'structure of output value and output batching specification returned '
        f'by custom vmap rule ({rule_name(rule)}) do not match.\n'
        f'Output values: {out_tree}\n'
        f'Batching spec: {out_batched_tree}')
  if out_tree != original_out_tree:
    raise ValueError(
        f'structure of output returned by custom vmap rule ({rule_name(rule)}) '
        'does not match that of original custom-vmapped function.\n'
        f'Original output: {original_out_tree}\n'
        f'Rule output: {out_tree}')

