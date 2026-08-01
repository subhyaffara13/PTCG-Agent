
def _assert_valid_qconfig(qconfig: QConfig | None, mod: torch.nn.Module) -> None:
    """
    Verifies that this `qconfig` is valid.
    """
    if qconfig is None:
        return
    is_conv_transpose_mod = isinstance(
        mod,
        (torch.nn.ConvTranspose1d, torch.nn.ConvTranspose2d, torch.nn.ConvTranspose3d),
    )
    if is_conv_transpose_mod:
        if qconfig.weight is None:
            # for now, we assume that any qconfig for ConvTranspose without a weight is valid
            return
        example_observer = qconfig.weight()
        is_per_channel = isinstance(
            example_observer,
            (
                torch.ao.quantization.PerChannelMinMaxObserver,
                torch.ao.quantization.MovingAveragePerChannelMinMaxObserver,
            ),
        )
        if is_per_channel:
            raise AssertionError(
                "Per channel weight observer is not supported yet for ConvTranspose{n}d."
            )

