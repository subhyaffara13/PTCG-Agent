
def _create_and_access_shape(cls, shape):
    sub = cls(torch.randn(shape))
    # NB: Wrapper subclasses with custom dispatched sizes / strides cache this info
    # on the first call via non-serializable PyCapsules. We purposefully trigger cache
    # population here for serialization / deepcopy tests to verify that the presence of this
    # cache info doesn't cause problems.
    sub.size()
    sub.stride()
    return sub

