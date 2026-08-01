
def _tree_mode_suggestion_api(fn_name: str) -> str:
  return (
    f'Consider the following options:\n\n'
    '1. Remove the duplicates and guarantee a tree structure.\n'
    f'2. Enable graph mode by passing graph=True to {fn_name} e.g.\n\n'
    f'  nnx.{fn_name}(..., graph=True)\n\n'
    f'3. Use nnx.compat.{fn_name} instead e.g.\n\n'
    f'  nnx.compat.{fn_name}(...)'
  )

