
def normalized(normalize):
    r"""Set flag controlling normalization of Hadamard gates by `1/\sqrt{2}`.

    This is a global setting that can be used to simplify the look of various
    expressions, by leaving off the leading `1/\sqrt{2}` of the Hadamard gate.

    Parameters
    ----------
    normalize : bool
        Should the Hadamard gate include the `1/\sqrt{2}` normalization factor?
        When True, the Hadamard gate will have the `1/\sqrt{2}`. When False, the
        Hadamard gate will not have this factor.
    """
    global _normalized
    _normalized = normalize

