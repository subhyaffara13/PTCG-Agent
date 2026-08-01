
def _calculate_shape(
    output: torch.Tensor | graph.GradientEdge,
    grad: torch.Tensor,
    is_grads_batched: bool,
) -> tuple[_ShapeorNestedShape, _ShapeorNestedShape]:
    # is_same_size ensures that both tensors are either nested or non nested
    # circular import
    from torch.nested._internal.nested_tensor import NestedTensor

    if isinstance(output, graph.GradientEdge):
        # We have already checked that we are not a C++ NestedTensor
        if is_grads_batched:
            raise RuntimeError("Batched grads are not supported with GradientEdge")
        out_metadata = output.node._input_metadata[output.output_nr]
        return torch.Size(out_metadata.shape), grad.shape

    if output.is_nested and not isinstance(output, NestedTensor):
        if is_grads_batched:
            raise RuntimeError("Batched grads are not supported with Nested Tensor.")
        out_shape = output._nested_tensor_size()
        grad_shape = grad._nested_tensor_size()

        return out_shape, grad_shape

    reg_out_shape = output.shape
    reg_grad_shape = grad.shape if not is_grads_batched else grad.shape[1:]
    return reg_out_shape, reg_grad_shape

