
def serialize_torch_artifact(
    artifact: Any | None, pickle_protocol: int = DEFAULT_PICKLE_PROTOCOL
) -> bytes:
    if artifact is None:
        return b""

    if FakeTensor in copyreg.dispatch_table:
        raise AssertionError("Refusing to stomp on existing FakeTensor reducer")
    try:
        copyreg.pickle(FakeTensor, _reduce_fake_tensor)
        buffer = io.BytesIO()
        # This is a workaround for backend's tensor deserialization problem:
        # unpickleTensor() always create a tensor on the device where it was originally saved
        # This behavior is bad for multi-gpu training, as we wish to directly load the tensor
        # on the designated device.
        # For now, we simply move the tensor to cpu before saving.
        # TODO: this should be fixed by deserialization instead.
        torch.save(artifact, buffer, pickle_protocol=pickle_protocol)
        return buffer.getvalue()
    finally:
        del copyreg.dispatch_table[FakeTensor]

