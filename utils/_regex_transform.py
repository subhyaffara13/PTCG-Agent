
def _regex_transform() -> nodes.Module:
    """The RegexFlag enum exposes all its entries by updating globals().

    We hard-code the flags for now.
    # pylint: disable-next=line-too-long
    See https://github.com/mrabarnett/mrab-regex/blob/2022.10.31/regex_3/regex.py#L200
    """
    return parse(
        """
    A = ASCII = 0x80          # Assume ASCII locale.
    B = BESTMATCH = 0x1000    # Best fuzzy match.
    D = DEBUG = 0x200         # Print parsed pattern.
    E = ENHANCEMATCH = 0x8000 # Attempt to improve the fit after finding the first
                              # fuzzy match.
    F = FULLCASE = 0x4000     # Unicode full case-folding.
    I = IGNORECASE = 0x2      # Ignore case.
    L = LOCALE = 0x4          # Assume current 8-bit locale.
    M = MULTILINE = 0x8       # Make anchors look for newline.
    P = POSIX = 0x10000       # POSIX-style matching (leftmost longest).
    R = REVERSE = 0x400       # Search backwards.
    S = DOTALL = 0x10         # Make dot match newline.
    U = UNICODE = 0x20        # Assume Unicode locale.
    V0 = VERSION0 = 0x2000    # Old legacy behaviour.
    DEFAULT_VERSION = V0
    V1 = VERSION1 = 0x100     # New enhanced behaviour.
    W = WORD = 0x800          # Default Unicode word breaks.
    X = VERBOSE = 0x40        # Ignore whitespace and comments.
    T = TEMPLATE = 0x1        # Template (present because re module has it).
    """
    )

