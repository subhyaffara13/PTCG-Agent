
def assert_no_fake_params_or_buffers(gm: torch.nn.Module) -> None:
    from torch._subclasses.fake_tensor import FakeTensorConfig, is_fake

    def stack_or_hint(t: Any) -> str:
        if FakeTensorConfig.debug:
            import traceback

            return f"FAKE TENSOR CREATION TRACEBACK: \n {traceback.format_list(t._debug_trace)}"
        else:
            return "Enable TORCH_FAKE_TENSOR_DEBUG=1 to get creation stack traces on fake tensors."

    for name, buffer in gm.named_buffers():
        assert not is_fake(buffer), (
            f"Unexpected fake buffer {name} {stack_or_hint(buffer)}"
        )
    for name, param in gm.named_parameters():
        assert not is_fake(param), (
            f"Unexpected fake param {name} {stack_or_hint(param)}"
        )

