
def get_annotation_label(ann: nodes.Name | nodes.NodeNG) -> str:
    if isinstance(ann, nodes.Name) and ann.name is not None:
        return ann.name  # type: ignore[no-any-return]
    if isinstance(ann, nodes.NodeNG):
        return ann.as_string()  # type: ignore[no-any-return]
    return ""

