
def combine_expressions(
    expressions,
    relation="AND",
    unique=True,
    licensing=Licensing(),
):
    """
    Return a combined LicenseExpression object with the `relation`, given a list
    of license ``expressions`` strings or LicenseExpression objects. If
    ``unique`` is True remove duplicates before combining expressions.

    For example::
        >>> a = 'mit'
        >>> b = 'gpl'
        >>> str(combine_expressions([a, b]))
        'mit AND gpl'
        >>> assert 'mit' == str(combine_expressions([a]))
        >>> combine_expressions([])
        >>> combine_expressions(None)
        >>> str(combine_expressions(('gpl', 'mit', 'apache',)))
        'gpl AND mit AND apache'
        >>> str(combine_expressions(('gpl', 'mit', 'apache',), relation='OR'))
        'gpl OR mit OR apache'
        >>> str(combine_expressions(('gpl', 'mit', 'mit',)))
        'gpl AND mit'
        >>> str(combine_expressions(('mit WITH foo', 'gpl', 'mit',)))
        'mit WITH foo AND gpl AND mit'
        >>> str(combine_expressions(('gpl', 'mit', 'mit',), relation='OR', unique=False))
        'gpl OR mit OR mit'
        >>> str(combine_expressions(('mit', 'gpl', 'mit',)))
        'mit AND gpl'
    """
    if not expressions:
        return

    if not isinstance(expressions, (list, tuple)):
        raise TypeError(f"expressions should be a list or tuple and not: {type(expressions)}")

    if not relation or relation.upper() not in (
        "AND",
        "OR",
    ):
        raise TypeError(f"relation should be one of AND, OR and not: {relation}")

    # only deal with LicenseExpression objects
    expressions = [licensing.parse(le, simple=True) for le in expressions]

    if unique:
        # Remove duplicate element in the expressions list
        # and preserve original order
        expressions = list({str(x): x for x in expressions}.values())

    if len(expressions) == 1:
        return expressions[0]

    relation = {"AND": licensing.AND, "OR": licensing.OR}[relation]
    return relation(*expressions)

