
def _compute_analytical_jacobian_rows(
    vjp_fn, sample_output
) -> list[list[torch.Tensor | None]]:
    # Computes Jacobian row-by-row by projecting `vjp_fn` = v^T J on standard basis
    # vectors: vjp_fn(e) = e^T J is a corresponding row of the Jacobian.
    # NB: this function does not assume vjp_fn(v) to return tensors with the same
    # number of elements for different v. This is checked when we later combine the
    # rows into a single tensor.
    grad_out_base = torch.zeros_like(
        sample_output, memory_format=torch.legacy_contiguous_format
    )
    flat_grad_out = grad_out_base.view(-1)
    # jacobians_rows[i][j] is the Jacobian jth row for the ith input
    jacobians_rows: list[list[torch.Tensor | None]] = []
    for j in range(flat_grad_out.numel()):
        flat_grad_out.zero_()
        flat_grad_out[j] = 1.0  # projection for jth row of Jacobian
        grad_inputs = vjp_fn(grad_out_base)
        for i, d_x in enumerate(grad_inputs):
            if j == 0:
                jacobians_rows.append([])
            jacobians_rows[i] += [
                d_x.clone() if isinstance(d_x, torch.Tensor) else None
            ]
    return jacobians_rows

