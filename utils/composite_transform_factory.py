
def composite_transform_factory(a, b):
    """
    Create a new composite transform that is the result of applying
    transform a then transform b.

    Shortcut versions of the blended transform are provided for the
    case where both child transforms are affine, or one or the other
    is the identity transform.

    Composite transforms may also be created using the '+' operator,
    e.g.::

      c = a + b
    """
    # check to see if any of a or b are IdentityTransforms. We use
    # isinstance here to guarantee that the transforms will *always*
    # be IdentityTransforms. Since TransformWrappers are mutable,
    # use of equality here would be wrong.
    if isinstance(a, IdentityTransform):
        return b
    elif isinstance(b, IdentityTransform):
        return a
    elif isinstance(a, Affine2D) and isinstance(b, Affine2D):
        return CompositeAffine2D(a, b)
    return CompositeGenericTransform(a, b)

