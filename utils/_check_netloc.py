
def _check_netloc(netloc: str) -> None:
    # Adapted from urllib.parse._checknetloc
    # looking for characters like \u2100 that expand to 'a/c'
    # IDNA uses NFKC equivalence, so normalize for this check

    # ignore characters already included
    # but not the surrounding text
    n = netloc.replace("@", "").replace(":", "").replace("#", "").replace("?", "")
    normalized_netloc = unicodedata.normalize("NFKC", n)
    if n == normalized_netloc:
        return
    # Note that there are no unicode decompositions for the character '@' so
    # its currently impossible to have test coverage for this branch, however if the
    # one should be added in the future we want to make sure its still checked.
    for c in "/?#@:":  # pragma: no branch
        if c in normalized_netloc:
            raise ValueError(
                f"netloc '{netloc}' contains invalid "
                "characters under NFKC normalization"
            )

