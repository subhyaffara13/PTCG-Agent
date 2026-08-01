
def clean_nn_module_stack_and_source_fn(
    graph_module: torch.fx.GraphModule, is_inline_builtin: bool = False
) -> torch.fx.GraphModule:
    """
    Clean up nn_module_stack metadata by removing export_root references.

    Removes the _export_root module references from nn_module_stack metadata
    in graph nodes, which are artifacts from the export process. Fixes two patterns:

    1. Keys: Removes "__export_root_" and "__modules['_export_root']_" prefixes
       - Normal case: "L__self____export_root_child" -> "L__self__child"
       - inline_builtin case: Uses numeric ID strings like "140468831433840"

    2. Values: Removes "._export_root" and "._modules['_export_root']" from child names
       e.g., "L['self']._export_root.child" -> "L['self'].child"
       e.g., "L['self']._modules['_export_root'].child" -> "L['self'].child"

    Also removes the root export entry "L__self____export_root" entirely.

    Args:
        graph_module: The GraphModule to clean up
        is_inline_builtin: If True, keys are numeric ID strings and self references
                          (L['self']) are filtered out

    Returns:
        The cleaned GraphModule (modified in-place)
    """

    def _process_nn_module_stack(
        nn_module_stack: dict[str, tuple[str, T]],
    ) -> dict[str, tuple[str, T]]:
        if "L__self____export_root" in nn_module_stack:
            del nn_module_stack["L__self____export_root"]

        # Clean up remaining entries
        cleaned_stack = {}
        for key, (child_name, child_class) in nn_module_stack.items():
            # Clean key by removing export_root patterns
            clean_key = clean_export_root_string(key)

            # Clean child_name by removing export_root patterns
            clean_name = clean_export_root_string(child_name)

            # Skip self reference for inline builtin case
            if is_inline_builtin and clean_name == "L['self']":
                continue

            cleaned_stack[clean_key] = (clean_name, child_class)
        return cleaned_stack

    def _process_source_fn(source_fn_stack: Iterable[T]) -> Iterable[T]:
        cleaned_stack = []
        for item in source_fn_stack:
            if isinstance(item, tuple) and len(item) == 2:
                name, cls = item
                if isinstance(name, str):
                    clean_name = clean_export_root_string(name)
                    cleaned_stack.append((clean_name, cls))
                else:
                    cleaned_stack.append(item)
            else:
                # pyrefly: ignore [bad-argument-type]
                cleaned_stack.append(item)
        # pyrefly: ignore [bad-return]
        return cleaned_stack

    for node in graph_module.graph.nodes:
        if "nn_module_stack" in node.meta:
            node.meta["nn_module_stack"] = _process_nn_module_stack(
                node.meta["nn_module_stack"].copy()
            )

        source_fn_stack = node.meta.get("source_fn_stack", None)
        if source_fn_stack:
            node.meta["source_fn_stack"] = _process_source_fn(source_fn_stack.copy())

    if "dynamo_flat_name_to_original_fqn" in graph_module.meta:
        # Clean up flat name to original fqn mapping
        clean_name_to_original_fqn = {}
        for flat_name, original_fqn in graph_module.meta[
            "dynamo_flat_name_to_original_fqn"
        ].items():
            clean_name_to_original_fqn[clean_export_root_string(flat_name)] = (
                clean_export_root_string(original_fqn)
            )
        graph_module.meta["dynamo_flat_name_to_original_fqn"] = (
            clean_name_to_original_fqn
        )

    return graph_module

