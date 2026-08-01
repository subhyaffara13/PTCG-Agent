
def _tensor_to_object(tensor, tensor_size, group):
    with _WaitCounter("pytorch.wait_counter.c10d._tensor_to_object").guard():
        if get_debug_level() == DebugLevel.DETAIL and is_nccl_available():
            backend = get_backend(group)
            if backend == Backend.NCCL:
                hash = torch._C._distributed_c10d._hash_tensors([tensor])
                logger.warning(
                    "_tensor_to_object size: %s hash value: %s", tensor.numel(), hash
                )
        tensor = tensor.cpu()
        buf = tensor.numpy().tobytes()[:tensor_size]
        return _unpickler(io.BytesIO(buf)).load()

