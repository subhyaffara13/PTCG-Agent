
def _split_node(node):
  return _AST_SPLIT_CONFIG_PATH.get(type(node), ast.literal_eval)(node)

