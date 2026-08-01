
def treespec_pprint(treespec: TreeSpec) -> str:
    dummy_tree = tree_unflatten([_asterisk] * treespec.num_leaves, treespec)
    return repr(dummy_tree)


def treespec_pprint(treespec: TreeSpec) -> str:
    dummy_tree = tree_unflatten([_asterisk] * treespec.num_leaves, treespec)
    return repr(dummy_tree)

