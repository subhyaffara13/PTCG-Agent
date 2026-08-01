
def out_arguments(g: NativeFunctionsGroup) -> list[Binding]:
    args: list[Argument | TensorOptionsArguments | SelfArgument] = []
    args.extend(g.out.func.arguments.out)
    return [r for arg in args for r in argument(arg)]

