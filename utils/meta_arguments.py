
def meta_arguments(g: NativeFunctionsGroup) -> list[Binding]:
    args: list[Argument | TensorOptionsArguments | SelfArgument] = []
    args.extend(g.functional.func.arguments.non_out)
    return [r for arg in args for r in argument(arg)]

