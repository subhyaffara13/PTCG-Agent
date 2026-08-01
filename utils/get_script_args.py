
def get_script_args(args):
    formals: list[str] = []
    tensors: list[torch.Tensor | list[torch.Tensor]] = []
    actuals: list[str] = []
    for arg in args:
        if isinstance(arg, torch.Tensor):
            name = f'i{len(formals)}'
            formals.append(name)
            actuals.append(name)
            tensors.append(arg)
        elif is_iterable_of_tensors(arg):
            name = f'i{len(formals)}'
            formals.append(name + ': List[torch.Tensor]')
            actuals.append(name)
            tensors.append(list(arg))
        elif isinstance(arg, str):
            actuals.append(f"'{arg}'")
        else:
            actuals.append(str(get_constant(arg)))
    return (formals, tensors, actuals)

