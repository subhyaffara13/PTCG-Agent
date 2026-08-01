
def impl_arguments(g: NativeFunctionsGroup) -> list[Binding]:
    args: list[Argument | TensorOptionsArguments | SelfArgument] = []

    if g.out.precomputed:
        # A list of parameters for the impl function with
        # certain parameters replaced with precomputed counterparts
        # as specified in native_functions.yaml.
        non_out_args_replaced: list[
            Argument | TensorOptionsArguments | SelfArgument
        ] = []
        for a in g.out.func.arguments.non_out:
            if isinstance(a, Argument) and a.name in g.out.precomputed.replace:
                # If a is in precompute.replace, append the parameters
                # that should replace it onto non_out_args_replaced.
                non_out_args_replaced.extend(g.out.precomputed.replace[a.name])
            else:
                # If not, push a as it is.
                non_out_args_replaced.append(a)

        args.extend(non_out_args_replaced)
        # g.out.precomputed.add is the list of parameters that are added
        # without replacement after the non out args and just before the out args
        args.extend(g.out.precomputed.add)
    else:
        args.extend(g.out.func.arguments.non_out)

    args.extend(g.out.func.arguments.out)
    return [r for arg in args for r in argument(arg)]

