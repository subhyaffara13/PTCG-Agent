
def _check_valid_flat_script_obj(flat_x):
    if not isinstance(flat_x, tuple):
        raise RuntimeError("Expect flat x to be a tuple.")

    for tp in flat_x:
        if not isinstance(tp, tuple):
            raise RuntimeError("Expect flat x to be a tuple of tuples.")

        if not len(tp) == 2 or not isinstance(tp[0], str):
            raise RuntimeError(
                "Expect element of flat x to be a tuple of two elements with first element being a string"
            )

