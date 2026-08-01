
def do_last(
    environment: "Environment", seq: "t.Reversible[V]"
) -> "t.Union[V, Undefined]":
    """Return the last item of a sequence.

    Note: Does not work with generators. You may want to explicitly
    convert it to a list:

    .. sourcecode:: jinja

        {{ data | selectattr('name', '==', 'Jinja') | list | last }}
    """
    try:
        return next(iter(reversed(seq)))
    except StopIteration:
        return environment.undefined("No last item, sequence was empty.")

