
def parse_type_line(type_line, rcb, loc):
    """Parse a type annotation specified as a comment.

    Example inputs:
        # type: (Tensor, torch.Tensor) -> Tuple[Tensor]
        # type: (Tensor, Tuple[Tensor, Tensor]) -> Tensor
    """
    arg_ann_str, ret_ann_str = split_type_line(type_line)

    try:
        arg_ann = _eval_no_call(arg_ann_str, {}, EvalEnv(rcb))
    except (NameError, SyntaxError) as e:
        raise RuntimeError(
            "Failed to parse the argument list of a type annotation"
        ) from e

    if not isinstance(arg_ann, tuple):
        arg_ann = (arg_ann,)

    try:
        ret_ann = _eval_no_call(ret_ann_str, {}, EvalEnv(rcb))
    except (NameError, SyntaxError) as e:
        raise RuntimeError(
            "Failed to parse the return type of a type annotation"
        ) from e

    arg_types = [ann_to_type(ann, loc) for ann in arg_ann]
    return arg_types, ann_to_type(ret_ann, loc)

