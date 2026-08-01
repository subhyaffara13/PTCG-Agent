
def _merge_annotations(
    annotations: Iterable[nodes.NodeNG], comment_annotations: Iterable[nodes.NodeNG]
) -> Iterable[nodes.NodeNG | None]:
    for ann, comment_ann in itertools.zip_longest(annotations, comment_annotations):
        if ann and not _is_ellipsis(ann):
            yield ann
        elif comment_ann and not _is_ellipsis(comment_ann):
            yield comment_ann
        else:
            yield None

