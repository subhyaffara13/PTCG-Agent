
def _replace_operation_buffer(
    orig_node: ir.MultiTemplateBuffer, new_node: ir.OperationBuffer
) -> None:
    replaced_buf_name = new_node.get_name()
    orig_buf_name = orig_node.get_name()
    assert isinstance(orig_buf_name, str) and isinstance(replaced_buf_name, str)

    replaced_op_name = new_node.get_operation_name()
    orig_op_name = orig_node.get_operation_name()
    assert isinstance(orig_op_name, str) and isinstance(replaced_op_name, str)

    del V.graph.name_to_buffer[replaced_buf_name]
    new_node.name = orig_buf_name

    del V.graph.name_to_op[replaced_op_name]
    new_node.operation_name = orig_op_name

    orig = V.graph.buffers.index(orig_node)
    V.graph.buffers.remove(new_node)
    V.graph.buffers[orig] = new_node
    V.graph.name_to_buffer[orig_buf_name] = new_node

    orig = V.graph.operations.index(orig_node)
    V.graph.operations.remove(new_node)
    V.graph.operations[orig] = new_node
    V.graph.name_to_op[orig_op_name] = new_node

