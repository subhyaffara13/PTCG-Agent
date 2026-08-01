
def _forbid_class_getitem_access(node: nodes.ClassDef) -> None:
    """Disable the access to __class_getitem__ method for the node in parameters."""

    def full_raiser(origin_func, attr, *args, **kwargs):
        """
        Raises an AttributeInferenceError in case of access to __class_getitem__ method.
        Otherwise, just call origin_func.
        """
        if attr == "__class_getitem__":
            raise AttributeInferenceError("__class_getitem__ access is not allowed")
        return origin_func(attr, *args, **kwargs)

    try:
        node.getattr("__class_getitem__")
        # If we are here, then we are sure to modify an object that does have
        # __class_getitem__ method (which origin is the protocol defined in
        # collections module) whereas the typing module considers it should not.
        # We do not want __class_getitem__ to be found in the classdef
        partial_raiser = partial(full_raiser, node.getattr)
        node.getattr = partial_raiser
    except AttributeInferenceError:
        pass

