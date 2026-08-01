
def _get_custom_obj_for_node(node, inputs_to_lifted_custom_objs, constants):
    """Extract the custom object from a node's arguments."""
    custom_obj_node = node
    custom_obj_meta = custom_obj_node.meta["val"]  # type: ignore[union-attr]
    if not isinstance(custom_obj_meta, CustomObjArgument):
        raise AssertionError(
            f"Expected custom_obj_meta to be a CustomObjArgument, but got {type(custom_obj_meta)}"
        )

    if custom_obj_meta.fake_val:
        return custom_obj_meta.fake_val
    elif custom_obj_node.name in inputs_to_lifted_custom_objs:  # type: ignore[union-attr]
        return constants[inputs_to_lifted_custom_objs[custom_obj_node.name]]  # type: ignore[union-attr]
    else:
        raise RuntimeError(f"Unable to find custom obj for node {node}")

