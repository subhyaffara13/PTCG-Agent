
def average_parameters_or_parameter_groups(
    params: Iterable[torch.nn.Parameter] | Iterable[dict[str, torch.nn.Parameter]],
    process_group: ProcessGroup,
):
    """Averages parameters of a model or parameter groups of an optimizer."""
    average_parameters(iter(get_params_to_average(params)), process_group)

