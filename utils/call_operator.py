
def call_operator(operator, *args):
    return pytree.tree_leaves(operator(*args))

