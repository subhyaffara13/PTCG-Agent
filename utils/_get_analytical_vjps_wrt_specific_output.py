
def _get_analytical_vjps_wrt_specific_output(
    vjp_fn, sample_output, v
) -> list[list[torch.Tensor | None]]:
    grad_inputs = vjp_fn(v.reshape(sample_output.shape))
    vjps: list[list[torch.Tensor | None]] = [
        [vjp.clone() if isinstance(vjp, torch.Tensor) else None] for vjp in grad_inputs
    ]
    return vjps

