
def get_swa_avg_fn():
    """Get the function applying stochastic weight average (SWA) across a single param."""

    @torch.no_grad()
    def swa_update(
        averaged_param: Tensor, current_param: Tensor, num_averaged: Tensor | int
    ):
        return averaged_param + (current_param - averaged_param) / (num_averaged + 1)

    return swa_update

