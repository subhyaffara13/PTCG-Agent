
def register_buffer_assignment_hook(
    mod: torch.nn.Module, assigned_buffers: dict[str, str]
) -> Any:
    """
    Register a hook that intercepts buffer assignments.
    This is used to detect when a buffer is assigned to, and then we can
    map that buffer to the corresponding proxy node in the graph.
    """

    def _map_assigned_buffer_to_proxy(
        _mod: torch.nn.Module, name: str, buffer: Any
    ) -> Any:
        # We intercept buffer assignments on the root module through this hook.
        if _mod._buffers is mod._buffers:
            # either buffer is a functional tensor, which wraps a fake tensor
            if isinstance(buffer, FunctionalTensor):
                buffer = buffer.from_functional()
            # or buffer is a fake tensor
            if not isinstance(buffer, FakeTensor):
                raise AssertionError(f"expected FakeTensor, got {type(buffer)}")
            # The fake tensor in turn is associated with a proxy node.
            proxy_mode = torch.fx.experimental.proxy_tensor.get_proxy_mode()
            if proxy_mode is None:
                raise AssertionError("proxy_mode must not be None")
            proxy = torch.fx.experimental.proxy_tensor.get_proxy_slot(
                buffer, proxy_mode.tracer
            ).proxy.node
            # We map the assigned buffer to this proxy node.
            assigned_buffers[name] = proxy.name
        return buffer

    return torch.nn.modules.module.register_module_buffer_registration_hook(
        _map_assigned_buffer_to_proxy
    )

