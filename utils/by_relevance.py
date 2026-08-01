
def by_relevance(weak=WEAK_MATCHES, strong=STRONG_MATCHES):
    """
    Create a key function that can be used to sort errors by relevance.

    Arguments:
        weak (set):
            a collection of validation keywords to consider to be
            "weak".  If there are two errors at the same level of the
            instance and one is in the set of weak validation keywords,
            the other error will take priority. By default, :kw:`anyOf`
            and :kw:`oneOf` are considered weak keywords and will be
            superseded by other same-level validation errors.

        strong (set):
            a collection of validation keywords to consider to be
            "strong"

    """

    def relevance(error):
        validator = error.validator
        return (                        # prefer errors which are ...
            -len(error.path),           # 'deeper' and thereby more specific
            error.path,                 # earlier (for sibling errors)
            validator not in weak,      # for a non-low-priority keyword
            validator in strong,        # for a high priority keyword
            not error._matches_type(),  # at least match the instance's type
        )                               # otherwise we'll treat them the same

    return relevance

