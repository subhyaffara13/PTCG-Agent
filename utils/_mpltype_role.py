
def _mpltype_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """
    Sphinx role ``:mpltype:`` for custom matplotlib types.

    In Matplotlib, there are a number of type-like concepts that do not have a
    direct type representation; example: color. This role allows to properly
    highlight them in the docs and link to their definition.

    Currently supported values:

    - :code:`:mpltype:`color`` will render as: :mpltype:`color`

    """
    mpltype = text
    type_to_link_target = {
        'color': 'colors_def',
        'hatch': 'hatch_def',
    }
    if mpltype not in type_to_link_target:
        raise ValueError(f"Unknown mpltype: {mpltype!r}")

    node_list, messages = inliner.interpreted(
        mpltype, f'{mpltype} <{type_to_link_target[mpltype]}>', 'ref', lineno)
    return node_list, messages

