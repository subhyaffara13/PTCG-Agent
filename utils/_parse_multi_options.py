
def _parse_multi_options(options, split_token=','):
    r"""Split and strip and discard empties.

    Turns the following:

    A,
    B,

    into ["A", "B"]
    """
    if options:
        return [o.strip() for o in options.split(split_token) if o.strip()]
    else:
        return options

