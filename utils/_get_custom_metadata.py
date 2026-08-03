from typing import Any

def _get_custom_metadata(gm: GraphModule) -> str:
    if not isinstance(gm, GraphModule):
        raise AssertionError(f"Expected GraphModule, got {type(gm)}")

    def helper(gm: GraphModule) -> list[Any]:
        custom_metadata = []
        for node in gm.graph.nodes:
            if hasattr(node, "meta") and node.meta.get("custom", None):
                custom_metadata.append((node.op, node.name, node.meta["custom"]))
            if node.op == "get_attr" and isinstance(
                getattr(gm, node.target), GraphModule
            ):
                custom_metadata.append(
                    # pyrefly: ignore[bad-argument-type]
                    helper(getattr(gm, node.target))
                )
        return custom_metadata

    return "\n".join(str(x) for x in helper(gm))

