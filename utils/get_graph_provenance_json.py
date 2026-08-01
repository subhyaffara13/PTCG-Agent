
def get_graph_provenance_json(graph: Graph) -> dict[str, Any]:
    """
    Given an fx.Graph, return a json that contains the provenance information of each node.
    """
    try:
        provenance_tracking_json = {}
        for node in graph.nodes:
            if node.op == "call_function":
                provenance_tracking_json[node.name] = (
                    [source.to_dict() for source in node.meta["from_node"]]
                    if "from_node" in node.meta
                    else []
                )
        return provenance_tracking_json
    except Exception as e:
        # Since this is just debugging, it should never interfere with regular
        # program execution, so we use this try-except to guard against any error
        signpost_event(
            "inductor",
            "provenance_tracking_error",
            {
                "function": "get_graph_provenance_json",
                "error_msg": str(e),
                "stack_trace": traceback.format_exc(),
            },
        )
        return {}

