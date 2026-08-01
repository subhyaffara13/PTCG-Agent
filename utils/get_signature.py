
def get_signature(fn, rcb, loc, is_method):
    if isinstance(fn, OpOverloadPacket):
        signature = try_real_annotations(fn.op, loc)
    else:
        signature = try_real_annotations(fn, loc)
    if signature is not None and is_method:
        # If this is a method, then the signature will include a type for
        # `self`, but type comments do not contain a `self`. So strip it
        # away here so everything is consistent (`inspect.ismethod` does
        # not work here since `fn` is unbound at this point)
        param_types, return_type = signature
        param_types = param_types[1:]
        signature = (param_types, return_type)

    if signature is None:
        type_line, source = None, None
        try:
            source = dedent("".join(get_source_lines_and_file(fn)[0]))
            type_line = get_type_line(source)
        except TypeError:
            pass
        # This might happen both because we failed to get the source of fn, or
        # because it didn't have any annotations.
        if type_line is not None:
            signature = parse_type_line(type_line, rcb, loc)

    return signature

