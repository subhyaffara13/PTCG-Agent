
def wrapper_set_seed(op, *args, **kwargs):
    """Wrapper to set seed manually for some functions like dropout
    See: https://github.com/pytorch/pytorch/pull/62315#issuecomment-896143189 for more details.
    """
    with freeze_rng_state():
        torch.manual_seed(42)
        output = op(*args, **kwargs)

        if isinstance(output, torch.Tensor) and output.device.type == "lazy":
            # We need to call mark step inside freeze_rng_state so that numerics
            # match eager execution
            torch._lazy.mark_step()  # type: ignore[attr-defined]

        return output

