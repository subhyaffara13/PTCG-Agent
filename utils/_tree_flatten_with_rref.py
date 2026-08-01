
def _tree_flatten_with_rref(output):
    output_is_rref = RPC_AVAILABLE and isinstance(output, RRef)
    if output_is_rref:
        output_tensor_list, treespec = tree_flatten(output.local_value())
    else:
        output_tensor_list, treespec = tree_flatten(output)
    # Need to return flattened tensors, spec to re-pack them, as well
    # as if the return type was actually an RRef to reconstruct.
    return output_tensor_list, treespec, output_is_rref

