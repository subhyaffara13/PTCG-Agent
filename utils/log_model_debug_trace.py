import json
import os

def log_model_debug_trace(debug_path: str | None, model):
    if debug_path:
        try:
            os.makedirs(debug_path, exist_ok=True)
            base = os.path.join(debug_path, model._debugger_module_dump_name + "_debug_tree")
        except Exception as e:
            raise ValueError(f"Unexpected or existing debug_path={debug_path}.") from e
    else:
        base = model._debugger_module_dump_name + "_debug_tree"

    logger.info(f"Writing model trace at {base}.json")
    full_path = base + "_FULL_TENSORS.json"
    summary_path = base + "_SUMMARY.json"

    prune_outputs_if_children(model._call_tree)

    with open(full_path, "w") as f:
        json.dump(model._call_tree, f, indent=2)

    # summary-only version for readability - traversing the tree again #TODO optimize?
    def strip_values(node):
        def clean(val):
            if isinstance(val, dict):
                val.pop("value", None)
                for v in val.values():
                    clean(v)
            elif isinstance(val, list):
                for item in val:
                    clean(item)

        clean(node.get("inputs", {}))
        clean(node.get("outputs", {}))

        for child in node.get("children", []):
            strip_values(child)

    tree_copy = json.loads(json.dumps(model._call_tree))  # deep copy
    strip_values(tree_copy)

    with open(summary_path, "w") as f:
        json.dump(tree_copy, f, indent=2)

