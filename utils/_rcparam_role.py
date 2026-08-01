
def _rcparam_role(name, rawtext, text, lineno, inliner, options=None, content=None):
    """
    Sphinx role ``:rc:`` to highlight and link ``rcParams`` entries.

    Usage: Give the desired ``rcParams`` key as parameter.

    :code:`:rc:`figure.dpi`` will render as: :rc:`figure.dpi`
    """
    # Generate a pending cross-reference so that Sphinx will ensure this link
    # isn't broken at some point in the future.
    title = f'rcParams["{text}"]'
    rc_param_name = _RC_WILDCARD_LINK_MAPPING.get(text, text)
    target = f'rcparam_{rc_param_name.replace(".", "_")}'
    ref_nodes, messages = inliner.interpreted(title, f'{title} <{target}>',
                                              'ref', lineno)

    qr = _QueryReference(rawtext, highlight=text)
    qr += ref_nodes
    node_list = [qr]

    # The default backend would be printed as "agg", but that's not correct (as
    # the default is actually determined by fallback).
    if text in rcParamsDefault and text != "backend":
        node_list.extend([
            nodes.Text(' (default: '),
            nodes.literal('', repr(rcParamsDefault[text])),
            nodes.Text(')'),
            ])

    return node_list, messages

