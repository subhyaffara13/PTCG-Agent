
def get_size_of_node(fx_module: GraphModule, node: Node) -> size_bytes:
    """Given a node with node.dtype and node.shape, return its total size and its output size.
    total_size = weights + bias + output_size
    """
    # Total num of elements
    total_num_of_elems = 0
    # For a module, consider all parameters
    if node.op == "call_module":
        submodule_dict = dict(fx_module.named_modules())
        submodule = submodule_dict[node.target]
        parameters = submodule.named_parameters()
        # Parameters are named tuples
        for _name, p in parameters:
            total_num_of_elems += p.numel()
    # Don't forget the output size
    # node.shape is the shape of this node's output
    tensor_meta = get_tensor_meta(node)
    output_elem = tensor_meta.shape.numel()
    total_num_of_elems += output_elem
    # Assume for now if it's quantized then it's qint8 or quint8
    if tensor_meta.is_quantized:
        size_per_elem_bytes = torch._empty_affine_quantized(
            [], dtype=tensor_meta.dtype
        ).element_size()
    else:
        size_per_elem_bytes = torch.tensor([], dtype=tensor_meta.dtype).element_size()
    total_size = size_per_elem_bytes * total_num_of_elems
    output_size = size_per_elem_bytes * output_elem
    return size_bytes(output_size, total_size)

