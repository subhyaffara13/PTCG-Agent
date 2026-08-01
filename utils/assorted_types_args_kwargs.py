
def assorted_types_args_kwargs(
    tensor_arg: Tensor,  # noqa: E999
    str_arg: str,
    int_arg: int,
    tensor_kwarg: Tensor = torch.tensor([2, 2]),
    str_kwarg: str = "str_kwarg",
    int_kwarg: int = 2,
):
    return tensor_arg + tensor_kwarg, str_arg + str_kwarg, int_arg + int_kwarg

