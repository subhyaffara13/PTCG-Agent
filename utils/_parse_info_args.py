
def _parse_info_args(args):
    """Convert INFO response args to a dict with string keys.

    Handles both RESP2 (flat list) and RESP3 (dict) responses.
    """
    if isinstance(args, dict):
        return {nativestr(k): v for k, v in args.items()}
    return dict(zip(map(nativestr, args[::2]), args[1::2]))

