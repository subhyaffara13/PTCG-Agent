
def check_inputs_type(args, kwargs):
    if not isinstance(args, tuple):
        raise ValueError(
            f"Expecting args type to be a tuple, got: {type(args)}"
        )
    if not isinstance(kwargs, dict):
        raise ValueError(
            f"Expecting kwargs type to be a dict, got: {type(kwargs)}"
        )
    for key in kwargs:
        if not isinstance(key, str):
            raise ValueError(
                f"Expecting kwargs keys to be a string, got: {type(key)}"
            )

