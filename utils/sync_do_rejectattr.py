
def sync_do_rejectattr(
    context: "Context", value: "t.Iterable[V]", *args: t.Any, **kwargs: t.Any
) -> "t.Iterator[V]":
    """Filters a sequence of objects by applying a test to the specified
    attribute of each object, and rejecting the objects with the test
    succeeding.

    If no test is specified, the attribute's value will be evaluated as
    a boolean.

    .. sourcecode:: jinja

        {{ users|rejectattr("is_active") }}
        {{ users|rejectattr("email", "none") }}

    Similar to a generator comprehension such as:

    .. code-block:: python

        (user for user in users if not user.is_active)
        (user for user in users if not test_none(user.email))

    .. versionadded:: 2.7
    """
    return select_or_reject(context, value, args, kwargs, lambda x: not x, True)

