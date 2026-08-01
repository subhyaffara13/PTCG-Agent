
def _zero_model(
    model: nn.Module,
    zero_buffers: bool = False,
    summon_full=True,
):
    """Zeros the parameters and optionally buffers of ``model`` in place."""
    ctx = FSDP.summon_full_params(model) if summon_full else nullcontext()
    with ctx:
        for param in model.parameters():
            with torch.no_grad():
                param.zero_()
        if zero_buffers:
            for buffer in model.buffers():
                with torch.no_grad():
                    buffer.zero_()

