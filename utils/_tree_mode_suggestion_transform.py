
def _tree_mode_suggestion_transform(fn_name: str) -> str:
  return (
    f'Consider the following options:\n\n'
    '1. Remove the duplicates.\n'
    f'2. Enable graph mode and graph updates by passing graph=True and '
    f'graph_updates=True to {fn_name} e.g.\n\n'
    f'  nnx.{fn_name}(..., graph=True, graph_updates=True)\n\n'
    f'3. Use nnx.compat.{fn_name} instead e.g.\n\n'
    f'  nnx.compat.{fn_name}(...)'
  )

