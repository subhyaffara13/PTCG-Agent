
def _inherit_constructor_args(name, op, inherited, overrides):
    # inherits metadata
    common_kwargs = {
        "name": name,
        "op": op,
        "aliases": None,  # TODO add a check for alias coverage
        "method_variant": None,
        "inplace_variant": None,  # TODO: add a check for inplace coverage
        "supports_scripting": False,
    }

    # Acquires inherited kwargs
    kwargs = inherited.copy()

    # Fixes metadata
    if "kwargs" in kwargs:
        kwargs.update(kwargs["kwargs"])
        del kwargs["kwargs"]
    if "self" in kwargs:
        del kwargs["self"]
    if "__class__" in kwargs:
        del kwargs["__class__"]
    if "skips" in kwargs:
        del kwargs["skips"]
    if "decorators" in kwargs:
        del kwargs["decorators"]

    # Overrides metadata
    kwargs.update(common_kwargs)
    kwargs.update(overrides)

    # At the moment no prims support autograd, so we must not run autograd
    # tests e.g. when testing dtype support.  Once we start writing autograd
    # formulas for prims this can be removed.
    kwargs["supports_autograd"] = False
    kwargs["supports_gradgrad"] = False
    kwargs["supports_fwgrad_bwgrad"] = False
    kwargs["supports_inplace_autograd"] = False
    kwargs["supports_forward_ad"] = False

    return kwargs

