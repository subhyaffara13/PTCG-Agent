
def _nested_select_backward_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")
    grad_output = new_kwargs.pop("grad_output")

    grad_input = torch.zeros_like(inp, dtype=grad_output.dtype)
    grad_input.select(new_kwargs["dim"], new_kwargs["index"]).copy_(grad_output)

    return grad_input

