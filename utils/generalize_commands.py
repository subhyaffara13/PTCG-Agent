
def generalizeCommands(commands, ignoreErrors=False):
    result = []
    mapping = _GeneralizerDecombinerCommandsMap
    for op, args in commands:
        # First, generalize any blend args in the arg list.
        if any([isinstance(arg, list) for arg in args]):
            try:
                args = [
                    n
                    for arg in args
                    for n in (
                        _convertBlendOpToArgs(arg) if isinstance(arg, list) else [arg]
                    )
                ]
            except ValueError:
                if ignoreErrors:
                    # Store op as data, such that consumers of commands do not have to
                    # deal with incorrect number of arguments.
                    result.append(("", args))
                    result.append(("", [op]))
                else:
                    raise

        func = getattr(mapping, op, None)
        if func is None:
            result.append((op, args))
            continue
        try:
            for command in func(args):
                result.append(command)
        except ValueError:
            if ignoreErrors:
                # Store op as data, such that consumers of commands do not have to
                # deal with incorrect number of arguments.
                result.append(("", args))
                result.append(("", [op]))
            else:
                raise
    return result

