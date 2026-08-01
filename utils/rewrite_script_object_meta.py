
def rewrite_script_object_meta(
    gm: torch.fx.GraphModule,
) -> dict[str, _ConstantAttributeType]:
    """When tracing, we produce a graph with FakeScriptObject in the
    meta["val"].

    For now, we rewrie meta["val"] to be a placeholder CustomObjArgument
    """
    constants: dict[
        str,
        _ConstantAttributeType,
    ] = {}
    for node in gm.graph.nodes:
        if "val" not in node.meta:
            continue

        old_meta = node.meta["val"]

        if isinstance(old_meta, torch.ScriptObject):
            class_fqn = old_meta._type().qualified_name()  # type: ignore[attr-defined]
            new_meta = CustomObjArgument(node.name, class_fqn)
            constants[node.name] = old_meta
            node.meta["val"] = new_meta

        elif isinstance(old_meta, FakeScriptObject):
            class_fqn = old_meta.script_class_name  # type: ignore[attr-defined]
            new_meta = CustomObjArgument(node.name, class_fqn, old_meta)
            constants[node.name] = old_meta
            node.meta["val"] = new_meta

    return constants

