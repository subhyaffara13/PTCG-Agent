
def _transform_to_interval(constraint):
    # Handle the special case of the unit interval.
    lower_is_0 = (
        isinstance(constraint.lower_bound, _Number) and constraint.lower_bound == 0
    )
    upper_is_1 = (
        isinstance(constraint.upper_bound, _Number) and constraint.upper_bound == 1
    )
    if lower_is_0 and upper_is_1:
        return transforms.SigmoidTransform()

    loc = constraint.lower_bound
    scale = constraint.upper_bound - constraint.lower_bound
    return transforms.ComposeTransform(
        [transforms.SigmoidTransform(), transforms.AffineTransform(loc, scale)]
    )

