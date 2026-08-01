
def _container_generic_transform(
    arg: SuccessfulInferenceResult,
    context: InferenceContext | None,
    klass: type[nodes.BaseContainer],
    iterables: tuple[type[nodes.BaseContainer] | type[ContainerObjects], ...],
    build_elts: BuiltContainers,
) -> nodes.BaseContainer | None:
    elts: Iterable | str | bytes

    if isinstance(arg, klass):
        return arg
    if isinstance(arg, iterables):
        arg = cast((nodes.BaseContainer | ContainerObjects), arg)
        if all(isinstance(elt, nodes.Const) for elt in arg.elts):
            elts = [cast(nodes.Const, elt).value for elt in arg.elts]
        else:
            # TODO: Does not handle deduplication for sets.
            elts = []
            for element in arg.elts:
                if not element:
                    continue
                inferred = util.safe_infer(element, context=context)
                if inferred:
                    evaluated_object = nodes.EvaluatedObject(
                        original=element, value=inferred
                    )
                    elts.append(evaluated_object)
    elif isinstance(arg, nodes.Dict):
        # Dicts need to have consts as strings already.
        elts = [
            item[0].value if isinstance(item[0], nodes.Const) else _use_default()
            for item in arg.items
        ]
    elif isinstance(arg, nodes.Const) and isinstance(arg.value, (str, bytes)):
        elts = arg.value
    else:
        return None
    return klass.from_elements(elts=build_elts(elts))

