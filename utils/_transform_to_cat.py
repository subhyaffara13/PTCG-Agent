
def _transform_to_cat(constraint):
    return transforms.CatTransform(
        [transform_to(c) for c in constraint.cseq], constraint.dim, constraint.lengths
    )

