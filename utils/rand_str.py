
def rand_str(nchars: int) -> str:
    """
    Generate one random byte string.
    """
    RANDS_CHARS = np.array(
        list(string.ascii_letters + string.digits), dtype=(np.str_, 1)
    )
    return "".join(np.random.default_rng(2).choice(RANDS_CHARS, nchars))

