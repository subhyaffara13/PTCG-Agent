
def _infer_builtin_container(
    node: nodes.Call,
    context: InferenceContext | None,
    klass: type[nodes.BaseContainer],
    iterables: tuple[type[nodes.NodeNG] | type[ContainerObjects], ...],
    build_elts: BuiltContainers,
) -> nodes.BaseContainer:
    transform_func = partial(
        _container_generic_transform,
        context=context,
        klass=klass,
        iterables=iterables,
        build_elts=build_elts,
    )

    return _container_generic_inference(node, context, klass, transform_func)

