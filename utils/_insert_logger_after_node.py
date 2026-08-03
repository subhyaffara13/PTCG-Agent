from typing import Callable

def _insert_logger_after_node(
    node: Node,
    gm: GraphModule,
    logger_cls: Callable,
    logger_node_name_suffix: str,
    ref_node_name: str,
    model_name: str,
    ref_name: str,
    ref_node_target_type: str,
    results_type: str,
    index_within_arg: int,
    index_of_arg: int,
    fqn: str | None,
) -> Node:
    """
    Given a starting graph of

    prev_node -> node -> next_node

    This function creates a new logger_cls obj and adds it
    after node, resulting in

    prev_node -> node -> logger_obj -> next_node
    """
    # create new name
    logger_node_name = get_new_attr_name_with_prefix(
        node.name + logger_node_name_suffix
    )(gm)
    target_type = get_target_type_str(node, gm)
    # create the logger object
    logger_obj = logger_cls(
        ref_node_name,
        node.name,
        model_name,
        ref_name,
        target_type,
        ref_node_target_type,
        results_type,
        index_within_arg,
        index_of_arg,
        fqn,
    )
    # attach the logger object to the parent module
    setattr(gm, logger_node_name, logger_obj)
    logger_node = node.graph.create_node("call_module", logger_node_name, (node,), {})
    return logger_node

