
def getKnownTagIndex(tag):
    """Return index of 'tag' in woff2KnownTags list. Return 63 if not found."""
    try:
        return woff2KnownTags.index(tag)
    except ValueError:
        return woff2UnknownTagIndex

