
def args_with_annotation(args_node: nodes.Arguments) -> set[str]:
    result = set()
    annotations = _annotations_list(args_node)
    annotation_offset = 0

    if args_node.posonlyargs:
        posonlyargs_annotations = args_node.posonlyargs_annotations
        if not any(args_node.posonlyargs_annotations):
            num_args = len(args_node.posonlyargs)
            posonlyargs_annotations = annotations[
                annotation_offset : annotation_offset + num_args
            ]
            annotation_offset += num_args

        for arg, annotation in zip(args_node.posonlyargs, posonlyargs_annotations):
            if annotation:
                result.add(arg.name)

    if args_node.args:
        num_args = len(args_node.args)
        for arg, annotation in zip(
            args_node.args,
            annotations[annotation_offset : annotation_offset + num_args],
        ):
            if annotation:
                result.add(arg.name)

        annotation_offset += num_args

    if args_node.vararg:
        if args_node.varargannotation:
            result.add(args_node.vararg)
        elif len(annotations) > annotation_offset and annotations[annotation_offset]:
            result.add(args_node.vararg)
            annotation_offset += 1

    if args_node.kwonlyargs:
        kwonlyargs_annotations = args_node.kwonlyargs_annotations
        if not any(args_node.kwonlyargs_annotations):
            num_args = len(args_node.kwonlyargs)
            kwonlyargs_annotations = annotations[
                annotation_offset : annotation_offset + num_args
            ]
            annotation_offset += num_args

        for arg, annotation in zip(args_node.kwonlyargs, kwonlyargs_annotations):
            if annotation:
                result.add(arg.name)

    if args_node.kwarg:
        if args_node.kwargannotation:
            result.add(args_node.kwarg)
        elif len(annotations) > annotation_offset and annotations[annotation_offset]:
            result.add(args_node.kwarg)
            annotation_offset += 1

    return result

