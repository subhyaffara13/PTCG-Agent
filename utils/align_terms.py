
def align_terms(terms):
    """
    Align a set of terms.
    """
    try:
        # flatten the parse tree (a nested list, really)
        terms = list(com.flatten(terms))
    except TypeError:
        # can't iterate so it must just be a constant or single variable
        if isinstance(terms.value, (ABCSeries, ABCDataFrame)):
            typ = type(terms.value)
            name = terms.value.name if isinstance(terms.value, ABCSeries) else None
            return typ, _zip_axes_from_type(typ, terms.value.axes), name
        return np.result_type(terms.type), None, None

    # if all resolved variables are numeric scalars
    if all(term.is_scalar for term in terms):
        return result_type_many(*(term.value for term in terms)).type, None, None

    # if all input series have a common name, propagate it to the returned series
    names = {term.value.name for term in terms if isinstance(term.value, ABCSeries)}
    name = names.pop() if len(names) == 1 else None

    # perform the main alignment
    typ, axes = _align_core(terms)
    return typ, axes, name

