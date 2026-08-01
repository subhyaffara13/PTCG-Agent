
def get_swa_multi_avg_fn():
    """Get the function applying stochastic weight average (SWA) across multiple params."""

    @torch.no_grad()
    def swa_update(
        averaged_param_list: PARAM_LIST,
        current_param_list: PARAM_LIST,
        num_averaged: Tensor | int,
    ) -> None:
        # foreach lerp only handles float and complex
        if torch.is_floating_point(averaged_param_list[0]) or torch.is_complex(
            averaged_param_list[0]
        ):
            torch._foreach_lerp_(
                averaged_param_list,
                current_param_list,
                cast(float, 1 / (num_averaged + 1)),
            )
        else:
            diffs = torch._foreach_sub(current_param_list, averaged_param_list)
            if isinstance(num_averaged, Tensor):
                torch._foreach_addcdiv_(
                    averaged_param_list,
                    diffs,
                    [num_averaged + 1] * len(averaged_param_list),
                )
            else:
                torch._foreach_add_(
                    averaged_param_list, diffs, alpha=1.0 / (num_averaged + 1)
                )

    return swa_update

