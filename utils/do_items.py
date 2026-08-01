
def do_items(value: t.Union[t.Mapping[K, V], Undefined]) -> t.Iterator[t.Tuple[K, V]]:
    """Return an iterator over the ``(key, value)`` items of a mapping.

    ``x|items`` is the same as ``x.items()``, except if ``x`` is
    undefined an empty iterator is returned.

    This filter is useful if you expect the template to be rendered with
    an implementation of Jinja in another programming language that does
    not have a ``.items()`` method on its mapping type.

    .. code-block:: html+jinja

        <dl>
        {% for key, value in my_dict|items %}
            <dt>{{ key }}
            <dd>{{ value }}
        {% endfor %}
        </dl>

    .. versionadded:: 3.1
    """
    if isinstance(value, Undefined):
        return

    if not isinstance(value, abc.Mapping):
        raise TypeError("Can only get item pairs from a mapping.")

    yield from value.items()

