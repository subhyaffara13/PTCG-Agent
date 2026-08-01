
def _transform_to_stack(constraint):
    return transforms.StackTransform(
        [transform_to(c) for c in constraint.cseq], constraint.dim
    )

