
def get_params_to_average(
    params: Iterable[torch.nn.Parameter] | Iterable[dict[str, torch.nn.Parameter]],
):
    """
    Return a list of parameters that need to average.

    This filters out the parameters that do not contain any gradients.
    Args:
        params: The parameters of a model or parameter groups of an optimizer.
    """
    filtered_params = []
    for param in params:
        if isinstance(param, torch.nn.Parameter):
            # model.parameters() input
            param_data = param
            if param_data.grad is not None:
                filtered_params.append(param_data)
        elif isinstance(param, dict):
            # optimizer.param_groups input
            for param_data in param["params"]:
                if param_data.grad is not None:
                    filtered_params.append(param_data)
        else:
            raise NotImplementedError(
                f"Parameter input of type {type(param)} is not supported"
            )
    return filtered_params

