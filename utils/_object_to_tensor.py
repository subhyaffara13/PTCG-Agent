
def _object_to_tensor(obj, device, group):
    with _WaitCounter("pytorch.wait_counter.c10d._object_to_tensor").guard():
        f = io.BytesIO()
        _pickler(f).dump(obj)
        byte_storage = torch.ByteStorage._from_buffer(f.getvalue())  # type: ignore[attr-defined]
        # Do not replace `torch.ByteTensor` or `torch.LongTensor` with torch.tensor and specifying dtype.
        # Otherwise, it will cause 100X slowdown.
        # See: https://github.com/pytorch/pytorch/issues/65696
        byte_tensor = torch.ByteTensor(byte_storage).to(device)
        if get_debug_level() == DebugLevel.DETAIL and is_nccl_available():
            backend = get_backend(group)
            if backend == Backend.NCCL:
                hash = torch._C._distributed_c10d._hash_tensors([byte_tensor])
                logger.warning(
                    "_object_to_tensor size: %s hash value: %s",
                    byte_tensor.numel(),
                    hash,
                )
        local_size = torch.LongTensor([byte_tensor.numel()]).to(device)
        return byte_tensor, local_size

