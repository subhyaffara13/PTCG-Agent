
def _transform_to_less_than(constraint):
    return transforms.ComposeTransform(
        [
            transforms.ExpTransform(),
            transforms.AffineTransform(constraint.upper_bound, -1),
        ]
    )

