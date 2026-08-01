
def tokenize_attribute(iterable, attribute):
    """Parse a raw string in header (e.g., starts by @attribute).

    Given a raw string attribute, try to get the name and type of the
    attribute. Constraints:

    * The first line must start with @attribute (case insensitive, and
      space like characters before @attribute are allowed)
    * Works also if the attribute is spread on multilines.
    * Works if empty lines or comments are in between

    Parameters
    ----------
    attribute : str
       the attribute string.

    Returns
    -------
    name : str
       name of the attribute
    value : str
       value of the attribute
    next : str
       next line to be parsed

    Examples
    --------
    If attribute is a string defined in python as r"floupi real", will
    return floupi as name, and real as value.

    >>> from scipy.io.arff._arffread import tokenize_attribute
    >>> iterable = iter([0] * 10) # dummy iterator
    >>> tokenize_attribute(iterable, r"@attribute floupi real")
    ('floupi', 'real', 0)

    If attribute is r"'floupi 2' real", will return 'floupi 2' as name,
    and real as value.

    >>> tokenize_attribute(iterable, r"  @attribute 'floupi 2' real   ")
    ('floupi 2', 'real', 0)

    """
    sattr = attribute.strip()
    mattr = r_attribute.match(sattr)
    if mattr:
        # atrv is everything after @attribute
        atrv = mattr.group(1)
        if r_comattrval.match(atrv):
            name, type = tokenize_single_comma(atrv)
            next_item = next(iterable)
        elif r_wcomattrval.match(atrv):
            name, type = tokenize_single_wcomma(atrv)
            next_item = next(iterable)
        else:
            # Not sure we should support this, as it does not seem supported by
            # weka.
            raise ValueError("multi line not supported yet")
    else:
        raise ValueError(f"First line unparsable: {sattr}")

    attribute = to_attribute(name, type)

    if type.lower() == 'relational':
        next_item = read_relational_attribute(iterable, attribute, next_item)
    #    raise ValueError("relational attributes not supported yet")

    return attribute, next_item

