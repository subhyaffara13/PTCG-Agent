
def _transform_to_greater_than(constraint):
    return transforms.ComposeTransform(
        [
            transforms.ExpTransform(),
            transforms.AffineTransform(constraint.lower_bound, 1),
        ]
    )

