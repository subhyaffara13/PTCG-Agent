from typing import Any

def clone_inputs(
    example_inputs: dict[str, T | tuple[T, ...]],
) -> dict[str, list[T]]: ...


def clone_inputs(example_inputs: Sequence[T]) -> list[T]: ...


def clone_inputs(example_inputs: Any) -> Any:
    res: dict[str, Any] | list[Any]
    if type(example_inputs) is dict:
        res = dict(example_inputs)
        for key, value in res.items():
            if isinstance(value, tuple):
                res[key] = clone_inputs(value)
            else:
                assert isinstance(value, torch.Tensor), type(value)
                res[key] = clone_input(value)
        return res

    res = list(example_inputs)
    for i in range(len(res)):
        if isinstance(res[i], torch.Tensor):
            res[i] = clone_input(res[i])
    return res


def clone_inputs(args: Iterable[Any]) -> list[Any]:
    inputs: list[Any] = []

    for arg in args:
        if isinstance(arg, torch.Tensor):
            inputs.append(arg.detach().clone())
        elif is_iterable_of_tensors(arg):
            inputs.append([t.detach().clone() for t in arg])
        else:
            inputs.append(arg)

    return inputs


def clone_inputs(args):
    inputs: list[torch.Tensor | list[torch.Tensor]] = []

    for arg in args:
        if isinstance(arg, torch.Tensor):
            inputs.append(arg.detach().clone())
        elif is_iterable_of_tensors(arg):
            inputs.append([t.detach().clone() for t in arg])
        else:
            inputs.append(arg)

    return inputs

