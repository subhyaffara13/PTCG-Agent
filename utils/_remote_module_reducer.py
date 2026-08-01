
def _remote_module_reducer(remote_module):
    """Serialize a RemoteModule."""
    pickled_attrs = {}
    for k, v in remote_module.__dict__.items():
        # Pickling the attribute `module_rref` must invoke RRef's `_serialize()` method.
        if k == "module_rref":
            pickled_attrs[k] = v._serialize()
        elif k in _REMOTE_MODULE_PICKLED_ATTRIBUTES:
            pickled_attrs[k] = v
        # Check if unpickled attributes are all in _REMOTE_MODULE_ATTRIBUTES_IGNORE_FOR_PICKLING.
        elif k not in _REMOTE_MODULE_ATTRIBUTES_IGNORE_FOR_PICKLING:
            print(
                f"The new attribute ``{k}`` of RemoteModule is ignored during RPC pickling. "
                "To pickle this attribute, please add it to ``_REMOTE_MODULE_PICKLED_ATTRIBUTES``. "
                "Otherwise, please explicitly add it to ``_REMOTE_MODULE_ATTRIBUTES_IGNORE_FOR_PICKLING``.",
                file=sys.stderr,
            )

    return (
        _remote_module_receiver,
        tuple(pickled_attrs.values()),
    )

