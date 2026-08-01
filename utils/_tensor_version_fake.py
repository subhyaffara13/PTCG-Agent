
def _tensor_version_fake(fake_mode: FakeTensorMode, self_tensor: Any) -> SymInt:
    """
    The initial dynamo capture of _tensor_version + _unsafe_set_version_counter turns the
    `._version` into an unbacked SymInt so that we don't need to specialize on the `._version`
    of input tensors to the graph.
    """
    assert fake_mode.shape_env is not None
    return fake_mode.shape_env.create_unbacked_symint()

