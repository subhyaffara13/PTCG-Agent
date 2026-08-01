
def attrs_block_plugin(md: MarkdownIt, *, allowed: Sequence[str] | None = None) -> None:
    """Parse block attributes.

    Block attributes are attributes on a single line, with no other content.
    They attach the specified attributes to the block below them::

        {.a #b c=1}
        A paragraph, that will be assigned the class ``a`` and the identifier ``b``.

    Attributes can be stacked, with classes accumulating and lower attributes overriding higher::

        {#a .a c=1}
        {#b .b c=2}
        A paragraph, that will be assigned the class ``a b c``, and the identifier ``b``.

    This syntax is inspired by Djot block attributes.

    :param allowed: A list of allowed attribute names.
        If not ``None``, any attributes not in this list will be removed
        and placed in the token's meta under the key "insecure_attrs".
    """
    md.block.ruler.before("fence", "attr", _attr_block_rule)
    md.core.ruler.after(
        "block",
        "attr",
        partial(
            _attr_resolve_block_rule, allowed=None if allowed is None else set(allowed)
        ),
    )

