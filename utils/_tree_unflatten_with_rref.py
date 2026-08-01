
def _tree_unflatten_with_rref(output, treespec, output_is_rref):
    output = tree_unflatten(output, treespec)
    if output_is_rref:
        output = RRef(output)
    return output

