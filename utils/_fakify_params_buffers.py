
def _fakify_params_buffers(
    fake_mode: FakeTensorMode,
    mod: torch.nn.Module,
) -> dict[str, torch.Tensor | torch.nn.Parameter]:
    params_buffers = {
        **dict(mod.named_parameters(remove_duplicate=False)),
        **dict(mod.named_buffers(remove_duplicate=False)),
    }

    faked_params_buffers = {}
    memo: dict[int, FakeTensor] = {}
    for key, value in params_buffers.items():
        if id(value) in memo:
            fake_tensor = memo[id(value)]
        else:
            fake_tensor = fake_mode.from_tensor(value, static_shapes=True)
            memo[id(value)] = fake_tensor
        faked_params_buffers[key] = fake_tensor
    return faked_params_buffers  # type: ignore[return-value]

