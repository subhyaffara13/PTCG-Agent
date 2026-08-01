
def _is_static_for_cudagraphs(x: torch.Tensor) -> bool:
    from torch._inductor.cudagraph_trees import get_manager

    if x.is_cuda:
        manager = get_manager(x.device.index, False)
        is_static_address = torch._dynamo.utils.get_static_address_type(x) is not None
        if manager:
            assert manager.current_node is not None
            return (
                is_static_address
                or manager.current_node._is_cuda_graph_recorded_tensor(x)
            )
        else:
            return is_static_address
    else:
        # Don't print a warning for non-cuda tensors
        return True

