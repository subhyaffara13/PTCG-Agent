
def _annotations_list(args_node: nodes.Arguments) -> list[nodes.NodeNG]:
    """Get a merged list of annotations.

    The annotations can come from:

    * Real type annotations.
    * A type comment on the function.
    * A type common on the individual argument.

    :param args_node: The node to get the annotations for.
    :returns: The annotations.
    """
    plain_annotations = args_node.annotations or ()
    func_comment_annotations = args_node.parent.type_comment_args or ()
    comment_annotations = args_node.type_comment_posonlyargs
    comment_annotations += args_node.type_comment_args or []
    comment_annotations += args_node.type_comment_kwonlyargs
    return list(
        _merge_annotations(
            plain_annotations,
            _merge_annotations(func_comment_annotations, comment_annotations),
        )
    )

