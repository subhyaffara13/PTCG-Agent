
def observe_tensor_cycles(callback):
    torch.cuda.memory._record_memory_history(max_entries=100000)

    def observer(garbage) -> None:
        if garbage:
            if not any(is_cuda_tensor(obj) for obj in garbage):
                logger.info("No CUDA Tensors found in garbage")
                return
            callback(to_html(create_graph(garbage)))
    return observe_garbage(observer)

