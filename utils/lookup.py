
def lookup(tag: int, group: int | None = None) -> TagInfo:
    """
    :param tag: Integer tag number
    :param group: Which :py:data:`~PIL.TiffTags.TAGS_V2_GROUPS` to look in

    .. versionadded:: 8.3.0

    :returns: Taginfo namedtuple, From the ``TAGS_V2`` info if possible,
        otherwise just populating the value and name from ``TAGS``.
        If the tag is not recognized, "unknown" is returned for the name

    """

    if group is not None:
        info = TAGS_V2_GROUPS[group].get(tag) if group in TAGS_V2_GROUPS else None
    else:
        info = TAGS_V2.get(tag)
    return info or TagInfo(tag, TAGS.get(tag, "unknown"))


def lookup(label):
    """
    Look for an encoding by its label.
    This is the spec’s `get an encoding
    <http://encoding.spec.whatwg.org/#concept-encoding-get>`_ algorithm.
    Supported labels are listed there.

    :param label: A string.
    :returns:
        An :class:`Encoding` object, or :obj:`None` for an unknown label.

    """
    # Only strip ASCII whitespace: U+0009, U+000A, U+000C, U+000D, and U+0020.
    label = ascii_lower(label.strip('\t\n\f\r '))
    name = LABELS.get(label)
    if name is None:
        return None
    encoding = CACHE.get(name)
    if encoding is None:
        if name == 'x-user-defined':
            from .x_user_defined import codec_info
        else:
            python_name = PYTHON_NAMES.get(name, name)
            # Any python_name value that gets to here should be valid.
            codec_info = codecs.lookup(python_name)
        encoding = Encoding(name, codec_info)
        CACHE[name] = encoding
    return encoding


def lookup(obj: Any) -> type[VariableTracker] | None:
    return lookup_inner(obj)


def lookup(
    node: nodes.NodeNG, name: str, context: InferenceContext | None = None
) -> list:
    """Lookup the given special method name in the given *node*.

    If the special method was found, then a list of attributes
    will be returned. Otherwise, `astroid.AttributeInferenceError`
    is going to be raised.
    """
    if isinstance(node, (nodes.List, nodes.Tuple, nodes.Const, nodes.Dict, nodes.Set)):
        return _builtin_lookup(node, name)
    if isinstance(node, astroid.Instance):
        return _lookup_in_mro(node, name)
    if isinstance(node, nodes.ClassDef):
        return _class_lookup(node, name, context=context)

    raise AttributeInferenceError(attribute=name, target=node)

