
def attrs_plugin(
    md: MarkdownIt,
    *,
    after: Sequence[str] = ("image", "code_inline", "link_close", "span_close"),
    spans: bool = False,
    span_after: str = "link",
    allowed: Sequence[str] | None = None,
) -> None:
    """Parse inline attributes that immediately follow certain inline elements::

        ![alt](https://image.com){#id .a b=c}

    This syntax is inspired by
    `Djot spans
    <https://htmlpreview.github.io/?https://github.com/jgm/djot/blob/master/doc/syntax.html#inline-attributes>`_.

    Inside the curly braces, the following syntax is possible:

    - `.foo` specifies foo as a class.
      Multiple classes may be given in this way; they will be combined.
    - `#foo` specifies foo as an identifier.
      An element may have only one identifier;
      if multiple identifiers are given, the last one is used.
    - `key="value"` or `key=value` specifies a key-value attribute.
       Quotes are not needed when the value consists entirely of
       ASCII alphanumeric characters or `_` or `:` or `-`.
       Backslash escapes may be used inside quoted values.
    - `%` begins a comment, which ends with the next `%` or the end of the attribute (`}`).

    Multiple attribute blocks are merged.

    :param md: The MarkdownIt instance to modify.
    :param after: The names of inline elements after which attributes may be specified.
        This plugin does not support attributes after emphasis, strikethrough or text elements,
        which all require post-parse processing.
    :param spans: If True, also parse attributes after spans of text, encapsulated by `[]`.
        Note Markdown link references take precedence over this syntax.
    :param span_after: The name of an inline rule after which spans may be specified.
    :param allowed: A list of allowed attribute names.
        If not ``None``, any attributes not in this list will be removed
        and placed in the token's meta under the key "insecure_attrs".
    """

    if spans:
        md.inline.ruler.after(span_after, "span", _span_rule)
    if after:
        md.inline.ruler.push(
            "attr",
            partial(
                _attr_inline_rule,
                after=after,
                allowed=None if allowed is None else set(allowed),
            ),
        )

