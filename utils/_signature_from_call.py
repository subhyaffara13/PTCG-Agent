
def _signature_from_call(call: nodes.Call) -> _CallSignature:
    kws = {}
    args = []
    starred_kws = []
    starred_args = []
    for keyword in call.keywords or []:
        arg, value = keyword.arg, keyword.value
        if arg is None and isinstance(value, nodes.Name):
            # Starred node, and we are interested only in names,
            # otherwise some transformation might occur for the parameter.
            starred_kws.append(value.name)
        elif isinstance(value, nodes.Name):
            kws[arg] = value.name
        else:
            kws[arg] = None

    for arg in call.args:
        match arg:
            case nodes.Starred(value=nodes.Name(name=name)):
                # Positional variadic and a name, otherwise some transformation
                # might have occurred.
                starred_args.append(name)
            case nodes.Name():
                args.append(arg.name)
            case _:
                args.append(None)

    return _CallSignature(args, kws, starred_args, starred_kws)

