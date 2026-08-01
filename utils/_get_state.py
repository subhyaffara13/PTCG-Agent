
def _get_state(state_class, ops, **options):
    # Try to get a state instance from the operator INSTANCES.
    # If this fails, get the class
    try:
        ret = state_class._operators_to_state(ops, **options)
    except NotImplementedError:
        ret = _make_default(state_class)

    return ret

