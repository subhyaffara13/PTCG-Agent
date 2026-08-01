
def get_num_model_outputs(model: GraphModule) -> int:
    model_outputs_node = output_node(model)
    model_outputs = pytree.arg_tree_leaves(*model_outputs_node.args)
    return len(model_outputs)

