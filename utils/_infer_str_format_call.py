
def _infer_str_format_call(
    node: nodes.Call, context: InferenceContext | None = None, **kwargs: Any
) -> Iterator[ConstFactoryResult | util.UninferableBase]:
    """Return a Const node based on the template and passed arguments."""
    call = arguments.CallSite.from_call(node, context=context)
    assert isinstance(node.func, (nodes.Attribute, nodes.AssignAttr, nodes.DelAttr))

    value: nodes.Const
    if isinstance(node.func.expr, nodes.Name):
        if not (
            (inferred := util.safe_infer(node.func.expr))
            and isinstance(inferred, nodes.Const)
        ):
            return iter([util.Uninferable])
        value = inferred
    elif isinstance(node.func.expr, nodes.Const):
        value = node.func.expr
    else:  # pragma: no cover
        return iter([util.Uninferable])

    format_template = value.value

    # Get the positional arguments passed
    inferred_positional: list[nodes.Const] = []
    for i in call.positional_arguments:
        one_inferred = util.safe_infer(i, context)
        if not isinstance(one_inferred, nodes.Const):
            return iter([util.Uninferable])
        inferred_positional.append(one_inferred)

    pos_values: list[str] = [i.value for i in inferred_positional]

    # Get the keyword arguments passed
    inferred_keyword: dict[str, nodes.Const] = {}
    for k, v in call.keyword_arguments.items():
        one_inferred = util.safe_infer(v, context)
        if not isinstance(one_inferred, nodes.Const):
            return iter([util.Uninferable])
        inferred_keyword[k] = one_inferred

    keyword_values: dict[str, str] = {k: v.value for k, v in inferred_keyword.items()}

    try:
        formatted_string = format_template.format(*pos_values, **keyword_values)
    except (AttributeError, IndexError, KeyError, TypeError, ValueError):
        # AttributeError: named field in format string was not found in the arguments
        # IndexError: there are too few arguments to interpolate
        # TypeError: Unsupported format string
        # ValueError: Unknown format code
        return iter([util.Uninferable])

    return iter([nodes.const_factory(formatted_string)])

