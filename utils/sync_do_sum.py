
def sync_do_sum(
    environment: "Environment",
    iterable: "t.Iterable[V]",
    attribute: t.Optional[t.Union[str, int]] = None,
    start: V = 0,  # type: ignore
) -> V:
    """Returns the sum of a sequence of numbers plus the value of parameter
    'start' (which defaults to 0).  When the sequence is empty it returns
    start.

    It is also possible to sum up only certain attributes:

    .. sourcecode:: jinja

        Total: {{ items|sum(attribute='price') }}

    .. versionchanged:: 2.6
       The ``attribute`` parameter was added to allow summing up over
       attributes.  Also the ``start`` parameter was moved on to the right.
    """
    if attribute is not None:
        iterable = map(make_attrgetter(environment, attribute), iterable)

    return sum(iterable, start)  # type: ignore[no-any-return, call-overload]

