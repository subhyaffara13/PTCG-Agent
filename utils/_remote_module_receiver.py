
def _remote_module_receiver(
    *remote_module_pickled_attrs,
):
    """Deserializes a RemoteModule."""
    serialized_remote_module = _SerializedRemoteModule._make(
        remote_module_pickled_attrs
    )
    m = object.__new__(RemoteModule)
    m.__dict__.update(serialized_remote_module._asdict())

    # Unpickling the attribute `module_rref` must invoke RRef's `_deserialize()` method.
    m.module_rref = rpc.PyRRef._deserialize(m.module_rref)

    # Install generated methods when unpickled.
    for method in m.generated_methods:
        method_name = method.__name__
        method = torch.jit.export(method)
        setattr(m, method_name, types.MethodType(method, m))

    return m

