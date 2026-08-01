
def _is_c_extension(module_node: InferenceResult) -> bool:
    return (
        isinstance(module_node, nodes.Module)
        and not astroid.modutils.is_stdlib_module(module_node.name)
        and not module_node.fully_defined()
    )

