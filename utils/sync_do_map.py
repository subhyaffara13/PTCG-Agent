
def sync_do_map(
    context: "Context",
    value: t.Iterable[t.Any],
    name: str,
    *args: t.Any,
    **kwargs: t.Any,
) -> t.Iterable[t.Any]: ...


def sync_do_map(
    context: "Context",
    value: t.Iterable[t.Any],
    *,
    attribute: str = ...,
    default: t.Optional[t.Any] = None,
) -> t.Iterable[t.Any]: ...


def sync_do_map(
    context: "Context", value: t.Iterable[t.Any], *args: t.Any, **kwargs: t.Any
) -> t.Iterable[t.Any]:
    """Applies a filter on a sequence of objects or looks up an attribute.
    This is useful when dealing with lists of objects but you are really
    only interested in a certain value of it.

    The basic usage is mapping on an attribute.  Imagine you have a list
    of users but you are only interested in a list of usernames:

    .. sourcecode:: jinja

        Users on this page: {{ users|map(attribute='username')|join(', ') }}

    You can specify a ``default`` value to use if an object in the list
    does not have the given attribute.

    .. sourcecode:: jinja

        {{ users|map(attribute="username", default="Anonymous")|join(", ") }}

    Alternatively you can let it invoke a filter by passing the name of the
    filter and the arguments afterwards.  A good example would be applying a
    text conversion filter on a sequence:

    .. sourcecode:: jinja

        Users on this page: {{ titles|map('lower')|join(', ') }}

    Similar to a generator comprehension such as:

    .. code-block:: python

        (u.username for u in users)
        (getattr(u, "username", "Anonymous") for u in users)
        (do_lower(x) for x in titles)

    .. versionchanged:: 2.11.0
        Added the ``default`` parameter.

    .. versionadded:: 2.7
    """
    if value:
        func = prepare_map(context, args, kwargs)

        for item in value:
            yield func(item)

